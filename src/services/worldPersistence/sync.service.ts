/**
 * World Sync Service - Cross-device synchronization
 * Handles synchronization between IndexedDB local storage and remote server
 */

import { worldPersistenceService } from './indexedDB.service';
import type {
  WorldState,
  ConflictResolution,
  SyncStatus,
  ExportData
} from '../../types/world.types';

// Sync Configuration
const SYNC_CONFIG = {
  SYNC_INTERVAL: 30000, // 30 seconds
  MAX_CONFLICTS: 50,
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000,
  BATCH_SIZE: 10,
  COMPRESSION_THRESHOLD: 1024 * 100 // 100KB
};

export interface SyncOptions {
  force?: boolean;
  batchSize?: number;
  resolveConflicts?: boolean;
  compression?: boolean;
  onProgress?: (progress: number) => void;
}

export interface SyncResult {
  success: boolean;
  worldId: string;
  conflicts: ConflictResolution[];
  uploaded: number;
  downloaded: number;
  errors: string[];
  duration: number;
}

export interface SyncStatus {
  lastSync?: Date;
  syncPending: boolean;
  conflicts: ConflictResolution[];
  remoteVersion?: number;
  syncError?: string;
  retryCount: number;
  lastAttempt?: Date;
}

export interface ConflictResolutionStrategy {
  id: string;
  description: string;
  resolve: (local: any, remote: any) => any;
  requiresUserInput: boolean;
}

class WorldSyncService {
  private syncInProgress: Map<string, boolean> = new Map();
  private syncQueue: Map<string, Array<() => Promise<void>>> = new Map();
  private conflictStrategies: Map<string, ConflictResolutionStrategy> = new Map();
  private syncStatus: Map<string, SyncStatus> = new Map();
  private syncTimer: NodeJS.Timeout | null = null;
  private isOnline: boolean = navigator.onLine;

  constructor() {
    this.initializeConflictStrategies();
    this.setupNetworkMonitoring();
    this.startPeriodicSync();
  }

  /**
   * Initialize default conflict resolution strategies
   */
  private initializeConflictStrategies(): void {
    this.conflictStrategies.set('last_write_wins', {
      id: 'last_write_wins',
      description: 'Use the most recent version',
      resolve: (local, remote) => {
        return new Date(local.metadata.lastModified) > new Date(remote.metadata.lastModified) ? local : remote;
      },
      requiresUserInput: false
    });

    this.conflictStrategies.set('local_wins', {
      id: 'local_wins',
      description: 'Always prefer local version',
      resolve: (local) => local,
      requiresUserInput: false
    });

    this.conflictStrategies.set('remote_wins', {
      id: 'remote_wins',
      description: 'Always prefer remote version',
      resolve: (_, remote) => remote,
      requiresUserInput: false
    });

    this.conflictStrategies.set('merge', {
      id: 'merge',
      description: 'Intelligently merge both versions',
      resolve: (local, remote) => {
        return this.intelligentMerge(local, remote);
      },
      requiresUserInput: false
    });

    this.conflictStrategies.set('user_choice', {
      id: 'user_choice',
      description: 'Prompt user to resolve',
      resolve: (local, remote) => {
        // This will be handled by UI layer
        throw new Error('User resolution required');
      },
      requiresUserInput: true
    });
  }

  /**
   * Setup network status monitoring
   */
  private setupNetworkMonitoring(): void {
    window.addEventListener('online', () => {
      this.isOnline = true;
      console.log('Network online - resuming sync operations');
      this.processSyncQueue();
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
      console.log('Network offline - pausing sync operations');
    });
  }

  /**
   * Start periodic sync timer
   */
  private startPeriodicSync(): void {
    if (this.syncTimer) {
      clearInterval(this.syncTimer);
    }

    this.syncTimer = setInterval(() => {
      if (this.isOnline) {
        this.syncAllPendingWorlds();
      }
    }, SYNC_CONFIG.SYNC_INTERVAL);
  }

  /**
   * Sync a specific world
   */
  async syncWorld(worldId: string, options: SyncOptions = {}): Promise<SyncResult> {
    if (!this.isOnline) {
      return {
        success: false,
        worldId,
        conflicts: [],
        uploaded: 0,
        downloaded: 0,
        errors: ['Offline - sync deferred'],
        duration: 0
      };
    }

    if (this.syncInProgress.get(worldId)) {
      console.log(`Sync already in progress for world: ${worldId}`);
      return {
        success: false,
        worldId,
        conflicts: [],
        uploaded: 0,
        downloaded: 0,
        errors: ['Sync already in progress'],
        duration: 0
      };
    }

    const startTime = Date.now();
    this.syncInProgress.set(worldId, true);

    try {
      console.log(`Starting sync for world: ${worldId}`);
      options.onProgress?.(0);

      // Get local world state
      const localWorld = await worldPersistenceService.loadWorld(worldId);
      options.onProgress?.(10);

      // Fetch remote world state
      const remoteWorld = await this.fetchRemoteWorld(worldId);
      options.onProgress?.(20);

      if (!remoteWorld) {
        // No remote version - upload local
        await this.uploadWorld(worldId, localWorld, options);
        options.onProgress?.(100);

        return {
          success: true,
          worldId,
          conflicts: [],
          uploaded: 1,
          downloaded: 0,
          errors: [],
          duration: Date.now() - startTime
        };
      }

      // Compare versions and resolve conflicts
      const comparison = this.compareWorldVersions(localWorld, remoteWorld);
      options.onProgress?.(30);

      if (comparison.isIdentical) {
        console.log('Local and remote versions are identical');
        options.onProgress?.(100);
        return {
          success: true,
          worldId,
          conflicts: [],
          uploaded: 0,
          downloaded: 0,
          errors: [],
          duration: Date.now() - startTime
        };
      }

      // Resolve conflicts
      const conflicts = await this.resolveConflicts(localWorld, remoteWorld, comparison.differences);
      options.onProgress?.(50);

      // Apply resolved state
      let resolvedWorld = localWorld;
      if (conflicts.length > 0) {
        resolvedWorld = this.applyConflictResolution(localWorld, remoteWorld, conflicts);
      }

      // Upload merged result
      if (conflicts.some(c => c.resolution !== 'skipped')) {
        await this.uploadWorld(worldId, resolvedWorld, options);
        options.onProgress?.(75);
      }

      // Update sync status
      await this.updateSyncStatus(worldId, {
        lastSync: new Date(),
        syncPending: false,
        conflicts,
        remoteVersion: remoteWorld.metadata.version
      });

      options.onProgress?.(100);

      console.log(`Sync completed for world: ${worldId}`);

      return {
        success: true,
        worldId,
        conflicts,
        uploaded: 1,
        downloaded: conflicts.some(c => c.resolution === 'remote_wins') ? 1 : 0,
        errors: [],
        duration: Date.now() - startTime
      };

    } catch (error) {
      console.error(`Sync failed for world ${worldId}:`, error);

      const syncStatus = this.syncStatus.get(worldId) || {
        syncPending: true,
        conflicts: [],
        retryCount: 0
      };

      this.updateSyncStatus(worldId, {
        ...syncStatus,
        syncError: error.message,
        lastAttempt: new Date(),
        retryCount: syncStatus.retryCount + 1
      });

      return {
        success: false,
        worldId,
        conflicts: [],
        uploaded: 0,
        downloaded: 0,
        errors: [error.message],
        duration: Date.now() - startTime
      };

    } finally {
      this.syncInProgress.set(worldId, false);
    }
  }

  /**
   * Compare local and remote world versions
   */
  private compareWorldVersions(local: WorldState, remote: WorldState): {
    isIdentical: boolean;
    differences: string[];
    localNewer: boolean;
    remoteNewer: boolean;
  } {
    const differences: string[] = [];

    // Compare metadata
    if (local.metadata.version !== remote.metadata.version) {
      differences.push(`Version mismatch: local=${local.metadata.version}, remote=${remote.metadata.version}`);
    }

    if (local.metadata.lastModified.getTime() !== remote.metadata.lastModified.getTime()) {
      const localNewer = new Date(local.metadata.lastModified) > new Date(remote.metadata.lastModified);
      differences.push(`Last modified: local(${local.metadata.lastModified}) ${localNewer ? 'NEWER' : 'OLDER'} than remote(${remote.metadata.lastModified})`);
    }

    // Compare elements
    const localElementIds = new Set(local.elements.map(el => el.id));
    const remoteElementIds = new Set(remote.elements.map(el => el.id));

    const localOnly = [...localElementIds].filter(id => !remoteElementIds.has(id));
    const remoteOnly = [...remoteElementIds].filter(id => !localElementIds.has(id));
    const common = [...localElementIds].filter(id => remoteElementIds.has(id));

    if (localOnly.length > 0) {
      differences.push(`Local-only elements: ${localOnly.join(', ')}`);
    }

    if (remoteOnly.length > 0) {
      differences.push(`Remote-only elements: ${remoteOnly.join(', ')}`);
    }

    // Compare modified elements
    common.forEach(elementId => {
      const localElement = local.elements.find(el => el.id === elementId);
      const remoteElement = remote.elements.find(el => el.id === elementId);

      if (localElement && remoteElement) {
        const localHash = this.generateElementHash(localElement);
        const remoteHash = this.generateElementHash(remoteElement);

        if (localHash !== remoteHash) {
          differences.push(`Element ${elementId} has been modified differently`);
        }
      }
    });

    // Compare branches
    if (local.branches.length !== remote.branches.length) {
      differences.push(`Branch count mismatch: local=${local.branches.length}, remote=${remote.branches.length}`);
    }

    const localNewer = new Date(local.metadata.lastModified) > new Date(remote.metadata.lastModified);
    const remoteNewer = new Date(remote.metadata.lastModified) > new Date(local.metadata.lastModified);

    return {
      isIdentical: differences.length === 0,
      differences,
      localNewer,
      remoteNewer
    };
  }

  /**
   * Resolve conflicts between local and remote versions
   */
  private async resolveConflicts(
    local: WorldState,
    remote: WorldState,
    differences: string[]
  ): Promise<ConflictResolution[]> {
    const conflicts: ConflictResolution[] = [];

    for (const difference of differences) {
      const conflict: ConflictResolution = {
        conflictId: `conflict_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        type: this.categorizeConflict(difference),
        elements: this.extractElementIds(difference),
        branches: [],
        resolution: 'pending',
        timestamp: new Date()
      };

      // Attempt to resolve using configured strategies
      const resolutionStrategy = this.determineResolutionStrategy(conflict.type);

      try {
        const strategy = this.conflictStrategies.get(resolutionStrategy);
        if (!strategy) {
          conflict.resolution = 'manual_resolution';
          conflict.resolutionTimestamp = new Date();
        } else if (strategy.requiresUserInput) {
          conflict.resolution = 'manual_resolution';
        } else {
          // Auto-resolve
          const resolved = strategy.resolve(local, remote);
          conflict.resolution = resolutionStrategy;
          conflict.resolutionTimestamp = new Date();
        }
      } catch (error) {
        conflict.resolution = 'failed';
        conflict.resolutionTimestamp = new Date();
      }

      conflicts.push(conflict);
    }

    return conflicts;
  }

  /**
   * Apply conflict resolution to generate final world state
   */
  private applyConflictResolution(
    local: WorldState,
    remote: WorldState,
    conflicts: ConflictResolution[]
  ): WorldState {
    let resolvedWorld = { ...local };

    conflicts.forEach(conflict => {
      switch (conflict.resolution) {
        case 'remote_wins':
          resolvedWorld = remote;
          break;
        case 'local_wins':
          // Keep local version
          break;
        case 'merge':
          resolvedWorld = this.intelligentMerge(local, remote);
          break;
        case 'manual_resolution':
          // Handled by UI layer
          break;
      }
    });

    return resolvedWorld;
  }

  /**
   * Intelligent merge of local and remote worlds
   */
  private intelligentMerge(local: WorldState, remote: WorldState): WorldState {
    const merged: WorldState = {
      ...local,
      metadata: {
        ...local.metadata,
        version: Math.max(local.metadata.version, remote.metadata.version) + 1,
        lastModified: new Date()
      },
      elements: this.mergeElements(local.elements, remote.elements),
      branches: this.mergeBranches(local.branches, remote.branches),
      patterns: this.mergePatterns(local.patterns, remote.patterns)
    };

    return merged;
  }

  /**
   * Merge elements with conflict resolution
   */
  private mergeElements(local: WorldElement[], remote: WorldElement[]): WorldElement[] {
    const localMap = new Map(local.map(el => [el.id, el]));
    const remoteMap = new Map(remote.map(el => [el.id, el]));

    const allIds = new Set([...localMap.keys(), ...remoteMap.keys()]);
    const merged: WorldElement[] = [];

    allIds.forEach(id => {
      const localEl = localMap.get(id);
      const remoteEl = remoteMap.get(id);

      if (localEl && remoteEl) {
        // Both versions exist - take the newer one
        const localNewer = new Date(localEl.metadata.lastModified) > new Date(remoteEl.metadata.lastModified);
        merged.push(localNewer ? localEl : remoteEl);
      } else if (localEl) {
        merged.push(localEl);
      } else if (remoteEl) {
        merged.push(remoteEl);
      }
    });

    return merged;
  }

  /**
   * Merge branches with conflict resolution
   */
  private mergeBranches(local: WorldBranch[], remote: WorldBranch[]): WorldBranch[] {
    const localMap = new Map(local.map(br => [br.id, br]));
    const remoteMap = new Map(remote.map(br => [br.id, br]));

    const allIds = new Set([...localMap.keys(), ...remoteMap.keys()]);
    const merged: WorldBranch[] = [];

    allIds.forEach(id => {
      const localBr = localMap.get(id);
      const remoteBr = remoteMap.get(id);

      if (localBr && remoteBr) {
        // Both versions exist - preserve both with conflict markers
        const newer = new Date(localBr.divergencePoint) > new Date(remoteBr.divergencePoint) ? localBr : remoteBr;
        merged.push({
          ...newer,
          name: `${newer.name} (Merged)`,
          description: `${newer.description} \n[Auto-merged from conflict]`
        });
      } else if (localBr) {
        merged.push(localBr);
      } else if (remoteBr) {
        merged.push(remoteBr);
      }
    });

    return merged;
  }

  /**
   * Merge patterns with conflict resolution
   */
  private mergePatterns(local: any[], remote: any[]): any[] {
    // Simple append for patterns - they're aggregated data
    return [...local, ...remote];
  }

  /**
   * Fetch world from remote server
   */
  private async fetchRemoteWorld(worldId: string): Promise<WorldState | null> {
    try {
      const response = await fetch(`/api/worlds/${worldId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${await this.getAuthToken()}`
        }
      });

      if (response.status === 404) {
        return null; // World doesn't exist remotely
      }

      if (!response.ok) {
        throw new Error(`Failed to fetch remote world: ${response.statusText}`);
      }

      const data = await response.json();
      return this.deserializeWorld(data);

    } catch (error) {
      console.error(`Failed to fetch remote world: ${worldId}`, error);
      throw error;
    }
  }

  /**
   * Upload world to remote server
   */
  private async uploadWorld(worldId: string, world: WorldState, options: SyncOptions): Promise<void> {
    try {
      let dataToUpload = world;
      let compressed = false;

      // Compress if enabled and above threshold
      if (options.compression && this.shouldCompressData(world)) {
        const exportData = await worldPersistenceService.exportWorld(worldId, 'compressed');
        dataToUpload = exportData.worldState;
        compressed = true;
      }

      const serialized = this.serializeWorld(dataToUpload);

      const response = await fetch(`/api/worlds/${worldId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${await this.getAuthToken()}`,
          'X-Compressed': compressed.toString(),
          'X-Version': world.metadata.version.toString()
        },
        body: JSON.stringify(serialized)
      });

      if (!response.ok) {
        throw new Error(`Failed to upload world: ${response.statusText}`);
      }

      console.log(`World uploaded successfully: ${worldId}`);

    } catch (error) {
      console.error(`Failed to upload world: ${worldId}`, error);
      throw error;
    }
  }

  /**
   * Sync all worlds with pending changes
   */
  private async syncAllPendingWorlds(): Promise<SyncResult[]> {
    try {
      const worldList = await worldPersistenceService.getWorldList();
      const syncResults: SyncResult[] = [];

      for (const worldInfo of worldList) {
        const status = this.syncStatus.get(worldInfo.id);
        if (status?.syncPending && !this.syncInProgress.get(worldInfo.id)) {
          console.log(`Syncing pending world: ${worldInfo.id}`);
          const result = await this.syncWorld(worldInfo.id);
          syncResults.push(result);
        }
      }

      return syncResults;

    } catch (error) {
      console.error('Failed to sync all pending worlds:', error);
      return [];
    }
  }

  /**
   * Update sync status for a world
   */
  private async updateSyncStatus(worldId: string, status: Partial<SyncStatus>): Promise<void> {
    const currentStatus = this.syncStatus.get(worldId) || {
      syncPending: false,
      conflicts: [],
      retryCount: 0
    };

    const newStatus = { ...currentStatus, ...status };
    this.syncStatus.set(worldId, newStatus);

    // Persist sync status to database
    try {
      const world = await worldPersistenceService.loadWorld(worldId);
      if (world._syncStatus) {
        world._syncStatus = newStatus;
        await worldPersistenceService.saveWorld(world, { sync: false });
      }
    } catch (error) {
      console.error(`Failed to update sync status for world ${worldId}:`, error);
    }
  }

  /**
   * Process sync queue for online/offline handling
   */
  private processSyncQueue(): void {
    if (!this.isOnline) return;

    this.syncQueue.forEach((queue, worldId) => {
      if (queue.length > 0) {
        console.log(`Processing sync queue for world: ${worldId}`);
        queue.forEach(syncTask => syncTask());
        queue.length = 0; // Clear queue
      }
    });
  }

  // Utility methods

  private serializeWorld(world: WorldState): any {
    return {
      ...world,
      // Convert Dates to ISO strings for JSON serialization
      metadata: {
        ...world.metadata,
        createdAt: world.metadata.createdAt.toISOString(),
        lastModified: world.metadata.lastModified.toISOString()
      }
    };
  }

  private deserializeWorld(data: any): WorldState {
    return {
      ...data,
      metadata: {
        ...data.metadata,
        createdAt: new Date(data.metadata.createdAt),
        lastModified: new Date(data.metadata.lastModified)
      }
    };
  }

  private generateElementHash(element: any): string {
    // Simple hash generation - in production use proper hash function
    return btoa(JSON.stringify(element));
  }

  private categorizeConflict(difference: string): string {
    if (difference.includes('Element')) return 'element_conflict';
    if (difference.includes('Branch')) return 'branch_conflict';
    if (difference.includes('Version')) return 'version_conflict';
    return 'unknown_conflict';
  }

  private extractElementIds(difference: string): string[] {
    const match = difference.match(/[a-f0-9-]{36}/g);
    return match || [];
  }

  private determineResolutionStrategy(conflictType: string): string {
    switch (conflictType) {
      case 'element_conflict':
        return 'merge';
      case 'branch_conflict':
        return 'merge';
      case 'version_conflict':
        return 'last_write_wins';
      default:
        return 'user_choice';
    }
  }

  private shouldCompressData(world: WorldState): boolean {
    const size = JSON.stringify(world).length;
    return size > SYNC_CONFIG.COMPRESSION_THRESHOLD;
  }

  private async getAuthToken(): Promise<string> {
    // Get authentication token from localStorage or auth service
    return localStorage.getItem('authToken') || '';
  }

  /**
   * Get sync status for a world
   */
  getSyncStatus(worldId: string): SyncStatus | undefined {
    return this.syncStatus.get(worldId);
  }

  /**
   * Get all sync statuses
   */
  getAllSyncStatuses(): Map<string, SyncStatus> {
    return new Map(this.syncStatus);
  }

  /**
   * Add custom conflict resolution strategy
   */
  addConflictStrategy(strategy: ConflictResolutionStrategy): void {
    this.conflictStrategies.set(strategy.id, strategy);
  }

  /**
   * Stop sync service
   */
  stop(): void {
    if (this.syncTimer) {
      clearInterval(this.syncTimer);
      this.syncTimer = null;
    }

    // Cancel any in-progress syncs
    this.syncInProgress.clear();
    this.syncQueue.clear();

    console.log('World sync service stopped');
  }
}

// Export singleton instance
export const worldSyncService = new WorldSyncService();
export default WorldSyncService;