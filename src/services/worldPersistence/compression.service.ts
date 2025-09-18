/**
 * World Compression Service - Advanced data compression for large worlds
 * Provides multiple compression strategies optimized for different data types
 */

import { compress, decompress } from 'lz-string';
import pako from 'pako';
import type {
  WorldState,
  WorldElement,
  WorldBranch,
  GlobalPattern,
  CompressionData,
  ElementProperties,
  CreativeDNA
} from '../../types/world.types';

// Compression Strategies
export enum CompressionStrategy {
  LZ_STRING = 'lz-string',
  GZIP = 'gzip',
  ZSTD = 'zstd',
  CUSTOM_DELTA = 'custom-delta',
  HYBRID = 'hybrid'
}

export interface CompressionOptions {
  strategy?: CompressionStrategy;
  level?: number; // 1-9 compression level
  threshold?: number; // Minimum size to compress
  parallel?: boolean;
  enableProfiling?: boolean;
}

export interface CompressionResult {
  algorithm: string;
  originalSize: number;
  compressedSize: number;
  ratio: number;
  duration: number;
  data: string | Uint8Array;
  metadata?: any;
}

export interface DecompressionResult {
  data: any;
  duration: number;
  metadata?: any;
}

export interface CompressionMetrics {
  totalProcessed: number;
  totalCompressed: number;
  averageRatio: number;
  totalTimeSaved: number;
  strategyUsage: Record<string, number>;
  performanceProfile: Record<string, number[]>;
}

export class WorldCompressionService {
  private compressionMetrics: CompressionMetrics;
  private strategyProfiles: Map<string, number[]>;

  constructor() {
    this.compressionMetrics = {
      totalProcessed: 0,
      totalCompressed: 0,
      averageRatio: 0,
      totalTimeSaved: 0,
      strategyUsage: {},
      performanceProfile: {}
    };
    this.strategyProfiles = new Map();
  }

  /**
   * Compress world data using optimal strategy
   */
  async compressWorld(
    world: WorldState,
    options: CompressionOptions = {}
  ): Promise<CompressionResult> {
    const startTime = performance.now();
    const {
      strategy = CompressionStrategy.HYBRID,
      level = 6,
      threshold = 1024 * 50, // 50KB
      parallel = false,
      enableProfiling = false
    } = options;

    const originalData = JSON.stringify(world);
    const originalSize = new Blob([originalData]).size;

    if (originalSize < threshold) {
      return {
        algorithm: 'none',
        originalSize,
        compressedSize: originalSize,
        ratio: 1,
        duration: performance.now() - startTime,
        data: originalData,
        metadata: { reason: 'below_threshold' }
      };
    }

    // Determine optimal strategy if hybrid
    const effectiveStrategy = strategy === CompressionStrategy.HYBRID
      ? await this.selectOptimalStrategy(world, originalData)
      : strategy;

    let compressionResult: CompressionResult;

    try {
      switch (effectiveStrategy) {
        case CompressionStrategy.LZ_STRING:
          compressionResult = await this.compressWithLZString(originalData, level);
          break;

        case CompressionStrategy.GZIP:
          compressionResult = await this.compressWithGzip(originalData, level);
          break;

        case CompressionStrategy.CUSTOM_DELTA:
          compressionResult = await this.compressWithDelta(world, originalData);
          break;

        default:
          compressionResult = await this.compressWithLZString(originalData, level);
      }

      compressionResult.duration = performance.now() - startTime;
      compressionResult.algorithm = effectiveStrategy;

      // Update metrics
      this.updateMetrics(compressionResult, enableProfiling);

      return compressionResult;

    } catch (error) {
      console.error(`Compression failed with strategy ${effectiveStrategy}:`, error);
      throw new Error(`Compression failed: ${error.message}`);
    }
  }

  /**
   * Decompress world data
   */
  async decompressWorld(
    compressedData: CompressionData,
    options: { profile?: boolean } = {}
  ): Promise<DecompressionResult> {
    const startTime = performance.now();

    if (compressedData.algorithm === 'none') {
      return {
        data: JSON.parse(compressedData.data as string),
        duration: performance.now() - startTime
      };
    }

    let decompressedData: string;

    try {
      switch (compressedData.algorithm) {
        case CompressionStrategy.LZ_STRING:
          decompressedData = decompress(compressedData.data as string);
          break;

        case CompressionStrategy.GZIP:
          const compressed = new Uint8Array(atob(compressedData as any).split('').map(c => c.charCodeAt(0)));
          const decompressed = pako.inflate(compressed, { to: 'string' });
          decompressedData = decompressed;
          break;

        case CompressionStrategy.CUSTOM_DELTA:
          decompressedData = await this.decompressDelta(compressedData);
          break;

        default:
          decompressedData = decompress(compressedData.data as string);
      }

      const world = JSON.parse(decompressedData);
      const duration = performance.now() - startTime;

      if (options.profile) {
        console.log(`Decompression completed in ${duration.toFixed(2)}ms using ${compressedData.algorithm}`);
      }

      return {
        data: world,
        duration,
        metadata: { algorithm: compressedData.algorithm }
      };

    } catch (error) {
      console.error('Decompression failed:', error);
      throw new Error(`Decompression failed: ${error.message}`);
    }
  }

  /**
   * Select optimal compression strategy based on data characteristics
   */
  private async selectOptimalStrategy(world: WorldState, data: string): Promise<CompressionStrategy> {
    const dataCharacteristics = this.analyzeDataCharacteristics(world, data);

    // Strategy selection logic
    if (dataCharacteristics.uniquePatterns < 0.1) {
      return CompressionStrategy.LZ_STRING;
    } else if (dataCharacteristics.hasHighRedundancy) {
      return CompressionStrategy.GZIP;
    } else if (dataCharacteristics.hasTemporalData) {
      return CompressionStrategy.CUSTOM_DELTA;
    } else {
      return CompressionStrategy.LZ_STRING;
    }
  }

  /**
   * Analyze data characteristics for optimal strategy selection
   */
  private analyzeDataCharacteristics(world: WorldState, data: string): {
    uniquePatterns: number;
    hasHighRedundancy: boolean;
    hasTemporalData: boolean;
    textRatio: number;
    numericRatio: number;
  } {
    const textAnalysis = this.analyzeTextContent(data);
    const structureAnalysis = this.analyzeWorldStructure(world);

    return {
      uniquePatterns: this.countUniquePatterns(world) / world.elements.length,
      hasHighRedundancy: textAnalysis.repetitionRatio > 0.3,
      hasTemporalData: structureAnalysis.hasTimelineEvents,
      textRatio: textAnalysis.textRatio,
      numericRatio: textAnalysis.numericRatio
    };
  }

  /**
   * Compress using LZ-string algorithm
   */
  private async compressWithLZString(data: string, level: number): Promise<CompressionResult> {
    const compressed = compress(data);
    const compressedSize = new Blob([compressed]).size;
    const originalSize = new Blob([data]).size;

    return {
      algorithm: CompressionStrategy.LZ_STRING,
      originalSize,
      compressedSize,
      ratio: compressedSize / originalSize,
      duration: 0,
      data: compressed,
      metadata: { level }
    };
  }

  /**
   * Compress using Gzip algorithm
   */
  private async compressWithGzip(data: string, level: number): Promise<CompressionResult> {
    const compressed = pako.gzip(data, { level });
    const compressedSize = compressed.length;
    const originalSize = data.length;

    // Convert to base64 for storage
    const base64Data = btoa(String.fromCharCode.apply(null, Array.from(compressed)));

    return {
      algorithm: CompressionStrategy.GZIP,
      originalSize,
      compressedSize,
      ratio: compressedSize / originalSize,
      duration: 0,
      data: base64Data,
      metadata: { level }
    };
  }

  /**
   * Compress using custom delta encoding
   */
  private async compressWithDelta(world: WorldState, data: string): Promise<CompressionResult> {
    // Create a baseline reference
    const baseline = this.createBaseline(world);
    const delta = this.calculateDelta(world, baseline);

    const deltaData = JSON.stringify(delta);
    const compressed = compress(deltaData);

    const compressedSize = new Blob([compressed]).size;
    const originalSize = new Blob([data]).size;

    return {
      algorithm: CompressionStrategy.CUSTOM_DELTA,
      originalSize,
      compressedSize,
      ratio: compressedSize / originalSize,
      duration: 0,
      data: compressed,
      metadata: { baselineId: baseline.id }
    };
  }

  /**
   * Decompress delta-encoded data
   */
  private async decompressDelta(compressedData: CompressionData): Promise<string> {
    const deltaData = decompress(compressedData.data as string);
    const delta = JSON.parse(deltaData);

    // Reconstruct world from delta
    const world = this.reconstructFromDelta(delta, compressedData.metadata.baselineId);
    return JSON.stringify(world);
  }

  /**
   * Create baseline for delta compression
   */
  private createBaseline(world: WorldState): any {
    return {
      id: `baseline_${Date.now()}`,
      version: world.metadata.version,
      elements: world.elements.map(el => ({
        id: el.id,
        type: el.type,
        position: el.position,
        metadata: { name: el.metadata.name }
      })),
      settings: world.settings,
      statistics: world.statistics
    };
  }

  /**
   * Calculate delta between current and baseline
   */
  private calculateDelta(world: WorldState, baseline: any): any {
    const delta: any = {
      baselineId: baseline.id,
      timestamp: new Date().toISOString(),
      metadata: {
        version: world.metadata.version,
        lastModified: world.metadata.lastModified
      },
      elementChanges: [],
      newElements: [],
      deletedElements: [],
      patternChanges: [],
      branchChanges: []
    };

    // Find element changes
    const baselineElements = new Map(baseline.elements.map((el: any) => [el.id, el]));

    world.elements.forEach(element => {
      const baselineElement = baselineElements.get(element.id);
      if (baselineElement) {
        const changes = this.findElementChanges(element, baselineElement);
        if (Object.keys(changes).length > 0) {
          delta.elementChanges.push({ id: element.id, changes });
        }
      } else {
        delta.newElements.push({
          id: element.id,
          type: element.type,
          position: element.position,
          properties: element.properties,
          metadata: element.metadata
        });
      }
    });

    // Find deleted elements
    const currentElementIds = new Set(world.elements.map(el => el.id));
    baseline.elements.forEach((baselineEl: any) => {
      if (!currentElementIds.has(baselineEl.id)) {
        delta.deletedElements.push(baselineEl.id);
      }
    });

    return delta;
  }

  /**
   * Find specific changes in an element
   */
  private findElementChanges(current: WorldElement, baseline: any): any {
    const changes: any = {};

    // Check position changes
    if (JSON.stringify(current.position) !== JSON.stringify(baseline.position)) {
      changes.position = current.position;
    }

    // Check metadata changes
    if (current.metadata.name !== baseline.metadata.name) {
      changes.name = current.metadata.name;
    }

    // Check properties changes
    const currentProps = JSON.stringify(current.properties);
    const baselineProps = JSON.stringify(this.getElementBaselineProperties(baseline));
    if (currentProps !== baselineProps) {
      changes.properties = current.properties;
    }

    return changes;
  }

  /**
   * Get baseline properties for comparison
   */
  private getElementBaselineProperties(baseline: any): any {
    return {
      visual: { color: '#ffffff', opacity: 1 },
      physics: { mass: 1, gravity: true, collision: false },
      behavior: { type: 'static', parameters: {} },
      interactions: { clickable: false, draggable: false, hoverable: false }
    };
  }

  /**
   * Reconstruct world from delta
   */
  private reconstructFromDelta(delta: any, baselineId: string): WorldState {
    // This is a simplified implementation
    // In practice, you'd need the original baseline or a reference to it
    const reconstructed: Partial<WorldState> = {
      metadata: {
        ...baselineId as any,
        version: delta.metadata.version,
        lastModified: new Date(delta.metadata.lastModified)
      }
    };

    // Apply element changes
    if (delta.elementChanges?.length > 0) {
      // Apply specific changes to elements
      console.log('Applying element changes:', delta.elementChanges.length);
    }

    return reconstructed as WorldState;
  }

  /**
   * Analyze text content characteristics
   */
  private analyzeTextContent(data: string): {
    textRatio: number;
    numericRatio: number;
    repetitionRatio: number;
    uniqueStrings: number;
  } {
    const characters = data.length;
    const textMatches = data.match(/[a-zA-Z]/g) || [];
    const numericMatches = data.match(/[0-9]/g) || [];

    // Simple repetition analysis
    const lines = data.split('\n');
    const uniqueLines = new Set(lines);
    const repetitionRatio = 1 - (uniqueLines.size / lines.length);

    return {
      textRatio: textMatches.length / characters,
      numericRatio: numericMatches.length / characters,
      repetitionRatio,
      uniqueStrings: uniqueLines.size
    };
  }

  /**
   * Analyze world structure for compression hints
   */
  private analyzeWorldStructure(world: WorldState): {
    hasTimelineEvents: boolean;
    hasComplexPatterns: boolean;
    hasSpatialData: boolean;
    elementCount: number;
    relationshipDensity: number;
  } {
    const hasTimelineEvents = world.branches.length > 1;
    const hasComplexPatterns = world.patterns.some(p => p.frequency > 10);
    const hasSpatialData = world.elements.some(el => el.position);

    const totalPossibleRelationships = world.elements.length * (world.elements.length - 1) / 2;
    const actualRelationships = world.elements.reduce((sum, el) => sum + el.relationships.length, 0);
    const relationshipDensity = totalPossibleRelationships > 0 ? actualRelationships / totalPossibleRelationships : 0;

    return {
      hasTimelineEvents,
      hasComplexPatterns,
      hasSpatialData,
      elementCount: world.elements.length,
      relationshipDensity
    };
  }

  /**
   * Count unique patterns for compression analysis
   */
  private countUniquePatterns(world: WorldState): number {
    const patternSignatures = new Set<string>();

    world.patterns.forEach(pattern => {
      patternSignatures.add(`${pattern.type}:${pattern.frequency}`);
    });

    world.elements.forEach(element => {
      patternSignatures.add(element.type);
    });

    return patternSignatures.size;
  }

  /**
   * Update compression metrics
   */
  private updateMetrics(result: CompressionResult, enableProfiling: boolean): void {
    this.compressionMetrics.totalProcessed++;

    if (result.ratio < 1) {
      this.compressionMetrics.totalCompressed++;
    }

    this.compressionMetrics.averageRatio =
      (this.compressionMetrics.averageRatio * (this.compressionMetrics.totalProcessed - 1) + result.ratio) /
      this.compressionMetrics.totalProcessed;

    this.compressionMetrics.strategyUsage[result.algorithm] =
      (this.compressionMetrics.strategyUsage[result.algorithm] || 0) + 1;

    if (enableProfiling) {
      const profileKey = `${result.algorithm}-${result.originalSize}`;
      if (!this.compressionMetrics.performanceProfile[profileKey]) {
        this.compressionMetrics.performanceProfile[profileKey] = [];
      }
      this.compressionMetrics.performanceProfile[profileKey].push(result.duration);
    }
  }

  /**
   * Get compression performance metrics
   */
  getMetrics(): CompressionMetrics {
    return { ...this.compressionMetrics };
  }

  /**
   * Get recommended compression strategy for data characteristics
   */
  recommendStrategy(worldSize: number, elementCount: number, hasTimeline: boolean): CompressionStrategy {
    if (worldSize < 1024 * 10) { // < 10KB
      return CompressionStrategy.NONE;
    } else if (worldSize < 1024 * 100) { // < 100KB
      return CompressionStrategy.LZ_STRING;
    } else if (hasTimeline && elementCount > 100) {
      return CompressionStrategy.CUSTOM_DELTA;
    } else if (worldSize < 1024 * 500) { // < 500KB
      return CompressionStrategy.GZIP;
    } else {
      return CompressionStrategy.HYBRID;
    }
  }

  /**
   * Benchmark compression strategies for specific data
   */
  async benchmarkStrategies(world: WorldState, strategies: CompressionStrategy[]): Promise<{
    strategy: CompressionStrategy;
    result: CompressionResult;
    score: number;
  }[]> {
    const results: { strategy: CompressionStrategy; result: CompressionResult; score: number }[] = [];

    for (const strategy of strategies) {
      try {
        const result = await this.compressWorld(world, { strategy, enableProfiling: true });
        const score = this.calculateCompressionScore(result);
        results.push({ strategy, result, score });
      } catch (error) {
        console.error(`Strategy ${strategy} failed:`, error);
      }
    }

    return results.sort((a, b) => b.score - a.score);
  }

  /**
   * Calculate compression effectiveness score
   */
  private calculateCompressionScore(result: CompressionResult): number {
    // Score based on ratio and speed
    const ratioScore = (1 - result.ratio) * 100; // Higher compression = higher score
    const speedScore = Math.max(0, 100 - result.duration); // Faster = higher score
    return (ratioScore * 0.7) + (speedScore * 0.3);
  }
}

// Export singleton instance
export const worldCompressionService = new WorldCompressionService();
export default WorldCompressionService;

// Default compression options
export const DEFAULT_COMPRESSION_OPTIONS: CompressionOptions = {
  strategy: CompressionStrategy.HYBRID,
  level: 6,
  threshold: 1024 * 50, // 50KB
  parallel: false,
  enableProfiling: false
};

// Compression presets for different scenarios
export const COMPRESSION_PRESETS = {
  REAL_TIME: {
    strategy: CompressionStrategy.LZ_STRING,
    level: 3,
    threshold: 1024 * 25
  },
  BATCH: {
    strategy: CompressionStrategy.GZIP,
    level: 9,
    threshold: 1024 * 10
  },
  OFFLINE: {
    strategy: CompressionStrategy.HYBRID,
    level: 8,
    threshold: 0
  },
  MOBILE: {
    strategy: CompressionStrategy.LZ_STRING,
    level: 6,
    threshold: 1024 * 50
  }
} as Record<string, CompressionOptions>;