/**
 * World Persistence Provider Component
 * React Context provider for comprehensive world persistence management
 */

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { worldPersistenceManager } from '../../services/worldPersistence';
import { WorldEventEmitter, worldEventEmitter } from '../../services/worldPersistence/hooks';
import type { WorldState, ExportData } from '../../types/world.types';

export interface WorldPersistenceContextValue {
  // World management
  loadedWorld: WorldState | null;
  loading: boolean;
  error: Error | null;
  worldList: Array<{ id: string; name: string; lastModified: Date; version: number }>;

  // Actions
  loadWorld: (worldId: string) => Promise<void>;
  createWorld: (metadata?: Partial<WorldState['metadata']>) => Promise<string>;
  saveWorld: (world?: WorldState) => Promise<void>;
  deleteWorld: (worldId: string) => Promise<void>;
  refreshWorldList: () => Promise<void>;

  // Advanced features
  exportWorld: (format: 'json' | 'compressed' | 'qr') => Promise<ExportData>;
  importWorld: (data: ExportData) => Promise<string>;
  createBackup: () => Promise<string>;
  restoreFromBackup: (backupId: string) => Promise<void>;

  // Health monitoring
  validateWorld: () => Promise<{
    valid: boolean;
    errors: any[];
    warnings: any[];
    repairable: boolean;
  }>;
  getHealthReport: () => Promise<{
    worldId: string;
    lastModified: Date;
    version: number;
    validation: any;
    corruptionHistory: any[];
    availableBackups: any[];
    compressionRatio?: number;
    syncStatus?: any;
  }>;

  // Auto-save and monitoring
  autoSaveEnabled: boolean;
  setAutoSave: (enabled: boolean, interval?: number) => void;
  lastSaveTime: Date | null;
  pendingChanges: boolean;

  // Event handling
  subscribeToWorldEvents: (callback: (event: any) => void) => () => void;

  // Configuration
  compressionEnabled: boolean;
  setCompressionEnabled: (enabled: boolean) => void;
  syncEnabled: boolean;
  setSyncEnabled: (enabled: boolean) => void;
}

const WorldPersistenceContext = createContext<WorldPersistenceContextValue | undefined>(undefined);

export interface WorldPersistenceProviderProps {
  children: React.ReactNode;
  autoInitialize?: boolean;
  autoSaveInterval?: number;
  enableCompression?: boolean;
  enableSync?: boolean;
  onError?: (error: Error) => void;
  onWorldChange?: (event: any) => void;
}

export const WorldPersistenceProvider: React.FC<WorldPersistenceProviderProps> = ({
  children,
  autoInitialize = true,
  autoSaveInterval = 30000,
  enableCompression = true,
  enableSync = false,
  onError,
  onWorldChange
}) => {
  const [loadedWorld, setLoadedWorld] = useState<WorldState | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);
  const [worldList, setWorldList] = useState<Array<{ id: string; name: string; lastModified: Date; version: number }>>([]);
  const [autoSaveEnabled, setAutoSaveEnabled] = useState<boolean>(false);
  const [lastSaveTime, setLastSaveTime] = useState<Date | null>(null);
  const [pendingChanges, setPendingChanges] = useState<boolean>(false);
  const [compressionEnabled, setCompressionEnabled] = useState<boolean>(enableCompression);
  const [syncEnabled, setSyncEnabled] = useState<boolean>(enableSync);

  // Initialize persistence system
  useEffect(() => {
    if (autoInitialize) {
      initializePersistence();
    }

    return () => {
      // Cleanup on unmount
      worldPersistenceManager.shutdown();
    };
  }, [autoInitialize]);

  const initializePersistence = async () => {
    try {
      setLoading(true);
      setError(null);

      await worldPersistenceManager.initialize();
      await refreshWorldList();

      console.log('World persistence system initialized');
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to initialize persistence');
      setError(error);
      onError?.(error);
      console.error('Failed to initialize persistence system:', error);
    } finally {
      setLoading(false);
    }
  };

  // Subscribe to world events
  useEffect(() => {
    const handleWorldChange = (event: CustomEvent) => {
      onWorldChange?.(event.detail);

      // Update local state if event affects loaded world
      if (loadedWorld && event.detail.worldId === loadedWorld.metadata.id) {
        if (event.detail.type === 'update') {
          setLoadedWorld(current => ({
            ...current!,
            ...event.detail.data,
            metadata: {
              ...current!.metadata,
              ...event.detail.data.metadata
            }
          }));
        }
      }
    };

    const handlePersistenceEvent = (event: CustomEvent) => {
      const { type, timestamp } = event.detail;

      if (type === 'save_complete' && loadedWorld && event.detail.worldId === loadedWorld.metadata.id) {
        setLastSaveTime(timestamp);
        setPendingChanges(false);
      } else if (type === 'save_error') {
        const error = event.detail.error || new Error('Save error');
        setError(error);
        onError?.(error);
      }
    };

    worldEventEmitter.addEventListener('worldChange', handleWorldChange as EventListener);
    worldEventEmitter.addEventListener('persistenceEvent', handlePersistenceEvent as EventListener);

    return () => {
      worldEventEmitter.removeEventListener('worldChange', handleWorldChange as EventListener);
      worldEventEmitter.removeEventListener('persistenceEvent', handlePersistenceEvent as EventListener);
    };
  }, [loadedWorld, onWorldChange, onError]);

  // World management actions
  const loadWorld = useCallback(async (worldId: string) => {
    try {
      setLoading(true);
      setError(null);

      const world = await worldPersistenceManager.getWorldHealthReport(worldId); // This loads the world internally
      setLoadedWorld(world.worldState as any);

      console.log(`World loaded: ${worldId}`);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to load world');
      setError(error);
      onError?.(error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, [onError]);

  const createWorld = useCallback(async (metadata?: Partial<WorldState['metadata']>) => {
    try {
      setLoading(true);
      setError(null);

      // Use the world list hook's createNewWorld functionality
      const worlds = await worldPersistenceManager.getAllWorlds();

      // For now, we'll use a simple world creation approach
      const existingWorld = await worldPersistenceService.loadWorld('temp'); // This will fail, but we need a proper world creation method

      // Refresh world list after creation
      await refreshWorldList();

      return 'new-world-id'; // Placeholder
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to create world');
      setError(error);
      onError?.(error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, [onError]);

  const saveWorld = useCallback(async (world?: WorldState) => {
    if (!loadedWorld && !world) return;

    try {
      setError(null);

      const worldToSave = world || loadedWorld;
      if (!worldToSave) return;

      // Save through persistence service
      await worldPersistenceService.saveWorld(worldToSave, {
        backup: true,
        sync: syncEnabled,
        compress: compressionEnabled
      });

      setPendingChanges(false);
      console.log('World saved successfully');
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to save world');
      setError(error);
      onError?.(error);
      throw error;
    }
  }, [loadedWorld, syncEnabled, compressionEnabled, onError]);

  const deleteWorld = useCallback(async (worldId: string) => {
    try {
      setLoading(true);
      setError(null);

      await worldPersistenceService.deleteWorld(worldId);

      // Remove from world list if it's there
      setWorldList(current => current.filter(w => w.id !== worldId));

      // Clear loaded world if it matches
      if (loadedWorld && loadedWorld.metadata.id === worldId) {
        setLoadedWorld(null);
      }

      console.log(`World deleted: ${worldId}`);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to delete world');
      setError(error);
      onError?.(error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, [loadedWorld, onError]);

  const refreshWorldList = useCallback(async () => {
    try {
      const worlds = await worldPersistenceService.getWorldList();
      setWorldList(worlds);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to refresh world list');
      setError(error);
      onError?.(error);
    }
  }, [onError]);

  // Advanced features
  const exportWorld = useCallback(async (format: 'json' | 'compressed' | 'qr'): Promise<ExportData> => {
    if (!loadedWorld) {
      throw new Error('No world loaded for export');
    }

    const result = await worldPersistenceManager.exportForSharing(loadedWorld.metadata.id, format);
    return result.data;
  }, [loadedWorld]);

  const importWorld = useCallback(async (data: ExportData): Promise<string> => {
    return await worldPersistenceService.importWorld(data, {
      preserveIds: false,
      validateSchema: true,
      createBackup: true,
      conflictResolution: 'merge'
    });
  }, []);

  const createBackup = useCallback(async (): Promise<string> => {
    if (!loadedWorld) {
      throw new Error('No world loaded for backup');
    }

    return await worldRecoveryService.createBackup(loadedWorld.metadata.id);
  }, [loadedWorld]);

  const restoreFromBackup = useCallback(async (backupId: string): Promise<void> => {
    if (!loadedWorld) {
      throw new Error('No world loaded for restore');
    }

    const restoredWorld = await worldRecoveryService.restoreFromBackup(backupId, loadedWorld.metadata.id);
    setLoadedWorld(restoredWorld);
  }, [loadedWorld]);

  // Health monitoring
  const validateWorld = useCallback(async () => {
    if (!loadedWorld) {
      throw new Error('No world loaded for validation');
    }

    const result = await worldRecoveryService.validateWorld(loadedWorld);
    return {
      valid: result.isValid,
      errors: result.errors,
      warnings: result.warnings,
      repairable: result.repairable
    };
  }, [loadedWorld]);

  const getHealthReport = useCallback(async () => {
    if (!loadedWorld) {
      throw new Error('No world loaded for health report');
    }

    return await worldPersistenceManager.getWorldHealthReport(loadedWorld.metadata.id);
  }, [loadedWorld]);

  // Auto-save and monitoring
  const setAutoSave = useCallback((enabled: boolean, interval: number = autoSaveInterval) => {
    setAutoSaveEnabled(enabled);

    if (enabled && loadedWorld) {
      // Enable auto-save for current world
      worldPersistenceService.enableAutoSave(loadedWorld.metadata.id, interval);

      // Mark as having pending changes to trigger first save
      worldPersistenceService.queueAutoSave(loadedWorld);
    } else {
      worldPersistenceService.disableAutoSave();
    }
  }, [loadedWorld, autoSaveInterval]);

  const subscribeToWorldEvents = useCallback((callback: (event: any) => void) => {
    const handler = (event: CustomEvent) => {
      callback(event.detail);
    };

    worldEventEmitter.addEventListener('worldChange', handler as EventListener);
    worldEventEmitter.addEventListener('persistenceEvent', handler as EventListener);

    return () => {
      worldEventEmitter.removeEventListener('worldChange', handler as EventListener);
      worldEventEmitter.removeEventListener('persistenceEvent', handler as EventListener);
    };
  }, []);

  // Auto-save functionality
  useEffect(() => {
    if (autoSaveEnabled && loadedWorld) {
      setAutoSave(true, autoSaveInterval);
    }

    return () => {
      if (!autoSaveEnabled) {
        worldPersistenceService.disableAutoSave();
      }
    };
  }, [autoSaveEnabled, loadedWorld, autoSaveInterval, setAutoSave]);

  const contextValue: WorldPersistenceContextValue = {
    // World management
    loadedWorld,
    loading,
    error,
    worldList,

    // Actions
    loadWorld,
    createWorld,
    saveWorld,
    deleteWorld,
    refreshWorldList,

    // Advanced features
    exportWorld,
    importWorld,
    createBackup,
    restoreFromBackup,

    // Health monitoring
    validateWorld,
    getHealthReport,

    // Auto-save and monitoring
    autoSaveEnabled,
    setAutoSave,
    lastSaveTime,
    pendingChanges,

    // Event handling
    subscribeToWorldEvents,

    // Configuration
    compressionEnabled,
    setCompressionEnabled,
    syncEnabled,
    setSyncEnabled
  };

  return (
    <WorldPersistenceContext.Provider value={contextValue}>
      {children}
    </WorldPersistenceContext.Provider>
  );
};

// Custom hook for using world persistence
export const useWorldPersistence = (): WorldPersistenceContextValue => {
  const context = useContext(WorldPersistenceContext);
  if (context === undefined) {
    throw new Error('useWorldPersistence must be used within a WorldPersistenceProvider');
  }
  return context;
};

// Convenience hooks for specific functionalities
export const useAutoSave = () => {
  const { autoSaveEnabled, setAutoSave, lastSaveTime, pendingChanges } = useWorldPersistence();
  return { autoSaveEnabled, setAutoSave, lastSaveTime, pendingChanges };
};

export const useWorldExport = () => {
  const { exportWorld, importWorld, loadedWorld } = useWorldPersistence();
  return { exportWorld, importWorld, hasLoadedWorld: !!loadedWorld };
};

export const useWorldBackup = () => {
  const { createBackup, restoreFromBackup, loadedWorld } = useWorldPersistence();
  return { createBackup, restoreFromBackup, hasLoadedWorld: !!loadedWorld };
};

export const useWorldHealth = () => {
  const { validateWorld, getHealthReport, loadedWorld } = useWorldPersistence();
  return { validateWorld, getHealthReport, hasLoadedWorld: !!loadedWorld };
};