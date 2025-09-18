/**
 * Cross-Device Save System for MYNFINI
 * Handles game state export/import functionality
 */

class SaveTransferManager {
    constructor() {
        this.apiBase = '/api/save';
    }

    /**
     * Export game state as JSON file download
     */
    async exportAsFile() {
        try {
            const response = await fetch(`${this.apiBase}/export`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error || 'Export failed');
            }

            // Create and trigger file download
            const blob = new Blob([result.data], { type: 'application/json' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = result.filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            return result;
        } catch (error) {
            console.error('Export failed:', error);
            throw error;
        }
    }

    /**
     * Generate QR code for game state transfer
     */
    async generateQRCode() {
        try {
            const response = await fetch(`${this.apiBase}/export/qr`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error || 'QR generation failed');
            }

            return result.qr_image;
        } catch (error) {
            console.error('QR generation failed:', error);
            throw error;
        }
    }

    /**
     * Get base64 save data for copy/paste transfer
     */
    async getBase64Data() {
        try {
            const response = await fetch(`${this.apiBase}/base64`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error || 'Base64 generation failed');
            }

            return result.base64;
        } catch (error) {
            console.error('Base64 generation failed:', error);
            throw error;
        }
    }

    /**
     * Import game state from JSON data
     */
    async importFromJSON(jsonData) {
        try {
            const response = await fetch(`${this.apiBase}/import`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    data: jsonData,
                    format: 'json'
                })
            });

            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error || 'Import failed');
            }

            return result;
        } catch (error) {
            console.error('Import failed:', error);
            throw error;
        }
    }

    /**
     * Import game state from base64 data
     */
    async importFromBase64(base64Data) {
        try {
            const response = await fetch(`${this.apiBase}/import`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    data: base64Data,
                    format: 'base64'
                })
            });

            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error || 'Import failed');
            }

            return result;
        } catch (error) {
            console.error('Import failed:', error);
            throw error;
        }
    }

    /**
     * Show file picker and read selected file
     */
    async pickAndReadFile() {
        return new Promise((resolve, reject) => {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.json';

            input.onchange = async (e) => {
                const file = e.target.files[0];
                if (!file) {
                    reject(new Error('No file selected'));
                    return;
                }

                try {
                    const text = await file.text();
                    resolve(text);
                } catch (error) {
                    reject(error);
                }
            };

            input.click();
        });
    }

    /**
     * Show QR code modal
     */
    async showQRModal() {
        try {
            const qrImage = await this.generateQRCode();

            // Create modal
            const modal = document.createElement('div');
            modal.className = 'save-transfer-modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <h3>Scan to Transfer Save</h3>
                    <img src="${qrImage}" alt="QR Code" class="qr-code-image">
                    <p>Scan this QR code with your other device to continue playing</p>
                    <button onclick="this.parentElement.parentElement.remove()">Close</button>
                </div>
            `;

            document.body.appendChild(modal);
        } catch (error) {
            alert('Failed to generate QR code: ' + error.message);
        }
    }

    /**
     * Show base64 data modal for copy/paste
     */
    async showBase64Modal() {
        try {
            const base64Data = await this.getBase64Data();

            // Create modal
            const modal = document.createElement('div');
            modal.className = 'save-transfer-modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <h3>Copy Save Data</h3>
                    <textarea readonly class="base64-textarea">${base64Data}</textarea>
                    <p>Copy this text and paste it on your other device to continue playing</p>
                    <button onclick="this.parentElement.parentElement.remove()">Close</button>
                </div>
            `;

            document.body.appendChild(modal);

            // Auto-select text for easy copying
            const textarea = modal.querySelector('textarea');
            textarea.select();
        } catch (error) {
            alert('Failed to generate save data: ' + error.message);
        }
    }

    /**
     * Show import modal with paste option
     */
    async showImportModal() {
        const modal = document.createElement('div');
        modal.className = 'save-transfer-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h3>Import Game Save</h3>
                <div class="import-options">
                    <button id="import-file-btn" class="import-btn">Choose File</button>
                    <button id="import-paste-btn" class="import-btn">Paste Base64</button>
                </div>
                <textarea id="import-textarea" class="import-textarea" placeholder="Paste base64 data here..."></textarea>
                <div class="import-buttons">
                    <button id="import-confirm-btn">Import</button>
                    <button onclick="this.parentElement.parentElement.parentElement.remove()">Cancel</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // File import
        modal.querySelector('#import-file-btn').onclick = async () => {
            try {
                const fileData = await this.pickAndReadFile();
                await this.importFromJSON(fileData);
                modal.remove();
                alert('Game save imported successfully! Refresh to continue playing.');
            } catch (error) {
                alert('Import failed: ' + error.message);
            }
        };

        // Paste import
        modal.querySelector('#import-paste-btn').onclick = () => {
            const textarea = modal.querySelector('#import-textarea');
            textarea.style.display = 'block';
            textarea.focus();
        };

        // Confirm import
        modal.querySelector('#import-confirm-btn').onclick = async () => {
            const textarea = modal.querySelector('#import-textarea');
            const data = textarea.value.trim();

            if (!data) {
                alert('Please paste save data or choose a file');
                return;
            }

            try {
                // Try JSON first, then base64
                let result;
                try {
                    JSON.parse(data);
                    result = await this.importFromJSON(data);
                } catch {
                    result = await this.importFromBase64(data);
                }

                modal.remove();
                alert('Game save imported successfully! Refresh to continue playing.');

                // Refresh page to load imported state
                location.reload();
            } catch (error) {
                alert('Import failed: ' + error.message);
            }
        };
    }
}

// Initialize save transfer manager when DOM is ready
let saveTransferManager;
document.addEventListener('DOMContentLoaded', () => {
    saveTransferManager = new SaveTransferManager();
});

// CSS for save transfer modals
const saveTransferStyles = `
.save-transfer-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10000;
}

.save-transfer-modal .modal-content {
    background-color: #1a1a2e;
    color: #eee;
    padding: 30px;
    border-radius: 10px;
    text-align: center;
    max-width: 500px;
    width: 90%;
}

.save-transfer-modal h3 {
    color: #4fbdba;
    margin-bottom: 20px;
}

.save-transfer-modal .qr-code-image {
    max-width: 300px;
    margin: 20px auto;
    display: block;
}

.save-transfer-modal .base64-textarea,
.save-transfer-modal .import-textarea {
    width: 100%;
    min-height: 150px;
    background-color: #0f3460;
    color: #eee;
    border: 1px solid #4fbdba;
    padding: 10px;
    margin: 20px 0;
    font-family: monospace;
    font-size: 12px;
    resize: vertical;
}

.save-transfer-modal button {
    background-color: #4fbdba;
    color: #1a1a2e;
    border: none;
    padding: 10px 20px;
    margin: 5px;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
}

.save-transfer-modal button:hover {
    background-color: #7ec8e3;
}

.save-transfer-modal .import-options {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 20px;
}

.save-transfer-modal .import-btn {
    background-color: #16213e;
    border: 2px solid #4fbdba;
    color: #4fbdba;
}

.save-transfer-modal .import-textarea {
    display: none;
}

@media (max-width: 768px) {
    .save-transfer-modal .modal-content {
        padding: 20px;
        margin: 20px;
    }

    .save-transfer-modal .qr-code-image {
        max-width: 250px;
    }
}
`;

// Inject styles if not already present
if (!document.getElementById('save-transfer-styles')) {
    const styleElement = document.createElement('style');
    styleElement.id = 'save-transfer-styles';
    styleElement.textContent = saveTransferStyles;
    document.head.appendChild(styleElement);
}