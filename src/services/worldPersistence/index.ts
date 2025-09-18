/**
 * World Persistence Services - Main Export Module
 * Provides centralized access to all world persistence functionality
 */

// Core Services
export { worldPersistenceService, WorldPersistenceService, WorldPersistenceOptions } from './indexedDB.service';
export { worldSyncService, WorldSyncService, SyncOptions, SyncResult } from './sync.service';
export { worldCompressionService, WorldCompressionService, CompressionOptions, CompressionStrategy } from './compression.service';
export { worldRecoveryService, WorldRecoveryService, BackupOptions, RecoveryOptions } from './recovery.service';

// React Hooks
export {
  useWorldPersistence,
  useWorldList,
  useAutoSave,
  useWorldExport,
  WorldEventEmitter,
  worldEventEmitter
} from './hooks';

// Types
export type {
  UseWorldPersistenceReturn,
  UseWorldListReturn,
  UseAutoSaveReturn,
  UseWorldExportReturn,
  SaveOptions,
  WorldPersistenceOptions
} from './hooks';

export type {
  CompressionResult,
  DecompressionResult,
  CompressionMetrics
} from './compression.service';

export type {
  BackupMetadata,
  ValidationResult,
  ValidationError,
  ValidationWarning,
  CorruptionRecord
} from './recovery.service';

// Re-export main world types for convenience
export type {
  WorldState,
  WorldMetadata,
  WorldElement,
  WorldBranch,
  GlobalPattern,
  CreativeDNA,
  TimelineEvent,
  ConflictResolution,
  ExportData,
  ImportOptions,
  CompressionData
} from '../../types/world.types';

// Utilities
export { setupAutomaticBackups, cleanupExpiredBackups, exportBackupForSharing } from './recovery.service';

// Constants
export { COMPRESSION_PRESETS, DEFAULT_COMPRESSION_OPTIONS } from './compression.service';

// Integration helpers
export class WorldPersistenceManager {
  private static instance: WorldPersistenceManager;

  static getInstance(): WorldPersistenceManager {
    if (!WorldPersistenceManager.instance) {
      WorldPersistenceManager.instance = new WorldPersistenceManager();
    }
    return WorldPersistenceManager.instance;
  }

  /**
   * Initialize all persistence services
   */
  async initialize(): Promise<void> {
    console.log('Initializing world persistence system...');

    try {
      // Initialize IndexedDB service
      await worldPersistenceService.initialize();

      // Initialize compression service
      console.log('Compression service ready');

      // Initialize sync service
      console.log('Sync service ready');

      // Initialize recovery service
      console.log('Recovery service ready');

      console.log('✅ World persistence system initialized successfully');

    } catch (error) {
      console.error('❌ Failed to initialize world persistence system:', error);
      throw error;
    }
  }

  /**
   * Create complete world backup with all options
   */
  async createFullBackup(worldId: string, options: BackupOptions = {}): Promise<{
    backupId: string;
    metadata: BackupMetadata;
    compressed: boolean;
  }> {
    const compressionResult = await worldCompressionService.compressWorld(
      await worldPersistenceService.loadWorld(worldId)
    );

    const backupMetadata = await worldRecoveryService.createBackup(worldId, {
      ...options,
      compression: true
    });

    return {
      backupId: backupMetadata.id,
      metadata: backupMetadata,
      compressed: !!compressionResult.metadata
    };
  }

  /**
   * Quick export for sharing
   */
  async exportForSharing(worldId: string, format: 'json' | 'compressed' | 'qr' = 'compressed'): Promise<{
    data: ExportData;
    qrCode?: string;
    shareLink?: string;
  }> {
    const exportData = await worldPersistenceService.exportWorld(worldId, format);

    let qrCode: string | undefined;
    let shareLink: string | undefined;

    if (format === 'qr' || format === 'compressed') {
      // Generate QR code
      const qrDataUri = `data:text/json;base64,${btoa(JSON.stringify(exportData))}`;
      qrCode = qrDataUri;
    }

    if (format === 'compressed') {
      // Generate share link
      shareLink = `${window.location.origin}/import?data=${btoa(JSON.stringify(exportData))}`;
    }

    return { data: exportData, qrCode, shareLink };
  }

  /**
   * Validate and repair world data
   */
  async validateAndRepair(worldId: string): Promise<{
    originalValid: boolean;
    repaired: boolean;
    validationResult: ValidationResult;
  }> {
    const world = await worldPersistenceService.loadWorld(worldId);
    const validationResult = await worldRecoveryService.validateWorld(world);

    if (validationResult.isValid) {
      return {
        originalValid: true,
        repaired: false,
        validationResult
      };
    }

    // Attempt repair
    const repairedWorld = await worldRecoveryService.repairWorld(worldId, validationResult);
    const newValidationResult = await worldRecoveryService.validateWorld(repairedWorld);

    return {
      originalValid: false,
      repaired: newValidationResult.isValid,
      validationResult: newValidationResult
    };
  }

  /**
   * Get comprehensive world health report
   */
  async getWorldHealthReport(worldId: string): Promise<{
    worldId: string;
    lastModified: Date;
    version: number;
    validation: ValidationResult;
    corruptionHistory: CorruptionRecord[];
    availableBackups: BackupMetadata[];
    compressionRatio?: number;
    syncStatus?: any;
  }> {
    const world = await worldPersistenceService.loadWorld(worldId);
    const [validation, corruptionHistory, availableBackups] = await Promise.all([
      worldRecoveryService.validateWorld(world),
      Promise.resolve(worldRecoveryService.getCorruptionHistory(worldId)),
      Promise.resolve(worldRecoveryService.getAvailableBackups(worldId))
    ]);

    return {
      worldId,
      lastModified: world.metadata.lastModified,
      version: world.metadata.version,
      validation,
      corruptionHistory,
      availableBackups,
      compressionRatio: await this.calculateCompressionRatio(world),
      syncStatus: worldSyncService.getSyncStatus(worldId)
    };
  }

  /**
   * Enable automatic sync and backup
   */
  async enableAutomaticSync(worldId: string, options: {
    syncInterval?: number;
    backupInterval?: number;
    compression?: boolean;
  } = {}): Promise<void> {
    const { syncInterval = 30000, backupInterval = 300000, compression = true } = options;

    // Enable auto-sync
    if (syncInterval > 0) {
      worldSyncService.syncWorld(worldId, {
        force: false,
        resolveConflicts: true,
        compression
      });
      setInterval(() => {
        worldSyncService.syncWorld(worldId);
      }, syncInterval);
    }

    // Enable auto-backup
    if (backupInterval > 0) {
      await worldRecoveryService.createBackup(worldId, {
        automatic: true,
        compression
      });
      setInterval(() => {
        worldRecoveryService.createBackup(worldId, {
          automatic: true,
          compression
        });
      }, backupInterval);
    }
  }

  /**
   * Cleanup and shutdown all persistence services
   */
  async shutdown(): Promise<void> {
    console.log('Shutting down world persistence system...');

    try {
      await worldPersistenceService.close();
      worldSyncService.stop();

      console.log('✅ World persistence system shutdown complete');
    } catch (error) {
      console.error('❌ Error during shutdown:', error);
    }
  }

  // Private utility methods

  private async calculateCompressionRatio(world: WorldState): Promise<number> {
    const result = await worldCompressionService.compressWorld(world);
    return result.ratio;
  }
}

// Export singleton instance
export const worldPersistenceManager = WorldPersistenceManager.getInstance();

// Default configuration
export const PERSISTENCE_DEFAULTS = {
  SYNC_INTERVAL: 30000, // 30 seconds
  BACKUP_INTERVAL: 300000, // 5 minutes
  COMPRESSION_THRESHOLD: 1024 * 50, // 50KB
  MAX_BACKUPS: 10,
  RETENTION_PERIOD: 30 // days
} as const;

// Quick setup function for new applications
export async function setupWorldPersistence(options: {
  enableCompression?: boolean;
  enableSync?: boolean;
  enableAutoBackup?: boolean;
  autoSyncInterval?: number;
  autoBackupInterval?: number;
} = {}): Promise<WorldPersistenceManager> {
  const {
    enableCompression = true,
    enableSync = true,
    enableAutoBackup = true,
    autoSyncInterval,
    autoBackupInterval
  } = options;

  // Initialize persistence system
  await worldPersistenceManager.initialize();

  // Configure services based on options
  if (enableCompression) {
    console.log('Compression enabled');
  }

  if (enableSync) {
    console.log('Sync enabled');
  }

  if (enableAutoBackup) {
    console.log('Auto-backup enabled');
  }

  return worldPersistenceManager;
}