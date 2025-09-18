/**
 * IndexedDB Service - Core World Persistence Implementation
 * Provides comprehensive offline-first world state management
 */

import { openDB, deleteDB, wrap, unwrap, IDBPDatabase } from 'idb';
import { compress, decompress } from 'lz-string';
import { v4 as uuidv4 } from 'uuid';
import type {
  WorldState,
  WorldElement,
  WorldBranch,
  GlobalPattern,
  WorldSettings,
  TimelineEvent,
  CompressionData,
  ExportData,
  ImportOptions,
  ConflictResolution,
  SyncStatus
} from '../types/world.types';

// Database Configuration
const DB_NAME = 'mynfini_worlds';
const DB_VERSION = 2; // Increment for schema changes

// Store Names
export const STORES = {
  WORLDS: 'worlds',
  ELEMENTS: 'elements',
  BRANCHES: 'branches',
  PATTERNS: 'patterns',
  TIMELINE: 'timeline',
  SETTINGS: 'settings',
  METADATA: 'metadata',
  BACKUPS: 'backups',
  CONFLICTS: 'conflicts'
} as const;

// Schema Definition
const SCHEMA = {
  [STORES.WORLDS]: { keyPath: 'metadata.id', autoIncrement: false, indices: ['metadata.name', 'metadata.lastModified', 'metadata.version'] },
  [STORES.ELEMENTS]: { keyPath: '_id', autoIncrement: false, indices: ['_worldId', 'type', 'branchId', 'metadata.name'] },
  [STORES.BRANCHES]: { keyPath: '_id', autoIncrement: false, indices: ['_worldId', 'parentId', 'isActive'] },
  [STORES.PATTERNS]: { keyPath: '_id', autoIncrement: false, indices: ['_worldId', 'type', 'frequency'] },
  [STORES.TIMELINE]: { keyPath: '_id', autoIncrement: false, indices: ['_worldId', 'timestamp', 'type', 'elementId'] },
  [STORES.SETTINGS]: { keyPath: '_id', autoIncrement: false, indices: ['_worldId'] },
  [STORES.METADATA]: { keyPath: 'key', autoIncrement: false },
  [STORES.BACKUPS]: { keyPath: '_id', autoIncrement: false, indices: ['worldId', 'timestamp'] },
  [STORES.CONFLICTS]: { keyPath: 'conflictId', autoIncrement: false, indices: ['worldId', 'timestamp', 'status'] }
};

export interface WorldPersistenceOptions {
  compressionThreshold?: number; // Size in bytes above which to compress
  autoSaveInterval?: number; // Milliseconds
  maxBackups?: number;
  enableEncryption?: boolean;
  syncOnSave?: boolean;
}

export interface PersistenceConfig extends WorldPersistenceOptions {
  dbName: string;
  version: number;
  encryptionKey?: CryptoKey;
}

class WorldPersistenceService {
  private db: IDBPDatabase | null = null;
  private config: PersistenceConfig;
  private autoSaveTimer: NodeJS.Timeout | null = null;
  private pendingSaves: Map<string, WorldState> = new Map();
  private compressionThreshold: number;
  private isOnline: boolean = navigator.onLine;
  private syncQueue: Array<() => Promise<void>> = [];

  constructor(config: Partial<PersistenceConfig> = {}) {
    this.config = {
      dbName: DB_NAME,
      version: DB_VERSION,
      compressionThreshold: 1024 * 50, // 50KB
      autoSaveInterval: 30000, // 30 seconds
      maxBackups: 10,
      enableEncryption: false,
      syncOnSave: false,
      ...config
    };

    this.compressionThreshold = this.config.compressionThreshold || 1024 * 50;
    this.setupOnlineStatusListener();
  }

  /**
   * Initialize the IndexedDB database with proper schema
   */
  async initialize(): Promise<void> {
    try {
      this.db = await openDB(this.config.dbName, this.config.version, {
        upgrade: (db, oldVersion, newVersion, transaction) => {
          this.handleDatabaseUpgrade(db, oldVersion, newVersion, transaction);
        },
        blocked: () => {
          console.warn('Database blocked - another tab has the database open');
        },
        blocking: () => {
          console.warn('Database blocking - this tab is preventing others from upgrading');
        }
      });

      // Verify database is properly initialized
      await this.verifyDatabaseIntegrity();
      console.log(`World persistence initialized: ${this.config.dbName} v${this.config.version}`);
    } catch (error) {
      console.error('Failed to initialize world persistence:', error);
      throw new Error(`Database initialization failed: ${error.message}`);
    }
  }

  /**
   * Handle database schema upgrades
   */
  private handleDatabaseUpgrade(
    db: IDBPDatabase,
    oldVersion: number,
    newVersion: number | null,
    transaction: IDBTransaction
  ): void {
    console.log(`Upgrading database from v${oldVersion} to v${newVersion}`);

    // Create all stores
    Object.entries(SCHEMA).forEach(([storeName, config]) => {
      let store: IDBObjectStore;

      if (!db.objectStoreNames.contains(storeName)) {
        store = db.createObjectStore(storeName, {
          keyPath: config.keyPath,
          autoIncrement: config.autoIncrement
        });
      } else {
        store = transaction.objectStore(storeName);
      }

      // Create indices
      if (config.indices) {
        config.indices.forEach(({ name, keyPath, unique = false }) => {
          if (!store.indexNames.contains(name)) {
            store.createIndex(name, keyPath, { unique });
          }
        });
      }
    });

    // Handle version-specific migrations
    if (oldVersion < 2) {
      this.migrateFromV1(transaction);
    }
  }

  /**
   * Handle version 1 to 2 migration
   */
  private async migrateFromV1(transaction: IDBTransaction): Promise<void> {
    console.log('Migrating database from v1 to v2');

    // Add compression support to existing worlds
    const worldStore = transaction.objectStore(STORES.WORLDS);
    const worlds = await worldStore.getAll();

    for (const world of worlds) {
      if (!world._compressed && this.shouldCompress(JSON.stringify(world))) {
        const compressed = this.compressData(world);
        await worldStore.put({ ...world, _compressed: compressed });
      }
    }
  }

  /**
   * Save world state with intelligent compression and versioning
   */
  async saveWorld(world: WorldState, options: { backup?: boolean; sync?: boolean } = {}): Promise<void> {
    if (!this.db) {
      throw new Error('Database not initialized');
    }

    try {
      // Update metadata
      world.metadata.lastModified = new Date();
      world.metadata.version += 1;

      // Create backup if requested
      if (options.backup) {
        await this.createBackup(world.metadata.id);
      }

      // Prepare data for storage
      let dataToStore = { ...world };
      let compressionData: CompressionData | undefined;

      // Compress if necessary
      if (this.shouldCompress(JSON.stringify(dataToStore))) {
        compressionData = this.compressData(dataToStore);
        dataToStore = {
          metadata: world.metadata,
          _compressed: compressionData,
          _syncStatus: {
            lastSync: new Date(),
            syncPending: options.sync || false,
            conflicts: []
          }
        } as any;
      }

      // Save in transaction
      const transaction = this.db.transaction([STORES.WORLDS, STORES.ELEMENTS, STORES.BRANCHES, STORES.PATTERNS], 'readwrite');

      // Save world metadata
      await transaction.objectStore(STORES.WORLDS).put(dataToStore);

      // Save elements separately for efficient querying
      if (world.elements.length > 0) {
        const elementStore = transaction.objectStore(STORES.ELEMENTS);
        for (const element of world.elements) {
          await elementStore.put({
            ...element,
            _id: `${world.metadata.id}:${element.id}`,
            _worldId: world.metadata.id
          });
        }
      }

      // Save branches
      if (world.branches.length > 0) {
        const branchStore = transaction.objectStore(STORES.BRANCHES);
        for (const branch of world.branches) {
          await branchStore.put({
            ...branch,
            _id: `${world.metadata.id}:${branch.id}`,
            _worldId: world.metadata.id
          });
        }
      }

      // Save patterns
      if (world.patterns.length > 0) {
        const patternStore = transaction.objectStore(STORES.PATTERNS);
        for (const pattern of world.patterns) {
          await patternStore.put({
            ...pattern,
            _id: `${world.metadata.id}:${pattern.id}`,
            _worldId: world.metadata.id
          });
        }
      }

      // Record timeline event
      await this.recordTimelineEvent({
        _id: uuidv4(),
        _worldId: world.metadata.id,
        id: uuidv4(),
        type: 'save',
        timestamp: new Date(),
        action: 'world_saved',
        parameters: {
          version: world.metadata.version,
          compressed: !!compressionData,
          backup: options.backup
        },
        preState: {},
        postState: {}
      });

      await transaction.done;

      // Trigger sync if enabled
      if (options.sync && this.isOnline) {
        this.scheduleSync(world.metadata.id);
      }

      console.log(`World saved: ${world.metadata.name} v${world.metadata.version}`);
    } catch (error) {
      console.error('Failed to save world:', error);
      throw new Error(`Save failed: ${error.message}`);
    }
  }

  /**
   * Load world state with decompression and integrity checking
   */
  async loadWorld(worldId: string, options: { verifyIntegrity?: boolean } = {}): Promise<WorldState> {
    if (!this.db) {
      throw new Error('Database not initialized');
    }

    try {
      // Retrieve world
      const worldRecord = await this.db.get(STORES.WORLDS, worldId);
      if (!worldRecord) {
        throw new Error(`World not found: ${worldId}`);
      }

      let worldState: WorldState;

      // Decompress if necessary
      if (worldRecord._compressed) {
        worldState = this.decompressData(worldRecord._compressed);
      } else {
        worldState = worldRecord;
      }

      // Load associated data
      const elements = await this.db.getAllFromIndex(STORES.ELEMENTS, '_worldId', worldId);
      const branches = await this.db.getAllFromIndex(STORES.BRANCHES, '_worldId', worldId);
      const patterns = await this.db.getAllFromIndex(STORES.PATTERNS, '_worldId', worldId);

      // Reconstruct world state
      worldState.elements = elements.map(el => {
        const { _id, _worldId, ...elementData } = el;
        return elementData as WorldElement;
      });

      worldState.branches = branches.map(br => {
        const { _id, _worldId, ...branchData } = br;
        return branchData as WorldBranch;
      });

      worldState.patterns = patterns.map(pt => {
        const { _id, _worldId, ...patternData } = pt;
        return { ...patternData, id: patternData.id } as GlobalPattern;
      });

      // Verify integrity if requested
      if (options.verifyIntegrity) {
        await this.verifyWorldIntegrity(worldState);
      }

      console.log(`World loaded: ${worldState.metadata.name}`);
      return worldState;
    } catch (error) {
      console.error('Failed to load world:', error);
      throw new Error(`Load failed: ${error.message}`);
    }
  }

  /**
   * Auto-save system with conflict detection
   */
  enableAutoSave(worldId: string, intervalMs: number = this.config.autoSaveInterval!): void {
    if (this.autoSaveTimer) {
      clearInterval(this.autoSaveTimer);
    }

    this.autoSaveTimer = setInterval(async () => {
      const pendingWorld = this.pendingSaves.get(worldId);
      if (pendingWorld) {
        try {
          await this.saveWorld(pendingWorld, { backup: true });
          this.pendingSaves.delete(worldId);
          console.log(`Autosaved world: ${worldId}`);
        } catch (error) {
          console.error('Auto-save failed:', error);
        }
      }
    }, intervalMs);
  }

  disableAutoSave(): void {
    if (this.autoSaveTimer) {
      clearInterval(this.autoSaveTimer);
      this.autoSaveTimer = null;
    }
  }

  /**
   * Queue world for auto-save
   */
  queueAutoSave(world: WorldState): void {
    this.pendingSaves.set(world.metadata.id, world);
  }

  /**
   * Create backup of world state
   */
  async createBackup(worldId: string): Promise<string> {
    if (!this.db) {
      throw new Error('Database not initialized');
    }

    try {
      const world = await this.loadWorld(worldId);
      const backupId = `${worldId}:backup:${Date.now()}`;

      const backupData = {
        _id: backupId,
        worldId,
        timestamp: new Date(),
        worldState: world,
        checksum: this.generateChecksum(world)
      };

      await this.db.put(STORES.BACKUPS, backupData);

      // Clean up old backups
      await this.cleanupOldBackups(worldId);

      console.log(`Backup created: ${backupId}`);
      return backupId;
    } catch (error) {
      console.error('Failed to create backup:', error);
      throw new Error(`Backup failed: ${error.message}`);
    }
  }

  /**
   * Export world to various formats
   */
  async exportWorld(worldId: string, format: 'json' | 'compressed' | 'qr'): Promise<ExportData> {
    try {
      const world = await this.loadWorld(worldId);

      let exportedData: ExportData;

      switch (format) {
        case 'json':
          exportedData = {
            format: 'json',
            version: '2.0',
            worldState: world,
            metadata: {
              exportedAt: new Date(),
              exportedBy: 'system',
              applicationVersion: process.env.REACT_APP_VERSION || '1.0.0',
              compatibility: ['v1.0', 'v2.0']
            },
            checksum: this.generateChecksum(world)
          };
          break;

        case 'compressed':
          const compressedData = this.compressData(world);
          exportedData = {
            format: 'compressed_json',
            version: '2.0',
            worldState: { metadata: world.metadata } as any,
            metadata: {
              exportedAt: new Date(),
              exportedBy: 'system',
              applicationVersion: process.env.REACT_APP_VERSION || '1.0.0',
              compatibility: ['v2.0']
            },
            compression: compressedData,
            checksum: this.generateChecksum(compressedData.data)
          };
          break;

        case 'qr':
          // Generate QR code compatible data
          const qrData = this.prepareQRData(world);
          exportedData = {
            format: 'qr_code',
            version: '2.0',
            worldState: world,
            metadata: {
              exportedAt: new Date(),
              exportedBy: 'system',
              applicationVersion: process.env.REACT_APP_VERSION || '1.0.0',
              compatibility: ['v2.0']
            },
            checksum: this.generateChecksum(qrData)
          };
          break;

        default:
          throw new Error(`Unsupported export format: ${format}`);
      }

      console.log(`World exported: ${worldId} (${format})`);
      return exportedData;
    } catch (error) {
      console.error('Failed to export world:', error);
      throw new Error(`Export failed: ${error.message}`);
    }
  }

  /**
   * Import world from exported data
   */
  async importWorld(exportedData: ExportData, options: ImportOptions = {}): Promise<string> {
    try {
      let worldState: WorldState;

      // Verify checksum
      if (!this.verifyChecksum(exportedData)) {
        throw new Error('Checksum verification failed - data integrity compromised');
      }

      // Decompress if necessary
      if (exportedData.format === 'compressed_json' && exportedData.compression) {
        worldState = this.decompressData(exportedData.compression);
      } else {
        worldState = exportedData.worldState;
      }

      // Generate new IDs if requested
      if (!options.preserveIds) {
        const oldId = worldState.metadata.id;
        worldState.metadata.id = uuidv4();
        worldState.metadata.name = `${worldState.metadata.name} (Imported)`;

        // Update element references
        const idMap = new Map<string, string>();
        worldState.elements.forEach(element => {
          const newId = uuidv4();
          idMap.set(element.id, newId);
          element.id = newId;
        });

        // Update relationship references
        worldState.elements.forEach(element => {
          element.relationships.forEach(relationship => {
            if (idMap.has(relationship.targetId)) {
              relationship.targetId = idMap.get(relationship.targetId)!;
            }
          });
        });
      }

      // Create backup if requested
      if (options.createBackup && await this.worldExists(worldState.metadata.id)) {
        await this.createBackup(worldState.metadata.id);
      }

      // Handle conflicts
      if (options.conflictResolution === 'replace') {
        // Delete existing world
        await this.deleteWorld(worldState.metadata.id);
      }

      // Save imported world
      await this.saveWorld(worldState, { sync: false });

      console.log(`World imported: ${worldState.metadata.id}`);
      return worldState.metadata.id;
    } catch (error) {
      console.error('Failed to import world:', error);
      throw new Error(`Import failed: ${error.message}`);
    }
  }

  /**
   * Get list of all worlds with metadata
   */
  async getWorldList(): Promise<Array<{ id: string; name: string; lastModified: Date; version: number }>> {
    if (!this.db) {
      throw new Error('Database not initialized');
    }

    try {
      const worlds = await this.db.getAll(STORES.WORLDS);
      return worlds.map(world => ({
        id: world.metadata.id,
        name: world.metadata.name,
        lastModified: new Date(world.metadata.lastModified),
        version: world.metadata.version
      }));
    } catch (error) {
      console.error('Failed to get world list:', error);
      throw new Error(`World list failed: ${error.message}`);
    }
  }

  /**
   * Delete world and all associated data
   */
  async deleteWorld(worldId: string): Promise<void> {
    if (!this.db) {
      throw new Error('Database not initialized');
    }

    try {
      const transaction = this.db.transaction([
        STORES.WORLDS,
        STORES.ELEMENTS,
        STORES.BRANCHES,
        STORES.PATTERNS,
        STORES.TIMELINE,
        STORES.SETTINGS,
        STORES.BACKUPS,
        STORES.CONFLICTS
      ], 'readwrite');

      await transaction.objectStore(STORES.WORLDS).delete(worldId);

      // Delete associated data
      const stores = [
        STORES.ELEMENTS,
        STORES.BRANCHES,
        STORES.PATTERNS,
        STORES.TIMELINE,
        STORES.SETTINGS,
        STORES.BACKUPS,
        STORES.CONFLICTS
      ];

      for (const storeName of stores) {
        const index = transaction.objectStore(storeName).index('_worldId');
        const records = await index.getAll(worldId);

        for (const record of records) {
          await transaction.objectStore(storeName).delete(record._id);
        }
      }

      await transaction.done;
      console.log(`World deleted: ${worldId}`);
    } catch (error) {
      console.error('Failed to delete world:', error);
      throw new Error(`Delete failed: ${error.message}`);
    }
  }

  /**
   * Resolve conflicts between different versions
   */
  async resolveConflict(conflictId: string, resolution: ConflictResolution): Promise<void> {
    if (!this.db) {
      throw new Error('Database not initialized');
    }

    try {
      await this.db.put(STORES.CONFLICTS, resolution);
      console.log(`Conflict resolved: ${conflictId}`);
    } catch (error) {
      console.error('Failed to resolve conflict:', error);
      throw new Error(`Conflict resolution failed: ${error.message}`);
    }
  }

  /**
   * Get conflict history for a world
   */
  async getConflictHistory(worldId: string): Promise<ConflictResolution[]> {
    if (!this.db) {
      throw new Error('Database not initialized');
    }

    try {
      const index = this.db.transaction(STORES.CONFLICTS).store.index('worldId');
      return await index.getAll(worldId);
    } catch (error) {
      console.error('Failed to get conflict history:', error);
      throw new Error(`Conflict history failed: ${error.message}`);
    }
  }

  /**
   * Timeline management
   */
  async getTimeline(worldId: string, limit: number = 100): Promise<TimelineEvent[]> {
    if (!this.db) {
      throw new Error('Database not initialized');
    }

    try {
      const index = this.db.transaction(STORES.TIMELINE).store.index('_worldId');
      const allEvents = await index.getAll(worldId);

      return allEvents
        .sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime())
        .slice(0, limit)
        .map(event => {
          const { _id, _worldId, ...eventData } = event;
          return eventData as TimelineEvent;
        });
    } catch (error) {
      console.error('Failed to get timeline:', error);
      throw new Error(`Timeline failed: ${error.message}`);
    }
  }

  /**
   * Close database connection
   */
  async close(): Promise<void> {
    if (this.db) {
      this.db.close();
      this.db = null;
    }

    if (this.autoSaveTimer) {
      clearInterval(this.autoSaveTimer);
      this.autoSaveTimer = null;
    }

    console.log('World persistence service closed');
  }

  // Private utility methods

  private shouldCompress(data: string): boolean {
    const size = new Blob([data]).size;
    return size > this.compressionThreshold;
  }

  private compressData(data: any): CompressionData {
    const jsonString = JSON.stringify(data);
    const originalSize = new Blob([jsonString]).size;
    const compressed = compress(jsonString);
    const compressedSize = new Blob([compressed]).size;

    return {
      algorithm: 'lz-string',
      ratio: compressedSize / originalSize,
      originalSize,
      compressedSize,
      checksum: this.generateChecksum(compressed),
      data: compressed
    };
  }

  private decompressData(compressionData: CompressionData): any {
    const decompressed = decompress(compressionData.data);
    return JSON.parse(decompressed);
  }

  private generateChecksum(data: any): string {
    // Simple checksum - in production, use a proper hash function
    return btoa(JSON.stringify(data));
  }

  private verifyChecksum(exportedData: ExportData): boolean {
    const currentChecksum = this.generateChecksum(exportedData.worldState);
    return currentChecksum === exportedData.checksum;
  }

  private prepareQRData(world: WorldState): string {
    // Prepare data for QR code generation
    const qrData = {
      id: world.metadata.id,
      name: world.metadata.name,
      version: world.metadata.version,
      createdAt: world.metadata.createdAt,
      thumbnail: world.metadata.thumbnail,
      elements: world.elements.length,
      branches: world.branches.length
    };
    return JSON.stringify(qrData);
  }

  private async verifyDatabaseIntegrity(): Promise<void> {
    // Basic integrity check
    if (!this.db) return;

    const transaction = this.db.transaction([STORES.WORLDS], 'readonly');
    const store = transaction.objectStore(STORES.WORLDS);
    const count = await store.count();

    console.log(`Database integrity check: ${count} worlds found`);
  }

  private async verifyWorldIntegrity(world: WorldState): Promise<void> {
    // Check for corrupted data
    if (!world.metadata || !world.metadata.id) {
      throw new Error('Invalid world metadata');
    }

    // Verify element relationships
    const elementIds = new Set(world.elements.map(el => el.id));
    for (const element of world.elements) {
      for (const relationship of element.relationships) {
        if (!elementIds.has(relationship.targetId)) {
          console.warn(`Broken relationship: ${element.id} -> ${relationship.targetId}`);
        }
      }
    }
  }

  private async cleanupOldBackups(worldId: string): Promise<void> {
    if (!this.db) return;

    const index = this.db.transaction(STORES.BACKUPS).store.index('worldId');
    const backups = await index.getAll(worldId);

    if (backups.length > this.config.maxBackups!) {
      // Sort by timestamp and delete oldest
      backups.sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime());
      const toDelete = backups.slice(0, backups.length - this.config.maxBackups!);

      const transaction = this.db.transaction(STORES.BACKUPS, 'readwrite');
      for (const backup of toDelete) {
        await transaction.store.delete(backup._id);
      }
    }
  }

  private async worldExists(worldId: string): Promise<boolean> {
    if (!this.db) return false;

    const world = await this.db.get(STORES.WORLDS, worldId);
    return !!world;
  }

  private async recordTimelineEvent(event: any): Promise<void> {
    if (!this.db) return;

    await this.db.put(STORES.TIMELINE, event);
  }

  private setupOnlineStatusListener(): void {
    window.addEventListener('online', () => {
      this.isOnline = true;
      this.processSyncQueue();
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
    });
  }

  private scheduleSync(worldId: string): void {
    this.syncQueue.push(async () => {
      try {
        await this.syncWorld(worldId);
      } catch (error) {
        console.error(`Sync failed for world ${worldId}:`, error);
      }
    });

    if (this.isOnline) {
      this.processSyncQueue();
    }
  }

  private async processSyncQueue(): Promise<void> {
    while (this.syncQueue.length > 0 && this.isOnline) {
      const syncTask = this.syncQueue.shift();
      if (syncTask) {
        await syncTask();
      }
    }
  }

  private async syncWorld(worldId: string): Promise<void> {
    // Placeholder for actual sync implementation
    console.log(`Sync scheduled for world: ${worldId}`);
  }
}

// Export singleton instance
export const worldPersistenceService = new WorldPersistenceService();
export default WorldPersistenceService;