/**
 * World Persistence Types - MYNFINI IndexedDB Implementation
 * Defines comprehensive type system for world state management
 */

export interface WorldMetadata {
  id: string;
  name: string;
  description: string;
  createdAt: Date;
  lastModified: Date;
  version: number;
  branchId: string;
  tags: string[];
  thumbnail?: string;
  isPublic: boolean;
  ownerId: string;
}

export interface CreativeDNA {
  patterns: Pattern[];
  evolutionScore: number;
  inspirationHistory: InspirationEvent[];
  creativityMetrics: CreativityMetrics;
  adaptationTraits: AdaptationTrait[];
}

export interface Pattern {
  id: string;
  type: PatternType;
  frequency: number;
  confidence: number;
  context: Record<string, any>;
  timestamp: Date;
  source: PatternSource;
}

export interface InspirationEvent {
  id: string;
  source: string;
  type: InspirationType;
  content: string;
  impact: number;
  timestamp: Date;
  context: Record<string, any>;
}

export interface CreativityMetrics {
  originality: number;
  complexity: number;
  coherence: number;
  novelty: number;
  fluency: number;
  adaptability: number;
}

export interface AdaptationTrait {
  id: string;
  name: string;
  value: number;
  stability: number;
  evolutionHistory: EvolutionPoint[];
}

export interface EvolutionPoint {
  timestamp: Date;
  value: number;
  trigger: string;
  context: Record<string, any>;
}

export interface WorldElement {
  id: string;
  type: ElementType;
  position: Position3D;
  properties: ElementProperties;
  relationships: ElementRelationship[];
  metadata: ElementMetadata;
  version: number;
  branchId: string;
}

export interface Position3D {
  x: number;
  y: number;
  z: number;
  rotation?: Rotation3D;
  scale?: Scale3D;
}

export interface Rotation3D {
  x: number;
  y: number;
  z: number;
  order?: string;
}

export interface Scale3D {
  x: number;
  y: number;
  z: number;
}

export interface ElementProperties {
  [key: string]: any;
  visual?: VisualProperties;
  physics?: PhysicsProperties;
  behavior?: BehaviorProperties;
  interactions?: InteractionProperties;
}

export interface VisualProperties {
  color: string;
  opacity: number;
  texture?: string;
  geometry?: string;
  material?: string;
  lighting?: LightingProperties;
}

export interface PhysicsProperties {
  mass: number;
  gravity: boolean;
  collision: boolean;
  velocity?: Vector3D;
  acceleration?: Vector3D;
}

export interface BehaviorProperties {
  type: BehaviorType;
  parameters: Record<string, any>;
  triggers: BehaviorTrigger[];
}

export interface InteractionProperties {
  clickable: boolean;
  draggable: boolean;
  hoverable: boolean;
  selectable: boolean;
  responses: InteractionResponse[];
}

export interface ElementRelationship {
  targetId: string;
  type: RelationshipType;
  strength: number;
  bidirectional: boolean;
  metadata: Record<string, any>;
}

export interface ElementMetadata {
  name: string;
  description: string;
  tags: string[];
  createdAt: Date;
  lastModified: Date;
  authorId: string;
  version: number;
}

export interface WorldBranch {
  id: string;
  parentId?: string;
  name: string;
  description: string;
  divergencePoint: Date;
  elements: string[];
  timeline: TimelineEvent[];
  isActive: boolean;
  mergedBranches: string[];
  mergeStatus?: MergeStatus;
}

export interface TimelineEvent {
  id: string;
  type: TimelineEventType;
  timestamp: Date;
  elementId?: string;
  userId?: string;
  action: string;
  parameters: Record<string, any>;
  preState: Record<string, any>;
  postState: Record<string, any>;
}

export interface WorldState {
  metadata: WorldMetadata;
  creativeDNA: CreativeDNA;
  elements: WorldElement[];
  branches: WorldBranch[];
  activeBranchId: string;
  patterns: GlobalPattern[];
  settings: WorldSettings;
  statistics: WorldStatistics;
  compressionRatio?: number;
}

export interface GlobalPattern {
  id: string;
  type: GlobalPatternType;
  frequency: number;
  elements: string[];
  confidence: number;
  evolution: PatternEvolution;
  timestamp: Date;
}

export interface PatternEvolution {
  stages: EvolutionStage[];
  complexity: number;
  novelty: number;
  stability: number;
}

export interface EvolutionStage {
  timestamp: Date;
  complexity: number;
  novelty: number;
  participation: number;
}

export interface WorldSettings {
  physics: PhysicsSettings;
  rendering: RenderingSettings;
  interaction: InteractionSettings;
  persistence: PersistenceSettings;
  creativity: CreativitySettings;
}

export interface PhysicsSettings {
  gravity: Vector3D;
  friction: number;
  collisionDetection: boolean;
  timeScale: number;
  constraints: PhysicsConstraint[];
}

export interface RenderingSettings {
  quality: RenderQuality;
  shadows: boolean;
  reflections: boolean;
  antiAliasing: boolean;
  postProcessing: string[];
}

export interface InteractionSettings {
  mouseSensitivity: number;
  keyboardShortcuts: Record<string, string>;
  gestureSupport: boolean;
  hapticFeedback: boolean;
  accessibilityMode: boolean;
}

export interface PersistenceSettings {
  autoSaveInterval: number;
  maxBranches: number;
  compressionLevel: number;
  backupCount: number;
  syncOnSave: boolean;
}

export interface CreativitySettings {
  aiAssistance: boolean;
  patternRecognition: boolean;
  inspirationSources: string[];
  evolutionSpeed: number;
  complexityThreshold: number;
}

export interface WorldStatistics {
  totalElements: number;
  totalBranches: number;
  creationTime: Date;
  totalPlayTime: number;
  modificationCount: number;
  collaborationCount: number;
  creativityScore: number;
}

export interface ConflictResolution {
  conflictId: string;
  type: ConflictType;
  elements: string[];
  branches: string[];
  resolution: ConflictResolutionStrategy;
  timestamp: Date;
  resolutionTimestamp?: Date;
  resolvedBy?: string;
}

export interface ExportData {
  format: ExportFormat;
  version: string;
  worldState: WorldState;
  metadata: ExportMetadata;
  compression?: CompressionData;
  checksum: string;
}

export interface ImportOptions {
  conflictResolution: ImportConflictResolution;
  preserveIds: boolean;
  validateSchema: boolean;
  createBackup: boolean;
  mergeStrategy?: MergeStrategy;
}

// Type Enums

export enum PatternType {
  GEOMETRIC = 'geometric',
  COLOR = 'color',
  SPATIAL = 'spatial',
  TEMPORAL = 'temporal',
  BEHAVIORAL = 'behavioral',
  CREATIVE = 'creative'
}

export enum PatternSource {
  USER = 'user',
  AI = 'ai',
  SYSTEM = 'system',
  COLLABORATIVE = 'collaborative',
  EVOLVED = 'evolved'
}

export enum InspirationType {
  VISUAL = 'visual',
  AUDIO = 'audio',
  TEXTUAL = 'textual',
  INTERACTIVE = 'interactive',
  AI_GENERATED = 'ai_generated'
}

export enum ElementType {
  GEOMETRY = 'geometry',
  LIGHT = 'light',
  PARTICLE = 'particle',
  TEXT = 'text',
  IMAGE = 'image',
  AUDIO = 'audio',
  INTERACTIVE = 'interactive',
  AI_GENERATED = 'ai_generated'
}

export enum RelationshipType {
  PARENT_CHILD = 'parent_child',
  SIBLING = 'sibling',
  DEPENDENCY = 'dependency',
  INFLUENCE = 'influence',
  CONNECTION = 'connection',
  GROUP = 'group'
}

export enum TimelineEventType {
  CREATION = 'creation',
  MODIFICATION = 'modification',
  DELETION = 'deletion',
  BRANCH = 'branch',
  MERGE = 'merge',
  PATTERN = 'pattern',
  INSPIRATION = 'inspiration'
}

export enum BehaviorType {
  STATIC = 'static',
  DYNAMIC = 'dynamic',
  INTERACTIVE = 'interactive',
  AI_DRIVEN = 'ai_driven',
  SCRIPTED = 'scripted'
}

export enum GlobalPatternType {
  SPATIAL_DISTRIBUTION = 'spatial_distribution',
  COLOR_PALETTE = 'color_palette',
  BEHAVIOR_CLUSTER = 'behavior_cluster',
  EVOLUTIONARY_TREND = 'evolutionary_trend',
  CREATIVE_FLOW = 'creative_flow'
}

export enum ConflictType {
  ELEMENT_OVERLAP = 'element_overlap',
  PROPERTY_CONFLICT = 'property_conflict',
  BRANCH_DIVERGENCE = 'branch_divergence',
  DELETION_CONFLICT = 'deletion_conflict',
  ACCESS_CONFLICT = 'access_conflict'
}

export enum ConflictResolutionStrategy {
  AUTO_MERGE = 'auto_merge',
  MANUAL_RESOLUTION = 'manual_resolution',
  LAST_WRITE_WINS = 'last_write_wins',
  VERSION_CONTROL = 'version_control',
  BRANCH_CREATION = 'branch_creation'
}

export enum ExportFormat {
  JSON = 'json',
  COMPRESSED_JSON = 'compressed_json',
  QR_CODE = 'qr_code',
  BACKUP = 'backup'
}

export enum ImportConflictResolution {
  REPLACE = 'replace',
  MERGE = 'merge',
  SKIP = 'skip',
  RENAME = 'rename',
  PROMPT = 'prompt'
}

export enum MergeStrategy {
  ADDITIVE = 'additive',
  REPLACE = 'replace',
  INTELLIGENT = 'intelligent'
}

// Utility Types

export interface Vector3D {
  x: number;
  y: number;
  z: number;
}

export interface BehaviorTrigger {
  event: string;
  condition: string;
  action: string;
  parameters: Record<string, any>;
}

export interface InteractionResponse {
  type: InteractionType;
  action: string;
  parameters: Record<string, any>;
  feedback?: string;
}

export interface LightingProperties {
  intensity: number;
  color: string;
  type: LightingType;
  shadows: boolean;
}

export interface PhysicsConstraint {
  type: ConstraintType;
  parameters: Record<string, any>;
}

export interface CompressionData {
  algorithm: string;
  ratio: number;
  originalSize: number;
  compressedSize: number;
  checksum: string;
}

export interface ExportMetadata {
  exportedAt: Date;
  exportedBy: string;
  applicationVersion: string;
  compatibility: string[];
}

export interface MergeStatus {
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  progress: number;
  conflicts: ConflictResolution[];
  mergedAt?: Date;
}

// Event Types for React Integration

export interface WorldStateChangeEvent {
  type: 'create' | 'update' | 'delete' | 'branch' | 'merge';
  worldId: string;
  elementId?: string;
  branchId?: string;
  timestamp: Date;
  data: Partial<WorldState>;
}

export interface PersistenceEvent {
  type: 'save_start' | 'save_complete' | 'save_error' | 'load_start' | 'load_complete' | 'load_error';
  worldId: string;
  timestamp: Date;
  data?: any;
  error?: Error;
}

// IndexedDB Specific Types

export interface DatabaseSchema {
  version: number;
  worlds: WorldRecord;
  elements: ElementRecord;
  branches: BranchRecord;
  patterns: PatternRecord;
  timeline: TimelineRecord;
  settings: SettingsRecord;
}

export interface WorldRecord extends WorldState {
  _id: string;
  _rev?: string;
  _compressed?: CompressionData;
  _syncStatus?: SyncStatus;
}

export interface ElementRecord extends WorldElement {
  _id: string;
  _worldId: string;
  _compressed?: CompressionData;
}

export interface BranchRecord extends WorldBranch {
  _id: string;
  _worldId: string;
  _compressed?: CompressionData;
}

export interface PatternRecord extends GlobalPattern {
  _id: string;
  _worldId: string;
  _compressed?: CompressionData;
}

export interface TimelineRecord extends TimelineEvent {
  _id: string;
  _worldId: string;
}

export interface SettingsRecord extends WorldSettings {
  _id: string;
  _worldId: string;
}

export interface SyncStatus {
  lastSync?: Date;
  syncPending: boolean;
  conflicts: ConflictResolution[];
  remoteVersion?: number;
}

export enum InteractionType {
  CLICK = 'click',
  HOVER = 'hover',
  DRAG = 'drag',
  SCROLL = 'scroll',
  KEYBOARD = 'keyboard',
  VOICE = 'voice',
  GESTURE = 'gesture'
}

export enum LightingType {
  AMBIENT = 'ambient',
  DIRECTIONAL = 'directional',
  POINT = 'point',
  SPOT = 'spot'
}

export enum ConstraintType {
  FIXED = 'fixed',
  SPRING = 'spring',
  DAMPED = 'damped',
  CUSTOM = 'custom'
}

export enum RenderQuality {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  ULTRA = 'ultra'
}