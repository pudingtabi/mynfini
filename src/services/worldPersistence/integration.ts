/**
 * World Persistence Integration Module
 * Provides integration points for React components and external services
 */

import { worldPersistenceService } from './indexedDB.service';
import { worldCompressionService } from './compression.service';
import { worldSyncService } from './sync.service';
import { worldRecoveryService } from './recovery.service';
import type { WorldState, WorldElement, WorldBranch, ExportData } from '../../types/world.types';

// Integration Interfaces
export interface PersistenceIntegrationOptions {
  autoSave?: boolean;
  validateOnSave?: boolean;
  createBackupOnSave?: boolean;
  syncOnSave?: boolean;
  compression?: boolean;
  maxRetries?: number;
}

export interface ImportExportOptions {
  format: 'json' | 'compressed' | 'qr';
  validateSchema?: boolean;
  createBackup?: boolean;
  preserveIds?: boolean;
  includeMetadata?: boolean;
}

export interface ShareOptions {
  platform: 'link' | 'qr' | 'file' | 'clipboard';
  expiration?: number; // seconds
  password?: string;
  permissions?: 'read' | 'write';
  includeHistory?: boolean;
}

export interface CollaborationOptions {
  enableRealTime?: boolean;
  userId?: string;
  permissions?: {
    canEdit?: boolean;
    canDelete?: boolean;
    canComment?: boolean;
    canBranch?: boolean;
  };
  conflictResolution?: 'auto' | 'manual' | 'last_write_wins';
}

// Utility Functions
export async function saveWorldWithValidation(
  world: WorldState,
  options: PersistenceIntegrationOptions = {}
): Promise<{
  success: boolean;
  worldId: string;
  validationErrors?: any[];
  backupId?: string;
  compressionUsed?: boolean;
}> {
  const {
    validateOnSave = true,
    createBackupOnSave = true,
    syncOnSave = false,
    compression = true,
    maxRetries = 3
  } = options;

  let attempt = 0;

  while (attempt < maxRetries) {
    try {
      // Validate world before saving if requested
      if (validateOnSave) {
        const validationResult = await worldRecoveryService.validateWorld(world);
        if (!validationResult.isValid && validationResult.errors.some(e => e.severity === 'critical')) {
          return {
            success: false,
            worldId: world.metadata.id,
            validationErrors: validationResult.errors
          };
        }
      }

      // Create backup if requested
      let backupId: string | undefined;
      if (createBackupOnSave) {
        backupId = (await worldRecoveryService.createBackup(world.metadata.id)).id;
      }

      // Save world with compression and sync options
      await worldPersistenceService.saveWorld(world, {
        backup: false, // We already created a custom backup
        sync: syncOnSave,
        compress: compression
      });

      return {
        success: true,
        worldId: world.metadata.id,
        backupId,
        compressionUsed: compression
      };

    } catch (error) {
      attempt++;
      console.error(`Save attempt ${attempt} failed:`, error);

      if (attempt >= maxRetries) {
        throw new Error(`Failed to save world after ${maxRetries} attempts: ${error.message}`);
      }

      // Wait before retry
      await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
    }
  }

  throw new Error('Failed to save world - maximum retries exceeded');
}

export async function exportWorldForSharing(
  worldId: string,
  options: ImportExportOptions
): Promise<{
  data: ExportData;
  qrCode?: string;
  shareLink?: string;
  fileSize: number;
}> {
  const {
    format,
    validateSchema = true,
    createBackup = false,
    preserveIds = true,
    includeMetadata = true
  } = options;

  try {
    // Create backup if requested
    if (createBackup) {
      await worldRecoveryService.createBackup(worldId);
    }

    // Export world data
    const exportData = await worldPersistenceService.exportWorld(worldId, format);

    // Generate share links based on format
    let qrCode: string | undefined;
    let shareLink: string | undefined;

    const shareData = exportData.worldState;
    if (format === 'qr') {
      // Generate QR code data URL
      qrCode = `data:application/json;base64,${btoa(JSON.stringify(shareData, null, 2))}`;
    } else {
      // Generate share link for compressed data
      shareLink = generateShareLink(exportData);
    }

    // Calculate file size
    const fileSize = new Blob([JSON.stringify(exportData)]).size;

    return {
      data: exportData,
      qrCode,
      shareLink,
      fileSize
    };

  } catch (error) {
    throw new Error(`Export failed: ${error.message}`);
  }
}

export async function importWorldFromFile(
  file: File,
  options: ImportExportOptions = {}
): Promise<{
  success: boolean;
  worldId?: string;
  validationErrors?: any[];
  importWarnings?: string[];
}> {
  const {
    validateSchema = true,
    createBackup = false,
    preserveIds = false
  } = options;

  let importWarnings: string[] = [];

  try {
    // Read file contents
    const fileContent = await file.text();
    let importData: ExportData;

    try {
      importData = JSON.parse(fileContent);
    } catch (parseError) {
      throw new Error('Invalid JSON format in import file');
    }

    // Validate schema if requested
    if (validateSchema) {
      const validationResult = await validateWorldSchema(importData);
      if (validationResult.errors.length > 0) {
        return {
          success: false,
          validationErrors: validationResult.errors
        };
      }

      if (validationResult.warnings.length > 0) {
        importWarnings = validationResult.warnings;
      }
    }

    // Import world
    const worldId = await worldPersistenceService.importWorld(importData, {
      preserveIds,
      validateSchema,
      createBackup,
      conflictResolution: 'merge'
    });

    return {
      success: true,
      worldId,
      importWarnings
    };

  } catch (error) {
    throw new Error(`Import failed: ${error.message}`);
  }
}

export async function collaborativeSave(
  world: WorldState,
  userId: string,
  collaborationOptions: CollaborationOptions = {}
): Promise<{
  success: boolean;
  worldId: string;
  conflictResolution?: string;
  syncStatus?: any;
}> {
  const {
    enableRealTime = true,
    permissions = { canEdit: true, canDelete: false, canComment: true, canBranch: true },
    conflictResolution = 'auto'
  } = collaborationOptions;

  try {
    // Check permissions
    if (!permissions.canEdit) {
      throw new Error('User does not have edit permissions');
    }

    // Add collaboration metadata
    const collaborativeWorld = {
      ...world,
      metadata: {
        ...world.metadata,
        lastEditor: userId,
        collaboration: {
          enabled: enableRealTime,
          lastEditor: userId,
          permissions,
          conflictResolution: conflictResolution
        }
      }
    };

    // Save with collaboration features
    await worldPersistenceService.saveWorld(collaborativeWorld, {
      backup: true,
      sync: enableRealTime
    });

    // Attempt sync if real-time is enabled
    let syncStatus: any;
    if (enableRealTime) {
      syncStatus = await worldSyncService.syncWorld(world.metadata.id, {
        resolveConflicts: conflictResolution !== 'manual',
        onProgress: (progress) => {
          console.log(`Sync progress: ${progress}%`);
        }
      });
    }

    return {
      success: true,
      worldId: world.metadata.id,
      conflictResolution,
      syncStatus
    };

  } catch (error) {
    throw new Error(`Collaborative save failed: ${error.message}`);
  }
}

export function generateQRCodeForWorld(
  worldData: WorldState,
  options: { size?: number; includeMetadata?: boolean } = {}
): {
  dataUrl: string;
  text: string;
  version: string;
} {
  const { size = 512, includeMetadata = true } = options;

  // Prepare data for QR code (limited size)
  const qrData = {
    id: worldData.metadata.id,
    name: worldData.metadata.name,
    version: worldData.metadata.version,
    createdAt: worldData.metadata.createdAt,
    elementCount: worldData.elements.length,
    branchCount: worldData.branches.length,
    ...(includeMetadata && {
      description: worldData.metadata.description,
      tags: worldData.metadata.tags
    })
  };

  const textData = JSON.stringify(qrData, null, 2);
  const dataUrl = `data:application/json;base64,${btoa(textData)}`;

  // In a real implementation, you'd use a QR code library here
  // This is a placeholder that returns the data URL and text
  return {
    dataUrl,
    text: textData,
    version: '2.0'
  };
}

export async function shareWorldViaLink(
  worldId: string,
  options: ShareOptions
): Promise<{
  shareUrl: string;
  expiresAt?: Date;
  accessCode?: string;
  qrDataUrl?: string;
}> {
  const {
    platform = 'link',
    expiration = 86400, // 24 hours default
    password,
    permissions = 'read',
    includeHistory = false
  } = options;

  try {
    // Export world data
    const exportResult = await exportWorldForSharing(worldId, {
      format: 'compressed',
      validateSchema: true,
      createBackup: false,
      preserveIds: true,
      includeMetadata: true
    });

    let shareData = exportResult.data;
    if (!includeHistory && shareData.worldState.metadata.lastModified) {
      // Remove historical timeline data for privacy
      shareData = {
        ...shareData,
        worldState: {
          ...shareData.worldState,
          branches: shareData.worldState.branches.map(branch => ({
            ...branch,
            timeline: [] // Clear timeline for privacy
          }))
        }
      };
    }

    // Generate share URL (in practice, this would be generated server-side)
    const encodedData = btoa(JSON.stringify(shareData));
    let shareUrl = `${window.location.origin}/import?data=${encodedData}`;

    let accessCode: string | undefined;
    let qrDataUrl: string | undefined;

    switch (platform) {
      case 'qr':
        const qrResult = generateQRCodeForWorld(shareData.worldState);
        qrDataUrl = qrResult.dataUrl;
        break;

      case 'clipboard':
        if (navigator.clipboard) {
          await navigator.clipboard.writeText(shareUrl);
        }
        break;

      case 'file':
        // Generate downloadable file
        const blob = new Blob([JSON.stringify(shareData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `world-${worldId}-share.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        break;
    }

    if (password) {
      // In practice, encrypt the data with the password
      shareUrl += `&access=${btoa(password)}`;
    }

    const expiresAt = new Date(Date.now() + expiration * 1000);

    return {
      shareUrl,
      expiresAt,
      accessCode: password || undefined,
      qrDataUrl
    };

  } catch (error) {
    throw new Error(`Failed to generate share link: ${error.message}`);
  }
}

// Validation utilities
async function validateWorldSchema(data: any): Promise<{
  errors: string[];
  warnings: string[];
  isValid: boolean;
}> {
  const errors: string[] = [];
  const warnings: string[] = [];

  try {
    // Check required fields
    if (!data.format) {
      errors.push('Missing format field');
    }

    if (!data.worldState) {
      errors.push('Missing worldState field');
    }

    if (data.worldState) {
      const world = data.worldState;

      // Validate metadata
      if (!world.metadata?.id) {
        errors.push('World has no ID');
      }

      if (!world.metadata?.name) {
        warnings.push('World has no name');
      }

      // Validate structure
      if (!world.elements || !Array.isArray(world.elements)) {
        errors.push('Invalid elements structure');
      }

      if (!world.branches || !Array.isArray(world.branches)) {
        errors.push('Invalid branches structure');
      }

      // Validate version compatibility
      if (data.version && parseFloat(data.version) > 2.0) {
        warnings.push('World version may be incompatible');
      }
    }

    return {
      errors,
      warnings,
      isValid: errors.length === 0
    };

  } catch (error) {
    return {
      errors: [`Validation failed: ${error.message}`],
      warnings: [],
      isValid: false
    };
  }
}

function generateShareLink(exportData: ExportData): string {
  const encodedData = btoa(JSON.stringify(exportData));
  return `${window.location.origin}/import?data=${encodedData}`;
}

// Error recovery utilities
export async function attemptWorldRecovery(
  worldId: string,
  recoveryOptions: RecoveryOptions = {}
): Promise<{
  success: boolean;
  restoredWorld?: WorldState;
  errors: string[];
  recoveryMethod: string;
}> {
  const startTime = Date.now();
  const errors: string[] = [];

  try {
    console.log(`Attempting recovery for world: ${worldId}`);

    // Step 1: Detect corruption
    const corruption = await worldRecoveryService.detectCorruption(worldId);
    if (!corruption) {
      return {
        success: true,
        errors: ['No corruption detected'],
        recoveryMethod: 'none'
      };
    }

    // Step 2: Try to load world despite corruption
    let currentWorld: WorldState;
    try {
      currentWorld = await worldPersistenceService.loadWorld(worldId);
    } catch (loadError) {
      errors.push(`Failed to load corrupted world: ${loadError.message}`);
    }

    // Step 3: Validate current state
    if (currentWorld) {
      const validation = await worldRecoveryService.validateWorld(currentWorld);
      if (!validation.isValid) {
        errors.push(`World validation failed: ${validation.errors[0]?.message}`);
      }
    }

    // Step 4: Attempt repair
    if (corruption.severity === 'low' || corruption.severity === 'medium') {
      const repairedWorld = await worldRecoveryService.repairWorld(worldId, validation);
      return {
        success: true,
        restoredWorld: repairedWorld,
        errors,
        recoveryMethod: 'auto_repair'
      };
    }

    // Step 5: If auto repair fails, try backup restore
    const backups = await worldRecoveryService.getAvailableBackups(worldId);
    if (backups.length > 0) {
      const latestBackup = backups.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime())[0];
      const restoredWorld = await worldRecoveryService.restoreFromBackup(latestBackup.id, worldId);

      return {
        success: true,
        restoredWorld,
        errors,
        recoveryMethod: 'backup_restore'
      };
    }

    // Step 6: Final fallback
    errors.push('Unable to recover world - all methods failed');
    return {
      success: false,
      errors,
      recoveryMethod: 'failed'
    };

  } catch (error) {
    errors.push(`Recovery failed: ${error.message}`);
    return {
      success: false,
      errors,
      recoveryMethod: 'error'
    };
  } finally {
    const duration = Date.now() - startTime;
    console.log(`Recovery attempt completed in ${duration}ms`);
  }
}

// Performance monitoring
export function startPersistenceMonitoring(): {
  getMetrics: () => any;
  stop: () => void;
} {
  const metrics = {
    saveCount: 0,
    saveErrors: 0,
    compressionRatio: 0,
    syncSuccessRate: 0,
    startTime: Date.now()
  };

  let monitoring = true;

  // Monitor save operations
  const originalSave = worldPersistenceService.saveWorld;
  worldPersistenceService.saveWorld = async function(world: WorldState, options?: any) {
    if (!monitoring) {
      return originalSave.call(this, world, options);
    }

    try {
      const result = await originalSave.call(this, world, options);
      metrics.saveCount++;
      return result;
    } catch (error) {
      metrics.saveErrors++;
      throw error;
    }
  };

  return {
    getMetrics: () => ({
      ...metrics,
      uptime: Date.now() - metrics.startTime,
      errorRate: metrics.saveCount > 0 ? metrics.saveErrors / metrics.saveCount : 0
    }),
    stop: () => {
      monitoring = false;
      worldPersistenceService.saveWorld = originalSave;
    }
  };
}

// Default export
export default {
  saveWorldWithValidation,
  exportWorldForSharing,
  importWorldFromFile,
  collaborativeSave,
  generateQRCodeForWorld,
  shareWorldViaLink,
  attemptWorldRecovery,
  startPersistenceMonitoring
};