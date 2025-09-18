/**
 * World Recovery Service - Data recovery and corruption handling
 * Provides comprehensive backup, restore, and corruption recovery capabilities
 */

import { worldPersistenceService } from './indexedDB.service';
import { worldCompressionService } from './compression.service';
import type {
  WorldState,
  WorldMetadata,
  CompressionData,
  ExportData
} from '../../types/world.types';

export interface BackupOptions {
  automatic?: boolean;
  maxBackups?: number;
  compression?: boolean;
  encryption?: boolean;
  schedule?: 'hourly' | 'daily' | 'weekly' | 'manual';
  retentionPeriod?: number; // days
}

export interface RecoveryOptions {
  verifyIntegrity?: boolean;
  restoreMetadata?: boolean;
  mergeMode?: 'replace' | 'merge' | 'selective';
  backupBeforeRestore?: boolean;
  dryRun?: boolean;
}

export interface ValidationResult {
  isValid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
  repairable: boolean;
  estimatedRepairTime: number;
}

export interface ValidationError {
  code: string;
  message: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  context: {
    worldId?: string;
    elementId?: string;
    field?: string;
    expected?: any;
    actual?: any;
  };
  repairFunction?: string;
}

export interface ValidationWarning {
  code: string;
  message: string;
  recommendations: string[];
  context: any;
}

export interface CorruptionRecord {
  id: string;
  worldId: string;
  detectedAt: Date;
  type: 'partial' | 'complete' | 'metadata' | 'structural';
  severity: 'low' | 'medium' | 'high' | 'critical';
  affectedElements: string[];
  backupId?: string;
  recoveryStatus: 'pending' | 'in_progress' | 'completed' | 'failed';
  repairActions: string[];
  estimatedDataLoss: number;
}

export interface BackupMetadata {
  id: string;
  worldId: string;
  worldName: string;
  createdAt: Date;
  size: number;
  compressionRatio?: number;
  checksum: string;
  integrityStatus: 'valid' | 'corrupted' | 'unknown';
  type: 'automatic' | 'manual' | 'pre_restore' | 'pre_update';
  retentionUntil?: Date;
  metadata?: {
    worldVersion: number;
    elementCount: number;
    branchCount: number;
    userAgent: string;
    platform: string;
  };
}

class WorldRecoveryService {
  private backupSchedule: Map<string, NodeJS.Timeout> = new Map();
  private corruptionHistory: Map<string, CorruptionRecord[]> = new Map();
  private validationCache: Map<string, ValidationResult> = new Map();
  private recoveryOptions: Map<string, RecoveryOptions> = new Map();

  constructor() {
    this.initializeAutoBackup();
    this.setupRecoveryMonitoring();
  }

  /**
   * Initialize automatic backup system
   */
  private initializeAutoBackup(): void {
    console.log('Initializing automatic backup system');
  }

  /**
   * Setup recovery monitoring
   */
  private setupRecoveryMonitoring(): void {
    // Monitor for storage quota issues
    if ('storage' in navigator && 'estimate' in navigator.storage) {
      this.monitorStorageQuota();
    }

    // Monitor for IndexedDB errors
    window.addEventListener('error', (event) => {
      if (event.error?.message?.includes('IndexedDB')) {
        this.handleIndexedDBError(event.error);
      }
    });
  }

  /**
   * Create backup of world with comprehensive options
   */
  async createBackup(
    worldId: string,
    options: BackupOptions = {}
  ): Promise<BackupMetadata> {
    const startTime = Date.now();
    const backupId = `backup_${worldId}_${Date.now()}`;

    try {
      console.log(`Creating backup for world: ${worldId}`);

      const {
        automatic = false,
        maxBackups = 10,
        compression = true,
        encryption = false,
        schedule = 'manual',
        retentionPeriod = 30 // days
      } = options;

      // Load world state
      const world = await worldPersistenceService.loadWorld(worldId);

      // Validate before backup
      const validation = await this.validateWorld(world);
      if (!validation.isValid && validation.errors.some(e => e.severity === 'critical')) {
        throw new Error(`Cannot backup corrupted world: ${validation.errors[0].message}`);
      }

      // Prepare backup data
      let backupData: any = { ...world };
      let compressionRatio: number | undefined;

      if (compression) {
        const compressionResult = await worldCompressionService.compressWorld(world);
        backupData = compressionResult.data;
        compressionRatio = compressionResult.ratio;
      }

      // Calculate checksum
      const checksum = this.calculateChecksum(backupData);

      // Create backup metadata
      const backupMetadata: BackupMetadata = {
        id: backupId,
        worldId,
        worldName: world.metadata.name,
        createdAt: new Date(),
        size: new Blob([JSON.stringify(backupData)]).size,
        compressionRatio,
        checksum,
        integrityStatus: 'valid',
        type: automatic ? 'automatic' : 'manual',
        retentionUntil: new Date(Date.now() + retentionPeriod * 24 * 60 * 60 * 1000),
        metadata: {
          worldVersion: world.metadata.version,
          elementCount: world.elements.length,
          branchCount: world.branches.length,
          userAgent: navigator.userAgent,
          platform: navigator.platform
        }
      };

      // Store backup
      await this.storeBackup(backupId, backupData, backupMetadata);

      // Cleanup old backups
      await this.cleanupOldBackups(worldId, maxBackups);

      console.log(`Backup created: ${backupId} (${Date.now() - startTime}ms)`);

      return backupMetadata;

    } catch (error) {
      console.error(`Backup creation failed for world ${worldId}:`, error);
      throw new Error(`Backup creation failed: ${error.message}`);
    }
  }

  /**
   * Restore world from backup
   */
  async restoreFromBackup(
    backupId: string,
    worldId: string,
    options: RecoveryOptions = {}
  ): Promise<WorldState> {
    const startTime = Date.now();

    try {
      console.log(`Restoring world ${worldId} from backup ${backupId}`);

      const {
        verifyIntegrity = true,
        restoreMetadata = true,
        mergeMode = 'replace',
        backupBeforeRestore = true,
        dryRun = false
      } = options;

      // Get backup data
      const backupData = await this.retrieveBackup(backupId);
      const backupMetadata = await this.getBackupMetadata(backupId);

      if (!backupData || !backupMetadata) {
        throw new Error('Backup not found');
      }

      // Verify backup integrity
      if (verifyIntegrity) {
        const isValid = await this.validateBackupIntegrity(backupData, backupMetadata.checksum);
        if (!isValid) {
          throw new Error('Backup integrity check failed');
        }
      }

      // Decompress if necessary
      let worldData: WorldState;
      if (backupMetadata.compressionRatio) {
        const compressionData: CompressionData = {
          algorithm: 'auto',
          ratio: backupMetadata.compressionRatio,
          originalSize: 0,
          compressedSize: 0,
          data: backupData
        };

        const decompression = await worldCompressionService.decompressWorld(compressionData);
        worldData = decompression.data;
      } else {
        worldData = backupData as WorldState;
      }

      // Create pre-restore backup if requested
      if (backupBeforeRestore) {
        await this.createBackup(worldId, { type: 'pre_restore' });
      }

      if (dryRun) {
        console.log('Dry run completed - no changes applied');
        return worldData;
      }

      // Apply restore based on merge mode
      let finalWorld: WorldState;

      switch (mergeMode) {
        case 'replace':
          finalWorld = worldData;
          break;

        case 'merge':
          const currentWorld = await worldPersistenceService.loadWorld(worldId);
          finalWorld = this.mergeWorldsDuringRestore(currentWorld, worldData);
          break;

        case 'selective':
          finalWorld = await this.selectiveRestore(worldId, worldData);
          break;

        default:
          finalWorld = worldData;
      }

      // Restore metadata if requested
      if (restoreMetadata) {
        finalWorld.metadata = {
          ...finalWorld.metadata,
          lastModified: new Date(),
          version: finalWorld.metadata.version + 1
        };
      }

      // Save restored world
      await worldPersistenceService.saveWorld(finalWorld, { backup: false });

      // Log recovery success
      this.logRecoverySuccess(backupId, worldId, Date.now() - startTime);

      console.log(`World restored successfully: ${worldId} (${Date.now() - startTime}ms)`);

      return finalWorld;

    } catch (error) {
      console.error(`Restoration failed for world ${worldId}:`, error);
      throw new Error(`Restoration failed: ${error.message}`);
    }
  }

  /**
   * Validate world integrity and structure
   */
  async validateWorld(world: WorldState): Promise<ValidationResult> {
    const errors: ValidationError[] = [];
    const warnings: ValidationWarning[] = [];

    try {
      // Validate metadata
      this.validateMetadata(world.metadata, errors, warnings);

      // Validate elements
      await this.validateElements(world.elements, errors, warnings);

      // Validate creative DNA
      this.validateCreativeDNA(world.creativeDNA, errors, warnings);

      // Validate branches
      this.validateBranches(world.branches, errors, warnings);

      // Validate patterns
      this.validatePatterns(world.patterns, errors, warnings);

      // Validate relationships
      this.validateRelationships(world.elements, errors, warnings);

      // Validate cross-references
      this.validateCrossReferences(world, errors, warnings);

      const criticalErrors = errors.filter(e => e.severity === 'critical');
      const hasCriticalErrors = criticalErrors.length > 0;

      const result: ValidationResult = {
        isValid: !hasCriticalErrors,
        errors,
        warnings,
        repairable: !hasCriticalErrors && errors.some(e => e.repairFunction),
        estimatedRepairTime: errors.length * 100 // Rough estimate
      };

      // Cache result
      this.validationCache.set(world.metadata.id, result);

      return result;

    } catch (error) {
      console.error('World validation failed:', error);

      return {
        isValid: false,
        errors: [{
          code: 'VALIDATION_ERROR',
          message: `Validation process failed: ${error.message}`,
          severity: 'critical',
          context: {}
        }],
        warnings: [],
        repairable: false,
        estimatedRepairTime: 0
      };
    }
  }

  /**
   * Validate world metadata
   */
  private validateMetadata(metadata: WorldMetadata, errors: ValidationError[], warnings: ValidationWarning[]): void {
    if (!metadata.id) {
      errors.push({
        code: 'MISSING_WORLD_ID',
        message: 'World ID is missing',
        severity: 'critical',
        context: { field: 'metadata.id' },
        repairFunction: 'generateWorldId'
      });
    }

    if (!metadata.name || metadata.name.trim().length === 0) {
      errors.push({
        code: 'EMPTY_WORLD_NAME',
        message: 'World name is empty',
        severity: 'medium',
        context: { field: 'metadata.name' },
        repairFunction: 'generateWorldName'
      });
    }

    if (!metadata.createdAt || isNaN(metadata.createdAt.getTime())) {
      errors.push({
        code: 'INVALID_CREATED_DATE',
        message: 'Invalid creation date',
        severity: 'medium',
        context: { field: 'metadata.createdAt' },
        repairFunction: 'setCurrentDate'
      });
    }

    if (metadata.version < 1) {
      errors.push({
        code: 'INVALID_VERSION',
        message: 'World version must be positive',
        severity: 'low',
        context: { field: 'metadata.version', expected: 1, actual: metadata.version }
      });
    }
  }

  /**
   * Validate world elements
   */
  private async validateElements(elements: WorldElement[], errors: ValidationError[], warnings: ValidationWarning[]): Promise<void> {
    const elementIds = new Set<string>();

    elements.forEach((element, index) => {
      // Validate element ID
      if (!element.id) {
        errors.push({
          code: 'MISSING_ELEMENT_ID',
          message: `Element at index ${index} has no ID`,
          severity: 'critical',
          context: { elementIndex: index },
          repairFunction: 'generateElementId'
        });
      } else if (elementIds.has(element.id)) {
        errors.push({
          code: 'DUPLICATE_ELEMENT_ID',
          message: `Duplicate element ID: ${element.id}`,
          severity: 'medium',
          context: { elementId: element.id },
          repairFunction: 'generateUniqueElementId'
        });
      } else {
        elementIds.add(element.id);
      }

      // Validate element type
      if (!element.type) {
        errors.push({
          code: 'MISSING_ELEMENT_TYPE',
          message: `Element ${element.id} has no type`,
          severity: 'medium',
          context: { elementId: element.id },
          repairFunction: 'setDefaultElementType'
        });
      }

      // Validate position
      if (element.position && (isNaN(element.position.x) || isNaN(element.position.y) || isNaN(element.position.z))) {
        errors.push({
          code: 'INVALID_ELEMENT_POSITION',
          message: `Element ${element.id} has invalid position coordinates`,
          severity: 'medium',
          context: { elementId: element.id, position: element.position }
        });
      }

      // Validate metadata
      if (!element.metadata || !element.metadata.name) {
        warnings.push({
          code: 'MISSING_ELEMENT_METADATA',
          message: `Element ${element.id} has incomplete metadata`,
          recommendations: ['Add descriptive name and tags to elements for better organization'],
          context: { elementId: element.id }
        });
      }

      // Validate relationships
      element.relationships.forEach((relationship, relIndex) => {
        if (!relationship.targetId) {
          errors.push({
            code: 'INVALID_RELATIONSHIP_TARGET',
            message: `Relationship ${relIndex} in element ${element.id} has no target`,
            severity: 'medium',
            context: { elementId: element.id, relationshipIndex: relIndex }
          });
        }
      });
    });
  }

  /**
   * Validate creative DNA
   */
  private validateCreativeDNA(creativeDNA: CreativeDNA, errors: ValidationError[], warnings: ValidationWarning[]): void {
    if (!creativeDNA.patterns) {
      errors.push({
        code: 'MISSING_CREATIVE_PATTERNS',
        message: 'Creative DNA patterns array is missing',
        severity: 'low',
        context: { field: 'creativeDNA.patterns' },
        repairFunction: 'initializeCreativePatterns'
      });
    }

    if (creativeDNA.evolutionScore < 0 || creativeDNA.evolutionScore > 100) {
      errors.push({
        code: 'INVALID_EVOLUTION_SCORE',
        message: 'Evolution score must be between 0 and 100',
        severity: 'low',
        context: { field: 'creativeDNA.evolutionScore', actual: creativeDNA.evolutionScore }
      });
    }
  }

  /**
   * Validate branches
   */
  private validateBranches(branches: WorldBranch[], errors: ValidationError[], warnings: ValidationWarning[]): void {
    const branchIds = new Set<string>();

    branches.forEach((branch, index) => {
      if (!branch.id) {
        errors.push({
          code: 'MISSING_BRANCH_ID',
          message: `Branch at index ${index} has no ID`,
          severity: 'medium',
          context: { branchIndex: index },
          repairFunction: 'generateBranchId'
        });
      } else if (branchIds.has(branch.id)) {
        errors.push({
          code: 'DUPLICATE_BRANCH_ID',
          message: ` Duplicate branch ID: ${branch.id}`,
          severity: 'medium',
          context: { branchId: branch.id },
          repairFunction: 'generateUniqueBranchId'
        });
      } else {
        branchIds.add(branch.id);
      }

      // Validate active branch
      const hasActiveBranch = branches.some(br => br.isActive);
      if (index === branches.length - 1 && !hasActiveBranch) {
        errors.push({
          code: 'NO_ACTIVE_BRANCH',
          message: 'No active branch found in world',
          severity: 'high',
          context: {},
          repairFunction: 'activateFirstBranch'
        });
      }
    });
  }

  /**
   * Validate patterns
   */
  private validatePatterns(patterns: GlobalPattern[], errors: ValidationError[], warnings: ValidationWarning[]): void {
    patterns.forEach((pattern, index) => {
      if (!pattern.id) {
        errors.push({
          code: 'MISSING_PATTERN_ID',
          message: `Pattern at index ${index} has no ID`,
          severity: 'low',
          context: { patternIndex: index },
          repairFunction: 'generatePatternId'
        });
      }

      if (pattern.frequency < 0) {
        errors.push({
          code: 'INVALID_PATTERN_FREQUENCY',
          message: `Pattern ${pattern.id} has negative frequency`,
          severity: 'low',
          context: { patternId: pattern.id, frequency: pattern.frequency }
        });
      }
    });
  }

  /**
   * Validate relationships
   */
  private validateRelationships(elements: WorldElement[], errors: ValidationError[], warnings: ValidationWarning[]): void {
    const elementIds = new Set(elements.map(el => el.id));

    elements.forEach(element => {
      element.relationships.forEach(relationship => {
        if (!elementIds.has(relationship.targetId)) {
          errors.push({
            code: 'INVALID_RELATIONSHIP_TARGET_ID',
            message: `Element ${element.id} references non-existent target: ${relationship.targetId}`,
            severity: 'medium',
            context: { elementId: element.id, targetId: relationship.targetId },
            repairFunction: 'removeBrokenRelationships'
          });
        }
      });
    });
  }

  /**
   * Validate cross-references
   */
  private validateCrossReferences(world: WorldState, errors: ValidationError[], warnings: ValidationWarning[]): void {
    const elementIds = new Set(world.elements.map(el => el.id));
    const branchIds = new Set(world.branches.map(br => br.id));

    // Validate active branch references
    if (world.activeBranchId && !branchIds.has(world.activeBranchId)) {
      errors.push({
        code: 'INVALID_ACTIVE_BRANCH_ID',
        message: `Active branch ID ${world.activeBranchId} does not exist`,
        severity: 'high',
        context: { activeBranchId: world.activeBranchId },
        repairFunction: 'fixActiveBranch'
      });
    }

    // Validate branch element references
    world.branches.forEach(branch => {
      branch.elements.forEach(elementId => {
        if (!elementIds.has(elementId)) {
          errors.push({
            code: 'INVALID_BRANCH_ELEMENT_REFERENCE',
            message: `Branch ${branch.id} references non-existent element: ${elementId}`,
            severity: 'medium',
            context: { branchId: branch.id, elementId }
          });
        }
      });
    });
  }

  /**
   * Attempt to repair world based on validation results
   */
  async repairWorld(worldId: string, validationResult: ValidationResult): Promise<WorldState> {
    const world = await worldPersistenceService.loadWorld(worldId);
    const repairedWorld = { ...world };
    let hasChanges = false;

    for (const error of validationResult.errors) {
      if (error.repairFunction) {
        try {
          const repairMethod = this.getRepairMethod(error.repairFunction);
          if (repairMethod) {
            await repairMethod(repairedWorld, error.context);
            hasChanges = true;
          }
        } catch (repairError) {
          console.error(`Failed to repair error ${error.code}:`, repairError);
        }
      }
    }

    if (hasChanges) {
      repairedWorld.metadata.version += 1;
      repairedWorld.metadata.lastModified = new Date();
      await worldPersistenceService.saveWorld(repairedWorld);
    }

    return repairedWorld;
  }

  /**
   * Detect corruption in world data
   */
  async detectCorruption(worldId: string): Promise<CorruptionRecord | null> {
    try {
      const world = await worldPersistenceService.loadWorld(worldId);
      const validationResult = await this.validateWorld(world);

      if (validationResult.errors.some(e => e.severity === 'critical')) {
        const corruptionRecord: CorruptionRecord = {
          id: `corruption_${worldId}_${Date.now()}`,
          worldId,
          detectedAt: new Date(),
          type: 'structural',
          severity: 'critical',
          affectedElements: [],
          recoveryStatus: 'pending',
          repairActions: [],
          estimatedDataLoss: this.estimateDataLoss(validationResult.errors)
        };

        // Store corruption record
        const history = this.corruptionHistory.get(worldId) || [];
        history.push(corruptionRecord);
        this.corruptionHistory.set(worldId, history);

        return corruptionRecord;
      }

      return null;

    } catch (error) {
      console.error(`Corruption detection failed for world ${worldId}:`, error);

      // If we can't even load the world, it's severely corrupted
      return {
        id: `corruption_${worldId}_${Date.now()}`,
        worldId,
        detectedAt: new Date(),
        type: 'complete',
        severity: 'critical',
        affectedElements: [],
        recoveryStatus: 'pending',
        repairActions: [],
        estimatedDataLoss: 100
      };
    }
  }

  /**
   * Get corruption history for a world
   */
  getCorruptionHistory(worldId: string): CorruptionRecord[] {
    return this.corruptionHistory.get(worldId) || [];
  }

  /**
   * Get available backups for a world
   */
  async getAvailableBackups(worldId: string): Promise<BackupMetadata[]> {
    try {
      // This would query the backups store in practice
      const backups: BackupMetadata[] = [];
      return backups.filter(backup => backup.worldId === worldId);
    } catch (error) {
      console.error(`Failed to get backups for world ${worldId}:`, error);
      return [];
    }
  }

  // Private utility methods

  private async storeBackup(backupId: string, data: any, metadata: BackupMetadata): Promise<void> {
    // Implementation depends on backup storage strategy
    console.log(`Storing backup ${backupId} with metadata`, metadata);
  }

  private async retrieveBackup(backupId: string): Promise<any> {
    // Implementation depends on backup storage strategy
    console.log(`Retrieving backup ${backupId}`);
    return null;
  }

  private async getBackupMetadata(backupId: string): Promise<BackupMetadata | null> {
    // Implementation depends on backup storage strategy
    return null;
  }

  private async cleanupOldBackups(worldId: string, maxBackups: number): Promise<void> {
    const backups = await this.getAvailableBackups(worldId);
    if (backups.length <= maxBackups) return;

    // Sort by creation date and keep only the newest ones
    backups.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
    const toDelete = backups.slice(maxBackups);

    for (const backup of toDelete) {
      // Delete old backups
      console.log(`Deleting old backup: ${backup.id}`);
    }
  }

  private async validateBackupIntegrity(backupData: any, expectedChecksum: string): Promise<boolean> {
    const actualChecksum = this.calculateChecksum(backupData);
    return actualChecksum === expectedChecksum;
  }

  private calculateChecksum(data: any): string {
    // Simple checksum - in production use proper hash function
    return btoa(JSON.stringify(data));
  }

  private mergeWorldsDuringRestore(current: WorldState, backup: WorldState): WorldState {
    // Intelligent merge strategy
    const merged: WorldState = {
      ...backup,
      metadata: {
        ...backup.metadata,
        version: Math.max(current.metadata.version, backup.metadata.version) + 1,
        lastModified: new Date()
      },
      elements: this.mergeElements(current.elements, backup.elements),
      branches: this.mergeBranches(current.branches, backup.branches)
    };

    return merged;
  }

  private mergeElements(current: WorldElement[], backup: WorldElement[]): WorldElement[] {
    const currentMap = new Map(current.map(el => [el.id, el]));
    const backupMap = new Map(backup.map(el => [el.id, el]));

    const allIds = new Set([...currentMap.keys(), ...backupMap.keys()]);
    const merged: WorldElement[] = [];

    allIds.forEach(id => {
      const currentEl = currentMap.get(id);
      const backupEl = backupMap.get(id);

      // Prefer backup version for most recent changes
      if (backupEl) {
        merged.push(backupEl);
      } else if (currentEl) {
        merged.push(currentEl);
      }
    });

    return merged;
  }

  private mergeBranches(current: WorldBranch[], backup: WorldBranch[]): WorldBranch[] {
    // Simple union of branches
    const branchMap = new Map<string, WorldBranch>();
    [...current, ...backup].forEach(branch => {
      branchMap.set(branch.id, branch);
    });
    return Array.from(branchMap.values());
  }

  private async selectiveRestore(worldId: string, backupData: WorldState): Promise<WorldState> {
    const currentWorld = await worldPersistenceService.loadWorld(worldId);

    // Implementation: Allow user to select which parts to restore
    // For now, return a merged version
    return this.mergeWorldsDuringRestore(currentWorld, backupData);
  }

  private getRepairMethod(repairFunction: string): ((world: WorldState, context: any) => Promise<void>) | null {
    const repairMethods: Record<string, (world: WorldState, context: any) => Promise<void>> = {
      'generateWorldId': async (world) => {
        if (!world.metadata.id) {
          world.metadata.id = `world_${Date.now()}`;
        }
      },
      'generateElementId': async (world, context) => {
        if (context.elementIndex !== undefined) {
          world.elements[context.elementIndex].id = `element_${Date.now()}_${context.elementIndex}`;
        }
      },
      'removeBrokenRelationships': async (world, context) => {
        const element = world.elements.find(el => el.id === context.elementId);
        if (element) {
          element.relationships = element.relationships.filter(rel =>
            world.elements.some(el => el.id === rel.targetId)
          );
        }
      }
    };

    return repairMethods[repairFunction] || null;
  }

  private estimateDataLoss(errors: ValidationError[]): number {
    const criticalCount = errors.filter(e => e.severity === 'critical').length;
    const totalCount = errors.length;
    return totalCount > 0 ? (criticalCount / totalCount) * 100 : 0;
  }

  private async monitorStorageQuota(): Promise<void> {
    try {
      const estimate = await navigator.storage.estimate();
      const usagePercent = (estimate.usage || 0) / (estimate.quota || 1) * 100;

      if (usagePercent > 90) {
        console.warn(`Storage quota warning: ${usagePercent.toFixed(1)}% used`);
        // Trigger cleanup of old backups
      }
    } catch (error) {
      console.error('Failed to monitor storage quota:', error);
    }
  }

  private handleIndexedDBError(error: Error): void {
    console.error('IndexedDB error detected:', error);
    // Log corruption and attempt recovery
  }

  private logRecoverySuccess(backupId: string, worldId: string, duration: number): void {
    console.log(`Recovery success logged: ${backupId} -> ${worldId} (${duration}ms)`);
  }
}

// Export singleton instance
export const worldRecoveryService = new WorldRecoveryService();
export default WorldRecoveryService;

// Utility functions for backup management
export async function setupAutomaticBackups(worldId: string, options: BackupOptions = {}): Promise<void> {
  const recoveryService = new WorldRecoveryService();
  await worldPersistenceService.createBackup(worldId, options);
}

export async function cleanupExpiredBackups(): Promise<number> {
  // Implementation for cleaning up expired backups
  return 0;
}

export async function exportBackupForSharing(backupId: string): Promise<ExportData> {
  const recoveryService = new WorldRecoveryService();
  const backupData = await recoveryService.retrieveBackup(backupId);
  const backupMetadata = await recoveryService.getBackupMetadata(backupId);

  if (!backupData || !backupMetadata) {
    throw new Error('Backup not found');
  }

  return {
    format: 'backup',
    version: '2.0',
    worldState: backupData as WorldState,
    metadata: {
      exportedAt: backupMetadata.createdAt,
      exportedBy: 'recovery_service',
      applicationVersion: process.env.REACT_APP_VERSION || '1.0.0',
      compatibility: ['v2.0']
    },
    checksum: backupMetadata.checksum
  };
}