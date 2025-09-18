/**
 * World Persistence Components Index
 * Exports all world persistence UI components and utilities
 */

// Main Provider Component
export { WorldPersistenceProvider, useWorldPersistence } from './WorldPersistenceProvider';
export type { WorldPersistenceProviderProps } from './WorldPersistenceProvider';

// Dashboard Component
export { WorldDashboard } from './WorldDashboard';
export type { WorldDashboardProps } from './WorldDashboard';

// Convenience Hooks
export {
  useAutoSave,
  useWorldExport,
  useWorldBackup,
  useWorldHealth
} from './WorldPersistenceProvider';

// Individual UI Components (additional components can be added here)

// Export types for external consumption
export type {
  WorldState,
  WorldMetadata,
  WorldElement,
  WorldBranch,
  ExportData,
  ImportOptions,
  CompressionData
} from '../../types/world.types';

// Integration utilities (optional - for advanced usage)
export { setupWorldPersistence } from '../../services/worldPersistence';
export type { PersistenceIntegrationOptions } from '../../services/worldPersistence/integration';