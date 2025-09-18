/**
 * World Compression Service Tests
 * Tests for advanced compression strategies
 */

import { worldCompressionService, CompressionStrategy, COMPRESSION_PRESETS } from '../compression.service';
import type { WorldState, WorldElement } from '../../../types/world.types';

// Test data generator
function generateTestWorld(size: 'small' | 'medium' | 'large' = 'small'): WorldState {
  const baseElements: WorldElement[] = [
    {
      id: 'element-1',
      type: 'geometry',
      position: { x: 0, y: 0, z: 0 },
      properties: { visual: { color: '#ff0000', opacity: 1 } },
      relationships: [],
      metadata: {
        name: 'Test Element 1',
        description: 'First test element',
        tags: ['test'],
        createdAt: new Date(),
        lastModified: new Date(),
        authorId: 'test-user',
        version: 1
      }
    }
  ];

  const elementCount = size === 'small' ? 10 : size === 'medium' ? 100 : 1000;
  const elements: WorldElement[] = [...baseElements];

  for (let i = 2; i <= elementCount; i++) {
    elements.push({
      id: `element-${i}`,
      type: i % 3 === 0 ? 'geometry' : i % 3 === 1 ? 'text' : 'light',
      position: { x: i * 10, y: i * 5, z: i * 2 },
      properties: {
        visual: {
          color: `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`,
          opacity: Math.random()
        }
      },
      relationships: i > 2 ? [{ targetId: `element-${i-1}`, type: 'connection', strength: 0.5, bidirectional: true, metadata: {} }] : [],
      metadata: {
        name: `Test Element ${i}`,
        description: `Element number ${i} with detailed description containing multiple words and metadata`,
        tags: ['test', `element-${i}`, 'compression-test'],
        createdAt: new Date(Date.now() - i * 1000),
        lastModified: new Date(Date.now() - i * 500),
        authorId: 'test-user',
        version: Math.floor(Math.random() * 10) + 1
      }
    });
  }

  return {
    metadata: {
      id: `test-world-compression-${size}-${Date.now()}`,
      name: `Compression Test World - ${size}`,
      description: `A ${size} world for testing compression algorithms with ${elementCount} elements`,
      createdAt: new Date(),
      lastModified: new Date(),
      version: 1,
      branchId: 'main',
      tags: ['test', 'compression', size],
      thumbnail: '',
      isPublic: false,
      ownerId: 'test-user'
    },
    creativeDNA: {
      patterns: Array.from({ length: size === 'small' ? 5 : size === 'medium' ? 25 : 100 }, (_, i) => ({
        id: `pattern-${i}`,
        type: 'geometric',
        frequency: Math.random() * 50 + 1,
        confidence: Math.random(),
        context: { source: `test-source-${i}` },
        timestamp: new Date(Date.now() - i * 3600000),
        source: 'system'
      })),
      evolutionScore: Math.random() * 100,
      inspirationHistory: Array.from({ length: 10 }, (_, i) => ({
        id: `inspiration-${i}`,
        source: 'test-source',
        type: 'visual',
        content: `Inspiration content ${i} with detailed description`,
        impact: Math.random() * 10,
        timestamp: new Date(Date.now() - i * 7200000),
        context: { test: true }
      })),
      creativityMetrics: {
        originality: Math.random() * 100,
        complexity: Math.random() * 100,
        coherence: Math.random() * 100,
        novelty: Math.random() * 100,
        fluency: Math.random() * 100,
        adaptability: Math.random() * 100
      },
      adaptationTraits: []
    },
    elements,
    branches: [
      {
        id: 'main',
        name: 'Main Branch',
        description: 'Main development branch',
        divergencePoint: new Date(),
        elements: elements.map(el => el.id),
        timeline: Array.from({ length: 5 }, (_, i) => ({
          id: `timeline-${i}`,
          type: 'creation',
          timestamp: new Date(Date.now() - i * 60000),
          action: 'element_created',
          parameters: { elementId: `element-${i + 1}` },
          preState: {},
          postState: {}
        })),
        isActive: true,
        mergedBranches: []
      }
    ],
    activeBranchId: 'main',
    patterns: [],
    settings: {
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
        postProcessing: ['bloom', 'ssao', 'depthOfField']
      },
      interaction: {
        mouseSensitivity: 1.2,
        keyboardShortcuts: {
          'ctrl+s': 'save',
          'ctrl+z': 'undo',
          'ctrl+y': 'redo',
          'space': 'play_pause',
          'shift+e': 'export'
        },
        gestureSupport: true,
        hapticFeedback: true,
        accessibilityMode: false
      },
      persistence: {
        autoSaveInterval: 30000,
        maxBranches: 100,
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
    },
    statistics: {
      totalElements: elements.length,
      totalBranches: 1,
      creationTime: new Date(),
      totalPlayTime: 0,
      modificationCount: 0,
      collaborationCount: 0,
      creativityScore: Math.random() * 100
    }
  };
}

describe('WorldCompressionService', () => {
  let testWorld: WorldState;
  let originalSize: number;

  beforeEach(() => {
    testWorld = generateTestWorld('small');
    originalSize = new Blob([JSON.stringify(testWorld)]).size;
  });

  describe('Basic Compression', () => {
    test('should compress world data successfully', async () => {
      const result = await worldCompressionService.compressWorld(testWorld);

      expect(result).toBeDefined();
      expect(result.algorithm).toBeDefined();
      expect(result.originalSize).toBe(originalSize);
      expect(result.compressedSize).toBeLessThan(result.originalSize);
      expect(result.ratio).toBeLessThan(1);
      expect(result.ratio).toBeGreaterThan(0);
      expect(result.duration).toBeGreaterThan(0);
      expect(result.data).toBeDefined();
      expect(result.metadata).toBeDefined();
    });

    test('should decompress data correctly', async () => {
      const compressed = await worldCompressionService.compressWorld(testWorld);
      const decompressed = await worldCompressionService.decompressWorld({
        algorithm: compressed.algorithm,
        originalSize: compressed.originalSize,
        compressedSize: compressed.compressedSize,
        ratio: compressed.ratio,
        data: compressed.data
      } as any);

      expect(decompressed).toBeDefined();
      expect(decompressed.data).toBeDefined();
      expect(decompressed.data.metadata.id).toBe(testWorld.metadata.id);
      expect(decompressed.data.elements.length).toBe(testWorld.elements.length);
      expect(decompressed.duration).toBeGreaterThan(0);
    });

    test('should skip compression for small data', async () => {
      const tinyWorld = generateTestWorld('small');
      tinyWorld.elements = []; // Make it really small

      const result = await worldCompressionService.compressWorld(tinyWorld, { threshold: 1024 * 100 });

      expect(result.algorithm).toBe('none');
      expect(result.originalSize).toBe(result.compressedSize);
      expect(result.ratio).toBe(1);
    });
  });

  describe('Compression Strategies', () => {
    test('should handle LZ-string compression', async () => {
      const result = await worldCompressionService.compressWorld(testWorld, {
        strategy: CompressionStrategy.LZ_STRING
      });

      expect(result.algorithm).toBe(CompressionStrategy.LZ_STRING);
      expect(result.compressedSize).toBeLessThan(result.originalSize);
      expect(result.ratio).toBeLessThan(1);
    });

    test('should handle GZIP compression', async () => {
      const result = await worldCompressionService.compressWorld(testWorld, {
        strategy: CompressionStrategy.GZIP,
        level: 6
      });

      expect(result.algorithm).toBe(CompressionStrategy.GZIP);
      expect(result.metadata?.level).toBe(6);
      expect(result.compressedSize).toBeLessThan(result.originalSize);
    });

    test('should handle hybrid compression', async () => {
      const result = await worldCompressionService.compressWorld(testWorld, {
        strategy: CompressionStrategy.HYBRID
      });

      expect(result.algorithm).toBeDefined();
      expect(['lz-string', 'gzip', 'custom-delta', 'hybrid']).toContain(result.algorithm);
      expect(result.compressedSize).toBeLessThan(result.originalSize);
    });
  });

  describe('Performance Benchmarking', () => {
    test('should benchmark multiple compression strategies', async () => {
      const strategies = [CompressionStrategy.LZ_STRING, CompressionStrategy.GZIP, CompressionStrategy.HYBRID];
      const results = await worldCompressionService.benchmarkStrategies(testWorld, strategies);

      expect(results).toBeDefined();
      expect(results.length).toBe(strategies.length);
      expect(results[0].strategy).toBeDefined();
      expect(results[0].result).toBeDefined();
      expect(results[0].score).toBeGreaterThan(0);

      // Results should be sorted by score
      for (let i = 1; i < results.length; i++) {
        expect(results[i-1].score).toBeGreaterThanOrEqual(results[i].score);
      }
    });

    test('should provide compression metrics', async () => {
      // Compress multiple worlds to generate metrics
      for (let i = 0; i < 5; i++) {
        const world = generateTestWorld('small');
        await worldCompressionService.compressWorld(world);
      }

      const metrics = worldCompressionService.getMetrics();

      expect(metrics).toBeDefined();
      expect(metrics.totalProcessed).toBeGreaterThan(0);
      expect(metrics.totalCompressed).toBeGreaterThan(0);
      expect(metrics.averageRatio).toBeGreaterThan(0);
      expect(metrics.strategyUsage).toBeDefined();
    });
  });

  describe('Data Size Optimization', () => {
    test('should optimize compression for small vs large worlds', async () => {
      const smallWorld = generateTestWorld('small');
      const largeWorld = generateTestWorld('large');

      const [smallCompressed, largeCompressed] = await Promise.all([
        worldCompressionService.compressWorld(smallWorld),
        worldCompressionService.compressWorld(largeWorld)
      ]);

      const smallOriginal = new Blob([JSON.stringify(smallWorld)]).size;
      const largeOriginal = new Blob([JSON.stringify(largeWorld)]).size;

      expect(smallOriginal).toBeLessThan(largeOriginal);
      expect(largeOriginal).toBeGreaterThan(smallOriginal * 10); // Should be significantly larger

      // Large data should benefit more from compression
      expect(largeCompressed.ratio).toBeLessThan(smallCompressed.ratio);
    });

    test('should handle worlds with high repetition efficiently', async () => {
      const repetitiveWorld = generateTestWorld('small');

      // Add many similar elements
      for (let i = 2; i <= 50; i++) {
        repetitiveWorld.elements.push({
          ...repetitiveWorld.elements[0],
          id: `element-${i}`,
          position: { x: i * 10, y: i * 5, z: i * 2 }
        });
      }

      const result = await worldCompressionService.compressWorld(repetitiveWorld);

      // Highly repetitive data should compress very well
      expect(result.ratio).toBeLessThan(0.5); // Should achieve at least 50% compression
    });
  });

  describe('Error Handling', () => {
    test('should handle compression errors gracefully', async () => {
      const invalidData = {} as any; // Minimal data that might break compression

      await expect(worldCompressionService.compressWorld(invalidData)).resolves.toBeDefined();
    });

    test('should handle decompression of corrupted data', async () => {
      const corruptedCompressionData = {
        algorithm: CompressionStrategy.LZ_STRING,
        originalSize: 1000,
        compressedSize: 500,
        ratio: 0.5,
        data: 'corrupted-compression-data-that-cannot-be-decompressed',
        metadata: {}
      };

      await expect(worldCompressionService.decompressWorld(corruptedCompressionData as any))
        .rejects.toThrow();
    });

    test('should handle unsupported compression strategies', async () => {
      const unsupportedStrategy = 'unsupported-strategy' as CompressionStrategy;

      await expect(worldCompressionService.compressWorld(testWorld, {
        strategy: unsupportedStrategy
      })).resolves.toBeDefined(); // Should fallback to default
    });
  });

  describe('Compression Presets', () => {
    test('should apply different compression presets effectively', async () => {
      const presets = ['REAL_TIME', 'BATCH', 'OFFLINE', 'MOBILE'];
      const results = [];

      for (const preset of presets) {
        const result = await worldCompressionService.compressWorld(testWorld, {
          ...COMPRESSION_PRESETS[preset as keyof typeof COMPRESSION_PRESETS]
        });
        results.push({ preset, ratio: result.ratio, duration: result.duration });
      }

      // All presets should produce valid compression
      results.forEach(({ ratio }) => {
        expect(ratio).toBeLessThan(1);
        expect(ratio).toBeGreaterThan(0);
      });

      // Different presets might produce different results
      const ratios = results.map(r => r.ratio);
      const uniqueRatios = new Set(ratios);
      expect(uniqueRatios.size).toBeGreaterThanOrEqual(2); // At least some variation expected
    });
  });

  describe('Data Characteristics Analysis', () => {
    test('should recommend optimal compression strategies', async () => {
      const smallWorld = generateTestWorld('small');
      const largeWorld = generateTestWorld('large');
      const timelineWorld = generateTestWorld('medium');
      // Add timeline events to indicate temporal data
      timelineWorld.branches.push({
        id: 'feature-branch',
        name: 'Feature Branch',
        description: 'Branch with timeline',
        divergencePoint: new Date(),
        elements: ['element-1'],
        timeline: [{ id: 'timeline-1', type: 'creation', timestamp: new Date(), action: 'created', parameters: {}, preState: {}, postState: {} }],
        isActive: false,
        mergedBranches: []
      });

      const smallRecommendation = worldCompressionService.recommendStrategy(
        new Blob([JSON.stringify(smallWorld)]).size,
        smallWorld.elements.length,
        false
      );

      const largeRecommendation = worldCompressionService.recommendStrategy(
        new Blob([JSON.stringify(largeWorld)]).size,
        largeWorld.elements.length,
        true // Has timeline
      );

      expect(smallRecommendation).toBeDefined();
      expect(largeRecommendation).toBeDefined();

      // Small worlds might use simpler strategies
      expect(['lz-string', 'none']).toContain(smallRecommendation);

      // Large worlds with timeline might use more complex strategies
      expect(['hybrid', 'custom-delta', 'gzip']).toContain(largeRecommendation);
    });
  });

  describe('Parallel Processing', () => {
    test('should handle parallel compression requests', async () => {
      const worlds = [];
      for (let i = 0; i < 5; i++) {
        worlds.push(generateTestWorld('small'));
      }

      const compressionPromises = worlds.map(world =>
        worldCompressionService.compressWorld(world, { parallel: true })
      );

      const results = await Promise.all(compressionPromises);

      expect(results).toHaveLength(5);
      results.forEach(result => {
        expect(result).toBeDefined();
        expect(result.compressedSize).toBeLessThan(result.originalSize);
      });
    });
  });

  describe('Edge Cases', () => {
    test('should handle empty world gracefully', async () => {
      const emptyWorld = generateTestWorld('small');
      emptyWorld.elements = [];
      emptyWorld.creativeDNA.patterns = [];
      emptyWorld.creativeDNA.inspirationHistory = [];
      emptyWorld.branches = [];

      const result = await worldCompressionService.compressWorld(emptyWorld);

      expect(result).toBeDefined();
      expect(result.compressedSize).toBeLessThanOrEqual(result.originalSize);
    });

    test('should handle worlds with special characters in text', async () => {
      const specialWorld = generateTestWorld('small');
      specialWorld.metadata.name = 'Test World with 🎨 emojis and "special" characters & symbols!';
      specialWorld.elements[0].metadata.description = 'Description with ñ, ü, 中文, العربية, and 🌍🌟 emojis';

      const result = await worldCompressionService.compressWorld(specialWorld);
      const decompressed = await worldCompressionService.decompressWorld({
        algorithm: result.algorithm,
        originalSize: result.originalSize,
        compressedSize: result.compressedSize,
        ratio: result.ratio,
        data: result.data
      } as any);

      expect(decompressed.data.metadata.name).toBe(specialWorld.metadata.name);
      expect(decompressed.data.elements[0].metadata.description).toBe(specialWorld.elements[0].metadata.description);
    });

    test('should handle very large compression levels', async () => {
      const result = await worldCompressionService.compressWorld(testWorld, {
        strategy: CompressionStrategy.GZIP,
        level: 9 // Maximum compression
      });

      expect(result.metadata?.level).toBe(9);
      expect(result.compressedSize).toBeLessThan(result.originalSize);
      expect(result.duration).toBeGreaterThan(0);
    });
  });
});