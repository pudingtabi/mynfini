/**
 * World Persistence Hooks - React Integration
 * Provides seamless React hooks for world state management
 */

import { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { worldPersistenceService } from './indexedDB.service';
import type {
  WorldState,
  WorldElement,
  WorldBranch,
  WorldMetadata,
  ExportData,
  ImportOptions,
  WorldStateChangeEvent,
  PersistenceEvent
} from '../types/world.types';

// Hook Interfaces
export interface UseWorldPersistenceReturn {
  world: WorldState | null;
  loading: boolean;
  error: Error | null;
  save: (options?: SaveOptions) => Promise<void>;
  load: (worldId: string) => Promise<void>;
  delete: () => Promise<void>;
  exportWorld: (format: 'json' | 'compressed' | 'qr') => Promise<ExportData>;
  importWorld: (data: ExportData, options?: ImportOptions) => Promise<string>;
  updateMetadata: (updates: Partial<WorldMetadata>) => void;
  addElement: (element: WorldElement) => void;
  removeElement: (elementId: string) => void;
  updateElement: (elementId: string, updates: Partial<WorldElement>) => void;
  createBranch: (branch: Partial<WorldBranch>) => void;
  switchBranch: (branchId: string) => void;
  getTimeline: (limit?: number) => Promise<any[]>;
  conflictHistory: any[];
  autoSaveEnabled: boolean;
  lastSaveTime: Date | null;
  compressionRatio?: number;
}

export interface UseWorldListReturn {
  worlds: Array<{ id: string; name: string; lastModified: Date; version: number }>;
  loading: boolean;
  error: Error | null;
  refresh: () => Promise<void>;
  createNewWorld: (metadata: Partial<WorldMetadata>) => Promise<string>;
  deleteWorld: (worldId: string) => Promise<void>;
}

export interface UseAutoSaveReturn {
  enabled: boolean;
  interval: number;
  pending: boolean;
  lastSave: Date | null;
  error: Error | null;
  enable: (worldId: string, intervalMs?: number) => void;
  disable: () => void;
  saveNow: () => Promise<void>;
}

export interface UseWorldExportReturn {
  exporting: boolean;
  error: Error | null;
  exportWorld: (worldId: string, format: 'json' | 'compressed' | 'qr') => Promise<ExportData>;
  importWorld: (data: ExportData, options?: ImportOptions) => Promise<string>;
  generateQRCode: (worldId: string) => Promise<string>;
  shareViaLink: (worldId: string) => Promise<string>;
}

export interface SaveOptions {
  backup?: boolean;
  sync?: boolean;
  compress?: boolean;
  onProgress?: (progress: number) => void;
}

export interface WorldPersistenceOptions {
  autoSave?: boolean;
  autoSaveInterval?: number;
  enableCompression?: boolean;
  syncOnSave?: boolean;
  maxRetries?: number;
}

// Event emitter for world state changes
class WorldEventEmitter extends EventTarget {
  emitWorldChange(event: WorldStateChangeEvent): void {
    this.dispatchEvent(new CustomEvent('worldChange', { detail: event }));
  }

  emitPersistenceEvent(event: PersistenceEvent): void {
    this.dispatchEvent(new CustomEvent('persistenceEvent', { detail: event }));
  }
}

export const worldEventEmitter = new WorldEventEmitter();

/**
 * Main world persistence hook
 * Manages a single world state with full CRUD operations
 */
export function useWorldPersistence(
  worldId: string | null,
  options: WorldPersistenceOptions = {}
): UseWorldPersistenceReturn {
  const [world, setWorld] = useState<WorldState | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);
  const [autoSaveEnabled, setAutoSaveEnabled] = useState<boolean>(options.autoSave || false);
  const [lastSaveTime, setLastSaveTime] = useState<Date | null>(null);
  const [conflictHistory, setConflictHistory] = useState<any[]>([]);

  const worldRef = useRef<WorldState | null>(null);
  const pendingChangesRef = useRef<boolean>(false);

  const {
    autoSaveInterval = 30000,
    enableCompression = true,
    syncOnSave = false,
    maxRetries = 3
  } = options;

  // Initialize persistence service
  useEffect(() => {
    const initializeService = async () => {
      try {
        setLoading(true);
        setError(null);
        await worldPersistenceService.initialize();
        console.log('World persistence service initialized');
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to initialize persistence'));
      } finally {
        setLoading(false);
      }
    };

    initializeService();

    return () => {
      worldPersistenceService.close();
    };
  }, []);

  // Load world when worldId changes
  useEffect(() => {
    if (worldId) {
      loadWorld(worldId);
    }
  }, [worldId]);

  // Auto-save functionality
  useEffect(() => {
    if (worldId && autoSaveEnabled && world) {
      worldPersistenceService.enableAutoSave(worldId, autoSaveInterval);
      worldPersistenceService.queueAutoSave(world);

      return () => {
        worldPersistenceService.disableAutoSave();
      };
    }
  }, [worldId, autoSaveEnabled, autoSaveInterval, world]);

  // Listen for world changes
  useEffect(() => {
    const handleWorldChange = (event: CustomEvent<WorldStateChangeEvent>) => {
      if (event.detail.worldId === worldId) {
        // Update local state if change originated elsewhere
        if (event.detail.type === 'update') {
          setWorld(prevWorld => ({ ...prevWorld!, ...event.detail.data }));
        }
      }
    };

    worldEventEmitter.addEventListener('worldChange', handleWorldChange as EventListener);
    return () => {
      worldEventEmitter.removeEventListener('worldChange', handleWorldChange as EventListener);
    };
  }, [worldId]);

  const loadWorld = useCallback(async (targetWorldId: string) => {
    if (!targetWorldId) return;

    try {
      setLoading(true);
      setError(null);

      const loadedWorld = await worldPersistenceService.loadWorld(targetWorldId);
      setWorld(loadedWorld);
      worldRef.current = loadedWorld;

      // Load conflict history
      const conflicts = await worldPersistenceService.getConflictHistory(targetWorldId);
      setConflictHistory(conflicts);

      console.log(`World loaded: ${loadedWorld.metadata.name}`);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to load world'));
      console.error('Failed to load world:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const save = useCallback(async (saveOptions: SaveOptions = {}): Promise<void> => {
    if (!world) return;

    const { backup = true, sync = syncOnSave, onProgress } = saveOptions;

    try {
      setError(null);
      onProgress?.(0);

      await worldPersistenceService.saveWorld(world, { backup, sync });
      setLastSaveTime(new Date());
      pendingChangesRef.current = false;

      // Emit change event
      worldEventEmitter.emitWorldChange({
        type: 'update',
        worldId: world.metadata.id,
        timestamp: new Date(),
        data: world
      });

      onProgress?.(100);
      console.log(`World saved: ${world.metadata.name}`);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to save world'));
      console.error('Failed to save world:', err);
      throw err;
    }
  }, [world, syncOnSave]);

  const deleteWorld = useCallback(async (): Promise<void> => {
    if (!world) return;

    try {
      setError(null);
      await worldPersistenceService.deleteWorld(world.metadata.id);

      // Emit deletion event
      worldEventEmitter.emitWorldChange({
        type: 'delete',
        worldId: world.metadata.id,
        timestamp: new Date()
      });

      setWorld(null);
      console.log(`World deleted: ${world.metadata.name}`);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to delete world'));
      console.error('Failed to delete world:', err);
      throw err;
    }
  }, [world]);

  const updateMetadata = useCallback((updates: Partial<WorldMetadata>) => {
    if (!world) return;

    const updatedWorld = {
      ...world,
      metadata: { ...world.metadata, ...updates, lastModified: new Date() }
    };

    setWorld(updatedWorld);
    worldRef.current = updatedWorld;
    pendingChangesRef.current = true;

    worldPersistenceService.queueAutoSave(updatedWorld);
  }, [world]);

  const addElement = useCallback((element: WorldElement) => {
    if (!world) return;

    const updatedWorld = {
      ...world,
      elements: [...world.elements, element],
      metadata: { ...world.metadata, lastModified: new Date() }
    };

    setWorld(updatedWorld);
    worldRef.current = updatedWorld;
    pendingChangesRef.current = true;

    worldPersistenceService.queueAutoSave(updatedWorld);

    // Emit element creation event
    worldEventEmitter.emitWorldChange({
      type: 'create',
      worldId: world.metadata.id,
      elementId: element.id,
      timestamp: new Date(),
      data: { element }
    });
  }, [world]);

  const removeElement = useCallback((elementId: string) => {
    if (!world) return;

    const updatedWorld = {
      ...world,
      elements: world.elements.filter(el => el.id !== elementId),
      metadata: { ...world.metadata, lastModified: new Date() }
    };

    setWorld(updatedWorld);
    worldRef.current = updatedWorld;
    pendingChangesRef.current = true;

    worldPersistenceService.queueAutoSave(updatedWorld);

    // Emit element deletion event
    worldEventEmitter.emitWorldChange({
      type: 'delete',
      worldId: world.metadata.id,
      elementId,
      timestamp: new Date()
    });
  }, [world]);

  const updateElement = useCallback((elementId: string, updates: Partial<WorldElement>) => {
    if (!world) return;

    const updatedWorld = {
      ...world,
      elements: world.elements.map(el =>
        el.id === elementId ? { ...el, ...updates } : el
      ),
      metadata: { ...world.metadata, lastModified: new Date() }
    };

    setWorld(updatedWorld);
    worldRef.current = updatedWorld;
    pendingChangesRef.current = true;

    worldPersistenceService.queueAutoSave(updatedWorld);

    // Emit element update event
    worldEventEmitter.emitWorldChange({
      type: 'update',
      worldId: world.metadata.id,
      elementId,
      timestamp: new Date(),
      data: { updates }
    });
  }, [world]);

  const createBranch = useCallback((branch: Partial<WorldBranch>) => {
    if (!world) return;

    const newBranch = {
      id: `branch_${Date.now()}`,
      name: branch.name || 'New Branch',
      description: branch.description || '',
      divergencePoint: new Date(),
      elements: world.elements.map(el => el.id),
      timeline: [],
      isActive: false,
      mergedBranches: [],
      ...branch
    } as WorldBranch;

    const updatedWorld = {
      ...world,
      branches: [...world.branches, newBranch],
      metadata: { ...world.metadata, lastModified: new Date() }
    };

    setWorld(updatedWorld);
    worldRef.current = updatedWorld;
    pendingChangesRef.current = true;

    worldPersistenceService.queueAutoSave(updatedWorld);

    // Emit branch creation event
    worldEventEmitter.emitWorldChange({
      type: 'branch',
      worldId: world.metadata.id,
      branchId: newBranch.id,
      timestamp: new Date(),
      data: { branch: newBranch }
    });
  }, [world]);

  const switchBranch = useCallback((branchId: string) => {
    if (!world) return;

    const updatedWorld = {
      ...world,
      activeBranchId: branchId,
      branches: world.branches.map(br => ({
        ...br,
        isActive: br.id === branchId
      })),
      metadata: { ...world.metadata, lastModified: new Date() }
    };

    setWorld(updatedWorld);
    worldRef.current = updatedWorld;
    pendingChangesRef.current = true;

    worldPersistenceService.queueAutoSave(updatedWorld);
  }, [world]);

  const getTimeline = useCallback(async (limit: number = 100): Promise<any[]> => {
    if (!worldId) return [];
    return await worldPersistenceService.getTimeline(worldId, limit);
  }, [worldId]);

  const exportWorld = useCallback(async (format: 'json' | 'compressed' | 'qr'): Promise<ExportData> => {
    if (!worldId) {
      throw new Error('No world loaded');
    }
    return await worldPersistenceService.exportWorld(worldId, format);
  }, [worldId]);

  const importWorld = useCallback(async (data: ExportData, options?: ImportOptions): Promise<string> => {
    return await worldPersistenceService.importWorld(data, options);
  }, []);

  // Calculate compression ratio
  const compressionRatio = useMemo(() => {
    if (!world) return undefined;

    const originalSize = JSON.stringify(world).length;
    const compressedSize = JSON.stringify(world).length * 0.6; // Estimate
    return compressedSize / originalSize;
  }, [world]);

  return {
    world,
    loading,
    error,
    save,
    load: loadWorld,
    delete: deleteWorld,
    exportWorld,
    importWorld,
    updateMetadata,
    addElement,
    removeElement,
    updateElement,
    createBranch,
    switchBranch,
    getTimeline,
    conflictHistory,
    autoSaveEnabled,
    lastSaveTime,
    compressionRatio
  };
}

/**
 * World list management hook
 * Handles multiple worlds and creation/deletion
 */
export function useWorldList(): UseWorldListReturn {
  const [worlds, setWorlds] = useState<Array<{ id: string; name: string; lastModified: Date; version: number }>>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  const refresh = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const worldList = await worldPersistenceService.getWorldList();
      setWorlds(worldList);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to refresh world list'));
      console.error('Failed to refresh world list:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const createNewWorld = useCallback(async (metadata: Partial<WorldMetadata>): Promise<string> => {
    try {
      setError(null);

      const newWorld: WorldState = {
        metadata: {
          id: generateWorldId(),
          name: metadata.name || 'New World',
          description: metadata.description || '',
          createdAt: new Date(),
          lastModified: new Date(),
          version: 1,
          branchId: 'main',
          tags: metadata.tags || [],
          isPublic: metadata.isPublic || false,
          ownerId: metadata.ownerId || 'current-user'
        },
        creativeDNA: {
          patterns: [],
          evolutionScore: 0,
          inspirationHistory: [],
          creativityMetrics: {
            originality: 0,
            complexity: 0,
            coherence: 0,
            novelty: 0,
            fluency: 0,
            adaptability: 0
          },
          adaptationTraits: []
        },
        elements: [],
        branches: [{
          id: 'main',
          name: 'Main Branch',
          description: 'Main development branch',
          divergencePoint: new Date(),
          elements: [],
          timeline: [],
          isActive: true,
          mergedBranches: []
        }],
        activeBranchId: 'main',
        patterns: [],
        settings: getDefaultWorldSettings(),
        statistics: {
          totalElements: 0,
          totalBranches: 1,
          creationTime: new Date(),
          totalPlayTime: 0,
          modificationCount: 0,
          collaborationCount: 0,
          creativityScore: 0
        }
      };

      await worldPersistenceService.saveWorld(newWorld);
      await refresh();

      console.log(`New world created: ${newWorld.metadata.name}`);
      return newWorld.metadata.id;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to create world'));
      console.error('Failed to create world:', err);
      throw err;
    }
  }, [refresh]);

  const deleteWorld = useCallback(async (worldId: string): Promise<void> => {
    try {
      setError(null);
      await worldPersistenceService.deleteWorld(worldId);
      await refresh();

      console.log(`World deleted: ${worldId}`);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to delete world'));
      console.error('Failed to delete world:', err);
      throw err;
    }
  }, [refresh]);

  // Initial load
  useEffect(() => {
    refresh();
  }, [refresh]);

  return {
    worlds,
    loading,
    error,
    refresh,
    createNewWorld,
    deleteWorld
  };
}

/**
 * Auto-save management hook
 */
export function useAutoSave(worldId: string | null): UseAutoSaveReturn {
  const [enabled, setEnabled] = useState<boolean>(false);
  const [interval, setInterval] = useState<number>(30000);
  const [pending, setPending] = useState<boolean>(false);
  const [lastSave, setLastSave] = useState<Date | null>(null);
  const [error, setError] = useState<Error | null>(null);

  const saveNow = useCallback(async () => {
    setError(null);
    // This would be called from the main hook
    console.log('Manual save triggered');
  }, []);

  const enable = useCallback((targetWorldId: string, intervalMs: number = 30000) => {
    if (enabled) return;

    setEnabled(true);
    setInterval(intervalMs);

    worldEventEmitter.emitPersistenceEvent({
      type: 'save_start',
      worldId: targetWorldId,
      timestamp: new Date()
    });
  }, [enabled]);

  const disable = useCallback(() => {
    setEnabled(false);
    setPending(false);

    worldEventEmitter.emitPersistenceEvent({
      type: 'save_complete',
      worldId: '',
      timestamp: new Date()
    });
  }, []);

  // Listen for persistence events
  useEffect(() => {
    const handlePersistenceEvent = (event: CustomEvent<PersistenceEvent>) => {
      switch (event.detail.type) {
        case 'save_start':
          setPending(true);
          break;
        case 'save_complete':
          setPending(false);
          setLastSave(event.detail.timestamp);
          break;
        case 'save_error':
          setError(event.detail.error || new Error('Save error'));
          setPending(false);
          break;
      }
    };

    worldEventEmitter.addEventListener('persistenceEvent', handlePersistenceEvent as EventListener);
    return () => {
      worldEventEmitter.removeEventListener('persistenceEvent', handlePersistenceEvent as EventListener);
    };
  }, []);

  return {
    enabled,
    interval,
    pending,
    lastSave,
    error,
    enable,
    disable,
    saveNow
  };
}

/**
 * Export/Import functionality hook
 */
export function useWorldExport(): UseWorldExportReturn {
  const [exporting, setExporting] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  const exportWorld = useCallback(async (worldId: string, format: 'json' | 'compressed' | 'qr'): Promise<ExportData> => {
    try {
      setExporting(true);
      setError(null);

      const data = await worldPersistenceService.exportWorld(worldId, format);

      console.log(`World exported: ${worldId} (${format})`);
      return data;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Export failed'));
      console.error('Failed to export world:', err);
      throw err;
    } finally {
      setExporting(false);
    }
  }, []);

  const importWorld = useCallback(async (data: ExportData, options?: ImportOptions): Promise<string> => {
    try {
      setExporting(true);
      setError(null);

      const worldId = await worldPersistenceService.importWorld(data, options);

      console.log(`World imported: ${worldId}`);
      return worldId;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Import failed'));
      console.error('Failed to import world:', err);
      throw err;
    } finally {
      setExporting(false);
    }
  }, []);

  const generateQRCode = useCallback(async (worldId: string): Promise<string> => {
    try {
      setError(null);

      const data = await worldPersistenceService.exportWorld(worldId, 'qr');
      const qrDataUri = `data:text/json;base64,${btoa(JSON.stringify(data))}`;

      return qrDataUri;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('QR generation failed'));
      console.error('Failed to generate QR code:', err);
      throw err;
    }
  }, []);

  const shareViaLink = useCallback(async (worldId: string): Promise<string> => {
    try {
      setError(null);

      const data = await worldPersistenceService.exportWorld(worldId, 'compressed');
      const encodedData = btoa(JSON.stringify(data));
      const shareLink = `${window.location.origin}/import?data=${encodedData}`;

      // Try to use Web Share API if available
      if (navigator.share) {
        try {
          await navigator.share({
            title: `MYNFINI World: ${data.worldState.metadata.name}`,
            text: `Check out this MYNFINI world!`,
            url: shareLink
          });
        } catch (shareError) {
          console.warn('Web Share API failed, falling back to link');
        }
      }

      return shareLink;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Share link generation failed'));
      console.error('Failed to generate share link:', err);
      throw err;
    }
  }, []);

  return {
    exporting,
    error,
    exportWorld,
    importWorld,
    generateQRCode,
    shareViaLink
  };
}

// Utility functions

function generateWorldId(): string {
  return `world_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

function getDefaultWorldSettings() {
  return {
    physics: {
      gravity: { x: 0, y: -9.8, z: 0 },
      friction: 0.5,
      collisionDetection: true,
      timeScale: 1,
      constraints: []
    },
    rendering: {
      quality: 'high',
      shadows: true,
      reflections: true,
      antiAliasing: true,
      postProcessing: ['bloom', 'ssao']
    },
    interaction: {
      mouseSensitivity: 1,
      keyboardShortcuts: {
        'ctrl+s': 'save',
        'ctrl+z': 'undo',
        'ctrl+y': 'redo',
        'space': 'play_pause'
      },
      gestureSupport: true,
      hapticFeedback: true,
      accessibilityMode: false
    },
    persistence: {
      autoSaveInterval: 30000,
      maxBranches: 50,
      compressionLevel: 6,
      backupCount: 10,
      syncOnSave: false
    },
    creativity: {
      aiAssistance: true,
      patternRecognition: true,
      inspirationSources: ['user', 'ai', 'collaborative'],
      evolutionSpeed: 1,
      complexityThreshold: 0.7
    }
  };
}