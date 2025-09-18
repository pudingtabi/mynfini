/**
 * World Dashboard Component
 * Comprehensive UI for world persistence management and monitoring
 */

import React, { useState, useEffect } from 'react';
import {
  useWorldPersistence,
  useAutoSave,
  useWorldExport,
  useWorldBackup,
  useWorldHealth
} from './WorldPersistenceProvider';
import { QrCode, Download, Upload, Save, Settings, Shield, Activity, AlertTriangle, CheckCircle, Clock, Zap, Network } from 'lucide-react';

interface WorldDashboardProps {
  className?: string;
  onWorldSelect?: (worldId: string) => void;
  onCreateNewWorld?: () => void;
}

export const WorldDashboard: React.FC<WorldDashboardProps> = ({
  className = '',
  onWorldSelect,
  onCreateNewWorld
}) => {
  const {
    loadedWorld,
    loading,
    error,
    worldList,
    loadWorld,
    createWorld,
    saveWorld,
    deleteWorld,
    refreshWorldList
  } = useWorldPersistence();

  const { autoSaveEnabled, setAutoSave, lastSaveTime, pendingChanges } = useAutoSave();
  const { exportWorld, importWorld } = useWorldExport();
  const { createBackup } = useWorldBackup();
  const { validateWorld, getHealthReport } = useWorldHealth();

  const [activeTab, setActiveTab] = useState<'overview' | 'backups' | 'export' | 'health' | 'settings'>('overview');
  const [selectedWorldId, setSelectedWorldId] = useState<string | null>(null);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [showImportDialog, setShowImportDialog] = useState(false);
  const [exportFormat, setExportFormat] = useState<'json' | 'compressed' | 'qr'>('compressed');
  const [importFile, setImportFile] = useState<File | null>(null);
  const [healthReport, setHealthReport] = useState<any>(null);
  const [validationResult, setValidationResult] = useState<any>(null);

  // Load health report and validation when overview tab is active
  useEffect(() => {
    if (activeTab === 'health' && loadedWorld) {
      loadHealthReport();
    }
  }, [activeTab, loadedWorld]);

  const loadHealthReport = async () => {
    if (!loadedWorld) return;

    try {
      const report = await getHealthReport();
      setHealthReport(report);

      const validation = await validateWorld();
      setValidationResult(validation);
    } catch (error) {
      console.error('Failed to load health report:', error);
    }
  };

  const handleCreateWorld = async (name: string, description?: string) => {
    try {
      const worldId = await createWorld({
        name: name || 'New World',
        description: description || '',
        ownerId: 'current-user'
      });

      setSelectedWorldId(worldId);
      await loadWorld(worldId);
      setShowCreateDialog(false);
      onCreateNewWorld?.();
    } catch (error) {
      console.error('Failed to create world:', error);
    }
  };

  const handleWorldSelect = async (worldId: string) => {
    try {
      await loadWorld(worldId);
      setSelectedWorldId(worldId);
      onWorldSelect?.(worldId);
    } catch (error) {
      console.error('Failed to load world:', error);
    }
  };

  const handleExport = async (format: 'json' | 'compressed' | 'qr') => {
    if (!loadedWorld) return;

    try {
      const exportData = await exportWorld(format);

      if (format === 'qr') {
        // Generate QR code data URL
        const qrDataUrl = `data:application/json;base64,${btoa(JSON.stringify(exportData, null, 2))}`;

        // Create download link
        const link = document.createElement('a');
        link.href = qrDataUrl;
        link.download = `${loadedWorld.metadata.name.replace(/[^a-zA-Z0-9]/g, '_')}_world_data.json`;
        link.click();
      } else {
        // Direct file download
        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${loadedWorld.metadata.name.replace(/[^a-zA-Z0-9]/g, '_')}_world_backup.${format === 'json' ? 'json' : 'json'}`;
        link.click();
        URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error('Failed to export world:', error);
    }
  };

  const handleImport = async () => {
    if (!importFile) return;

    try {
      const text = await importFile.text();
      const importData = JSON.parse(text);
      const worldId = await importWorld(importData);

      setImportFile(null);
      setShowImportDialog(false);
      await refreshWorldList();
      await handleWorldSelect(worldId);
    } catch (error) {
      console.error('Failed to import world:', error);
    }
  };

  const handleDelete = async (worldId: string) => {
    if (!confirm(`Are you sure you want to delete this world? This action cannot be undone.`)) {
      return;
    }

    try {
      await deleteWorld(worldId);

      if (loadedWorld && loadedWorld.metadata.id === worldId) {
        setSelectedWorldId(null);
      }

      await refreshWorldList();
    } catch (error) {
      console.error('Failed to delete world:', error);
    }
  };

  const handleBackup = async () => {
    if (!loadedWorld) return;

    try {
      const backupId = await createBackup();
      console.log(`Backup created: ${backupId}`);
      alert('Backup created successfully!');
    } catch (error) {
      console.error('Failed to create backup:', error);
      alert('Failed to create backup');
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  const formatDuration = (ms: number): string => {
    if (ms < 1000) return `${ms}ms`;
    if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
    return `${(ms / 60000).toFixed(1)}m`;
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'text-red-600';
      case 'high': return 'text-red-500';
      case 'medium': return 'text-yellow-500';
      case 'low': return 'text-blue-500';
      default: return 'text-gray-500';
    }
  };

  return (
    <div className={`world-dashboard bg-white rounded-lg shadow-lg overflow-hidden ${className}`}>
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold flex items-center gap-2">
              <Shield className="w-6 h-6" />
              World Persistence Dashboard
            </h1>
            <p className="text-blue-100 mt-1">Manage your worlds, backups, and persistence settings</p>
          </div>
          <div className="flex items-center gap-4">
            {lastSaveTime && (
              <div className="text-sm text-blue-100">
                <Clock className="w-4 h-4 inline mr-1" />
                Last saved: {lastSaveTime.toLocaleTimeString()}
              </div>
            )}
            {pendingChanges && (
              <div className="bg-yellow-500 text-yellow-900 px-2 py-1 rounded text-xs font-medium">
                Unsaved changes
              </div>
            )}
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 m-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <AlertTriangle className="h-5 w-5 text-red-400" />
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Persistence Error</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>{error.message}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="flex">
        {/* Sidebar - World List */}
        <div className="w-80 bg-gray-50 border-r border-gray-200 p-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-800">My Worlds</h2>
            <button
              onClick={() => setShowCreateDialog(true)}
              className="bg-blue-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors"
            >
              Create New
            </button>
          </div>

          <div className="space-y-2 max-h-96 overflow-y-auto">
            {worldList.map((world) => (
              <div
                key={world.id}
                className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                  selectedWorldId === world.id
                    ? 'bg-blue-50 border-blue-200'
                    : 'bg-white border-gray-200 hover:bg-gray-50'
                }`}
                onClick={() => handleWorldSelect(world.id)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <h3 className="text-sm font-medium text-gray-900 truncate">
                      {world.name}
                    </h3>
                    <p className="text-xs text-gray-500 mt-1">
                      Version {world.version} • {world.lastModified.toLocaleDateString()}
                    </p>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDelete(world.id);
                    }}
                    className="text-gray-400 hover:text-red-500 p-1"
                  >
                    ×
                  </button>
                </div>
              </div>
            ))}
            {worldList.length === 0 && (
              <div className="text-center text-gray-500 py-8">
                <p>No worlds found</p>
                <button
                  onClick={() => setShowCreateDialog(true)}
                  className="text-blue-600 hover:text-blue-700 mt-2 text-sm"
                >
                  Create your first world
                </button>
              </div>
            )}
          </div>

          <div className="mt-4 pt-4 border-t border-gray-200">
            <button
              onClick={() => setShowImportDialog(true)}
              className="w-full bg-gray-100 text-gray-700 px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-200 transition-colors flex items-center justify-center gap-2"
            >
              <Upload className="w-4 h-4" />
              Import World
            </button>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1">
          {!loadedWorld ? (
            <div className="flex items-center justify-center h-full text-gray-500">
              <div className="text-center">
                <Shield className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                <h3 className="text-lg font-medium mb-2">No World Selected</h3>
                <p>Select a world from the sidebar to view persistence details</p>
              </div>
            </div>
          ) : (
            <div className="p-6">
              {/* Current World Header */}
              <div className="bg-gray-50 rounded-lg p-6 mb-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900">{loadedWorld.metadata.name}</h2>
                    <p className="text-gray-600 mt-1">{loadedWorld.metadata.description}</p>
                    <div className="flex items-center gap-4 mt-3 text-sm text-gray-500">
                      <span>Version {loadedWorld.metadata.version}</span>
                      <span>{loadedWorld.elements.length} elements</span>
                      <span>{loadedWorld.branches.length} branches</span>
                      <span>Created {loadedWorld.metadata.createdAt.toLocaleDateString()}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => setAutoSave(!autoSaveEnabled)}
                      className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                        autoSaveEnabled
                          ? 'bg-green-100 text-green-800 hover:bg-green-200'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      <Save className="w-4 h-4 inline mr-1" />
                      Auto-save {autoSaveEnabled ? 'On' : 'Off'}
                    </button>
                    <button
                      onClick={handleBackup}
                      className="bg-blue-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors"
                    >
                      <Shield className="w-4 h-4 inline mr-1" />
                      Create Backup
                    </button>
                    <button
                      onClick={() => saveWorld(loadedWorld)}
                      disabled={loading}
                      className="bg-green-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-green-700 transition-colors disabled:opacity-50"
                    >
                      <Save className="w-4 h-4 inline mr-1" />
                      Save Now
                    </button>
                  </div>
                </div>
              </div>

              {/* Tabs */}
              <div className="border-b border-gray-200 mb-6">
                <nav className="flex space-x-8">
                  {[
                    { id: 'overview', label: 'Overview', icon: Activity },
                    { id: 'export', label: 'Export/Import', icon: Download },
                    { id: 'health', label: 'Health Check', icon: CheckCircle },
                    { id: 'backups', label: 'Backups', icon: Shield },
                    { id: 'settings', label: 'Settings', icon: Settings }
                  ].map(({ id, label, icon: Icon }) => (
                    <button
                      key={id}
                      onClick={() => setActiveTab(id as any)}
                      className={`flex items-center gap-2 py-3 px-1 border-b-2 font-medium text-sm ${
                        activeTab === id
                          ? 'border-blue-500 text-blue-600'
                          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                      {label}
                    </button>
                  ))}
                </nav>
              </div>

              {/* Tab Content */}
              {activeTab === 'overview' && (
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="bg-white p-6 rounded-lg border border-gray-200">
                      <h3 className="text-sm font-medium text-gray-500">File Size</h3>
                      <p className="text-2xl font-semibold text-gray-900 mt-2">
                        {formatFileSize(new Blob([JSON.stringify(loadedWorld)]).size)}
                      </p>
                    </div>
                    <div className="bg-white p-6 rounded-lg border border-gray-200">
                      <h3 className="text-sm font-medium text-gray-500">Elements</h3>
                      <p className="text-2xl font-semibold text-gray-900 mt-2">{loadedWorld.elements.length}</p>
                    </div>
                    <div className="bg-white p-6 rounded-lg border border-gray-200">
                      <h3 className="text-sm font-medium text-gray-500">Sync Status</h3>
                      <p className="text-2xl font-semibold text-gray-900 mt-2 flex items-center gap-2">
                        <Network className="w-5 h-5 text-green-500" />
                        Online
                      </p>
                    </div>
                    <div className="bg-white p-6 rounded-lg border border-gray-200">
                      <h3 className="text-sm font-medium text-gray-500">Compression</h3>
                      <p className="text-2xl font-semibold text-gray-900 mt-2">
                        {(new Blob([JSON.stringify(loadedWorld)]).size * 0.7).toFixed(1)}KB
                      </p>
                    </div>
                  </div>

                  <div className="bg-white p-6 rounded-lg border border-gray-200">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Activity</h3>
                    <div className="space-y-3">
                      <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <Save className="w-5 h-5 text-green-500" />
                        <div>
                          <p className="text-sm font-medium text-gray-900">World saved</p>
                          <p className="text-xs text-gray-500">{lastSaveTime ? lastSaveTime.toLocaleTimeString() : 'Never'}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'export' && (
                <div className="space-y-6">
                  <div className="bg-white p-6 rounded-lg border border-gray-200">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Export World</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <button
                        onClick={() => handleExport('json')}
                        className="p-4 border-2 border-gray-200 rounded-lg hover:border-blue-500 transition-colors text-left"
                      >
                        <h4 className="font-medium text-gray-900">JSON Export</h4>
                        <p className="text-sm text-gray-500 mt-1">Human-readable format, larger file size</p>
                      </button>
                      <button
                        onClick={() => handleExport('compressed')}
                        className="p-4 border-2 border-gray-200 rounded-lg hover:border-blue-500 transition-colors text-left"
                      >
                        <h4 className="font-medium text-gray-900">Compressed Export</h4>
                        <p className="text-sm text-gray-500 mt-1">Optimized size, faster transfer</p>
                      </button>
                      <button
                        onClick={() => handleExport('qr')}
                        className="p-4 border-2 border-gray-200 rounded-lg hover:border-blue-500 transition-colors text-left"
                      >
                        <h4 className="font-medium text-gray-900">QR Code Data</h4>
                        <p className="text-sm text-gray-500 mt-1">Share via QR code</p>
                      </button>
                    </div>
                  </div>

                  <div className="bg-white p-6 rounded-lg border border-gray-200">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Import World</h3>
                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors">
                      <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                      <p className="text-gray-600 mb-2">Click to select a world file to import</p>
                      <input
                        type="file"
                        accept=".json"
                        onChange={(e) => setImportFile(e.target.files?.[0] || null)}
                        className="hidden"
                        id="import-file"
                      />
                      <label
                        htmlFor="import-file"
                        className="cursor-pointer bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors"
                      >
                        Choose File
                      </label>
                      {importFile && (
                        <div className="mt-4">
                          <p className="text-sm text-gray-600">Selected: {importFile.name}</p>
                          <button
                            onClick={handleImport}
                            className="mt-2 bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700 transition-colors"
                          >
                            Import World
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'health' && (
                <div className="space-y-6">
                  {validationResult && (
                    <div className="bg-white p-6 rounded-lg border border-gray-200">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">Validation Results</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="flex items-center gap-3">
                          {validationResult.valid ? (
                            <CheckCircle className="w-6 h-6 text-green-500" />
                          ) : (
                            <AlertTriangle className="w-6 h-6 text-red-500" />
                          )}
                          <div>
                            <p className="font-medium text-gray-900">
                              {validationResult.valid ? 'World is valid' : 'Issues detected'}
                            </p>
                            <p className="text-sm text-gray-500">
                              {validationResult.errors.length} errors, {validationResult.warnings.length} warnings
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center justify-end">
                          <button
                            onClick={() => loadHealthReport()}
                            className="text-blue-600 hover:text-blue-700 font-medium"
                          >
                            Refresh Check
                          </button>
                        </div>
                      </div>

                      {validationResult.errors.length > 0 && (
                        <div className="mt-4">
                          <h4 className="font-medium text-gray-900 mb-2">Errors</h4>
                          <div className="space-y-2">
                            {validationResult.errors.map((error: any, index: number) => (
                              <div key={index} className="flex items-start gap-2 p-3 bg-red-50 rounded-lg">
                                <AlertTriangle className="w-4 h-4 text-red-500 mt-0.5" />
                                <div>
                                  <p className="text-sm font-medium text-red-800">{error.message}</p>
                                  <p className="text-xs text-red-600 mt-1">Severity: {error.severity}</p>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {validationResult.warnings.length > 0 && (
                        <div className="mt-4">
                          <h4 className="font-medium text-gray-900 mb-2">Warnings</h4>
                          <div className="space-y-2">
                            {validationResult.warnings.map((warning: any, index: number) => (
                              <div key={index} className="flex items-start gap-2 p-3 bg-yellow-50 rounded-lg">
                                <AlertTriangle className="w-4 h-4 text-yellow-500 mt-0.5" />
                                <div>
                                  <p className="text-sm font-medium text-yellow-800">{warning.message}</p>
                                  {warning.recommendations.length > 0 && (
                                    <ul className="text-xs text-yellow-700 mt-1 list-disc list-inside">
                                      {warning.recommendations.map((rec: string, idx: number) => (
                                        <li key={idx}>{rec}</li>
                                      ))}
                                    </ul>
                                  )}
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {healthReport && (
                    <>
                      <div className="bg-white p-6 rounded-lg border border-gray-200">
                        <h3 className="text-lg font-medium text-gray-900 mb-4">World Statistics</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          <div>
                            <h4 className="font-medium text-gray-700 mb-3">Data Integrity</h4>
                            <div className="space-y-2">
                              <div className="flex justify-between">
                                <span className="text-sm text-gray-600">Elements:</span>
                                <span className="text-sm font-medium">{healthReport.worldState.elements.length}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-sm text-gray-600">Branches:</span>
                                <span className="text-sm font-medium">{healthReport.worldState.branches.length}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-sm text-gray-600">Version:</span>
                                <span className="text-sm font-medium">{healthReport.worldState.metadata.version}</span>
                              </div>
                            </div>
                          </div>
                          <div>
                            <h4 className="font-medium text-gray-700 mb-3">Performance</h4>
                            <div className="space-y-2">
                              <div className="flex justify-between">
                                <span className="text-sm text-gray-600">Compression Ratio:</span>
                                <span className="text-sm font-medium">{(healthReport.compressionRatio || 0).toFixed(2)}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-sm text-gray-600">Last Modified:</span>
                                <span className="text-sm font-medium">{healthReport.worldState.metadata.lastModified.toLocaleDateString()}</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="bg-white p-6 rounded-lg border border-gray-200">
                        <h3 className="text-lg font-medium text-gray-900 mb-4">Available Backups</h3>
                        {healthReport.availableBackups.length > 0 ? (
                          <div className="space-y-3">
                            {healthReport.availableBackups.map((backup: any, index: number) => (
                              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <div>
                                  <p className="font-medium text-gray-900">Backup from {backup.createdAt.toLocaleDateString()}</p>
                                  <p className="text-sm text-gray-500">
                                    {formatFileSize(backup.size)} • {backup.type}
                                  </p>
                                </div>
                                <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                                  Restore
                                </button>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <p className="text-gray-500">No backups available</p>
                        )}
                      </div>
                    </>
                  )}
                </div>
              )}

              {activeTab === 'settings' && (
                <div className="space-y-6">
                  <div className="bg-white p-6 rounded-lg border border-gray-200">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Auto-save Settings</h3>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="font-medium text-gray-900">Enable Auto-save</p>
                          <p className="text-sm text-gray-500">Automatically save changes to prevent data loss</p>
                        </div>
                        <button
                          onClick={() => setAutoSave(!autoSaveEnabled)}
                          className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                            autoSaveEnabled ? 'bg-blue-600' : 'bg-gray-200'
                          }`}
                        >
                          <span
                            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                              autoSaveEnabled ? 'translate-x-6' : 'translate-x-1'
                            }`}
                          />
                        </button>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Auto-save Interval (seconds)
                        </label>
                        <select
                          className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                          onChange={(e) => setAutoSave(autoSaveEnabled, parseInt(e.target.value) * 1000)}
                          defaultValue={30}
                        >
                          <option value={10}>10 seconds</option>
                          <option value={30}>30 seconds</option>
                          <option value={60}>1 minute</option>
                          <option value={300}>5 minutes</option>
                        </select>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white p-6 rounded-lg border border-gray-200">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Advanced Settings</h3>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="font-medium text-gray-900">Enable Compression</p>
                          <p className="text-sm text-gray-500">Compress data to save storage space</p>
                        </div>
                        <button
                          onClick={() => setCompressionEnabled(!compressionEnabled)}
                          className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                            compressionEnabled ? 'bg-blue-600' : 'bg-gray-200'
                          }`}
                        >
                          <span
                            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                              compressionEnabled ? 'translate-x-6' : 'translate-x-1'
                            }`}
                          />
                        </button>
                      </div>
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="font-medium text-gray-900">Enable Sync</p>
                          <p className="text-sm text-gray-500">Synchronize with cloud storage</p>
                        </div>
                        <button
                          onClick={() => setSyncEnabled(!syncEnabled)}
                          className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                            syncEnabled ? 'bg-blue-600' : 'bg-gray-200'
                          }`}
                        >
                          <span
                            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                              syncEnabled ? 'translate-x-6' : 'translate-x-1'
                            }`}
                          />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Create World Dialog */}
      {showCreateDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Create New World</h3>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                const formData = new FormData(e.target as HTMLFormElement);
                handleCreateWorld(
                  formData.get('name') as string,
                  formData.get('description') as string
                );
              }}
            >
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    World Name
                  </label>
                  <input
                    type="text"
                    name="name"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Enter world name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description (Optional)
                  </label>
                  <textarea
                    name="description"
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Describe your world"
                  />
                </div>
              </div>
              <div className="flex justify-end gap-3 mt-6">
                <button
                  type="button"
                  onClick={() => setShowCreateDialog(false)}
                  className="px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                >
                  Create World
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Import Dialog */}
      {showImportDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Import World</h3>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600 mb-2">Select a world file to import</p>
              <input
                type="file"
                accept=".json"
                onChange={(e) => setImportFile(e.target.files?.[0] || null)}
                className="hidden"
                id="import-dialog-file"
              />
              <label
                htmlFor="import-dialog-file"
                className="cursor-pointer bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors"
              >
                Choose File
              </label>
              {importFile && (
                <div className="mt-4">
                  <p className="text-sm text-gray-600">Selected: {importFile.name}</p>
                  <button
                    onClick={handleImport}
                    className="mt-2 bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700 transition-colors"
                  >
                    Import World
                  </button>
                </div>
              )}
            </div>
            <div className="flex justify-end gap-3 mt-6">
              <button
                onClick={() => {
                  setShowImportDialog(false);
                  setImportFile(null);
                }}
                className="px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default WorldDashboard;