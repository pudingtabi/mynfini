#!/usr/bin/env python3
"""
MYNFINI Error Handler - Plain English error messages for complete beginners
Translates technical errors into friendly, actionable advice
"""

import os
import sys
import traceback
import platform
import subprocess
from datetime import datetime
from typing import Dict, Any, Optional, List
import json
import re

class FriendlyErrorHandler:
    """Converts scary technical errors into friendly, helpful messages"""

    def __init__(self):
        self.error_translations = self.load_error_translations()
        self.known_issues = self.load_known_issues()
        self.suggestion_engine = self.create_suggestion_engine()
        self.error_log_file = "friendly_errors.log"

    def load_error_translations(self) -> Dict[str, str]:
        """Load translations for common technical errors"""
        return {
            # Python errors
            "ModuleNotFoundError": "I need some extra tools to run. Let me get them for you!",
            "ImportError": "I'm missing something important. Let's fix that together!",
            "SyntaxError": "There's a small typo in the code. Don't worry, this shouldn't happen!",
            "IndentationError": "The code formatting is off. Easy to fix!",
            "NameError": "Something isn't named correctly. Simple fix coming up!",
            "TypeError": "I'm expecting something different. Let me adjust that!",
            "KeyError": "I can't find that specific thing. Let me check what happened!",
            "IndexError": "I'm looking for something that isn't there. No big deal!",
            "AttributeError": "I'm trying to use something that doesn't exist. I'll fix it!",

            # Network/Internet errors
            "ConnectionError": "I can't connect to the internet right now.",
            "TimeoutError": "The connection is taking too long. Let me try again!",
            "SSLError": "There's a security issue with the connection.",
            "URLError": "I can't reach the website. Let's check your internet!",

            # File system errors
            "FileNotFoundError": "I can't find that file. Let me create it for you!",
            "PermissionError": "I need permission to do that. Let's fix the permissions!",
            "IsADirectoryError": "That's a folder, not a file. Easy mix-up!",
            "NotADirectoryError": "That's not a folder. Simple mistake!",

            # API/Service errors
            "401": "Your API key needs to be set up. Let's do that together!",
            "403": "I don't have permission to access that service.",
            "404": "I can't find what I'm looking for on the server.",
            "429": "The service is busy. I'll wait a moment and try again!",
            "500": "The service is having issues. Let me try a different approach!",
            "503": "The service is temporarily unavailable. I'll retry!",
        }

    def load_known_issues(self) -> Dict[str, Dict[str, Any]]:
        """Load known issues and their solutions"""
        return {
            # Python not found
            "python_not_found": {
                "symptoms": ["command not found", "python", "is not recognized", "'python' is not"],
                "friendly_message": "I can't find Python on your computer!",
                "solution_steps": [
                    "Python is like the engine that makes the game work",
                    "Let me install it for you automatically",
                    "Or you can go to python.org and install Python 3.9 or newer",
                    "Then run me again!"
                ],
                "auto_fix": True,
                "priority": 1
            },

            # Permission issues
            "permission_denied": {
                "symptoms": ["Permission denied", "Access is denied", "permission"],
                "friendly_message": "I need permission to set up your game!",
                "solution_steps": [
                    "Right-click on the launcher and select 'Run as administrator'",
                    "Or try running from a different folder",
                    "Don't worry - this is normal and safe!"
                ],
                "auto_fix": False,
                "priority": 2
            },

            # Network issues
            "network_issue": {
                "symptoms": ["Connection refused", "Timeout", "Network", "internet"],
                "friendly_message": "I'm having trouble connecting to the internet!",
                "solution_steps": [
                    "Check if your internet is working",
                    "Try reloading the program",
                    "The game works offline too - let me set that up for you!"
                ],
                "auto_fix": True,
                "priority": 3
            },

            # Antivirus blocking
            "antivirus_blocking": {
                "symptoms": ["quarantine", "blocked", "antivirus", "virus"],
                "friendly_message": "Your antivirus might be protecting me too much!",
                "solution_steps": [
                    "This is totally normal for new programs",
                    "Add this folder to your antivirus exceptions",
                    "Or temporarily disable antivirus during setup",
                    "The game is 100% safe!"
                ],
                "auto_fix": False,
                "priority": 4
            },

            # Disk space
            "disk_space": {
                "symptoms": ["No space left", "disk full", "insufficient space"],
                "friendly_message": "Your computer needs a bit more space!",
                "solution_steps": [
                    "The game needs about 500MB of free space",
                    "Try deleting some files or emptying the recycle bin",
                    "Then run me again!"
                ],
                "auto_fix": False,
                "priority": 5
            },

            # Corrupted download
            "corrupted_download": {
                "symptoms": ["corrupt", "invalid", "checksum", "hash"],
                "friendly_message": "Something got mixed up during download!",
                "solution_steps": [
                    "Let's download everything again",
                    "Make sure your internet is stable",
                    "I'll use an extra-safe download method!"
                ],
                "auto_fix": True,
                "priority": 6
            }
        }

    def create_suggestion_engine(self) -> Dict[str, Any]:
        """Create engine for suggesting fixes"""
        return {
            "easy_fixes": [
                "Restart your computer - this fixes 80% of issues!",
                "Right-click and select 'Run as administrator'",
                "Move the game to your Documents folder",
                "Temporarily disable antivirus during setup",
                "Check if you have enough free disk space"
            ],
            "windows_specific": [
                "Try Windows compatibility mode",
                "Run Windows Update",
                "Install Visual C++ Redistributables",
                "Check Windows Defender exclusions"
            ],
            "mac_specific": [
                "Install Xcode Command Line Tools",
                "Allow apps from anywhere in Security settings",
                "Clear quarantine attributes: xattr -cr .",
                "Install Homebrew for easier dependency management"
            ],
            "linux_specific": [
                "Install build-essential package",
                "Check your package manager for updates",
                "Install python3-dev package",
                "Use sudo for permission issues"
            ]
        }

    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """Handle an error and return friendly information"""
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "original_error": str(error),
            "error_type": type(error).__name__,
            "context": context,
            "system_info": self.get_system_info(),
            "traceback": traceback.format_exc() if context else "",
            "friendly_message": "",
            "suggested_solutions": [],
            "auto_fix_possible": False,
            "urgency_level": "low"
        }

        try:
            # Classify the error
            error_classification = self.classify_error(error, context)
            error_info.update(error_classification)

            # Log the error
            self.log_error(error_info)

            return error_info

        except Exception as classification_error:
            # If classification fails, return a generic message
            error_info["friendly_message"] = "Something went wrong, but don't worry!"
            error_info["suggested_solutions"] = [
                "Try restarting the program",
                "Check your internet connection",
                "Run me as administrator",
                "Contact support if the issue persists"
            ]
            error_info["urgency_level"] = "medium"
            return error_info

    def classify_error(self, error: Exception, context: str) -> Dict[str, Any]:
        """Classify the error and find appropriate solutions"""
        error_str = str(error).lower()
        error_type = type(error).__name__

        # Check for known issues first
        for issue_name, issue_data in self.known_issues.items():
            if any(symptom.lower() in error_str for symptom in issue_data["symptoms"]):
                return {
                    "friendly_message": issue_data["friendly_message"],
                    "suggested_solutions": issue_data["solution_steps"],
                    "auto_fix_possible": issue_data["auto_fix"],
                    "urgency_level": self.get_urgency_level(issue_data["priority"]),
                    "issue_type": issue_name
                }

        # Check for common error types
        if error_type in self.error_translations:
            return self.handle_common_error_type(error_type, error_str, context)

        # Analyze the error message
        return self.analyze_error_message(error_str, context)

    def handle_common_error_type(self, error_type: str, error_str: str, context: str) -> Dict[str, Any]:
        """Handle common Python error types"""
        base_message = self.error_translations[error_type]

        # Add more specific information based on error content
        if error_type == "ModuleNotFoundError":
            module_match = re.search(r"No module named '?(\w+)'?", error_str)
            if module_match:
                module_name = module_match.group(1)
                return {
                    "friendly_message": f"I'm missing the '{module_name}' tool!",
                    "suggested_solutions": [
                        "I'll install it for you automatically",
                        "This is totally normal on first run",
                        "Let me fix this right now!"
                    ],
                    "auto_fix_possible": True,
                    "urgency_level": "low",
                    "issue_type": "missing_module"
                }

        elif error_type == "ConnectionError" or "timeout" in error_str.lower():
            return {
                "friendly_message": base_message,
                "suggested_solutions": [
                    "Check if your WiFi is working",
                    "Try refreshing the page",
                    "The game works offline too!",
                    "Let me switch to offline mode for you"
                ],
                "auto_fix_possible": True,
                "urgency_level": "medium",
                "issue_type": "network_issue"
            }

        elif "permission" in error_str.lower() or "access" in error_str.lower():
            return {
                "friendly_message": "I need permission to do that!",
                "suggested_solutions": [
                    "Right-click and select 'Run as administrator'",
                    "Make sure you have permission to install programs",
                    "Try putting the game in your Documents folder"
                ],
                "auto_fix_possible": False,
                "urgency_level": "medium",
                "issue_type": "permission_issue"
            }

        return {
            "friendly_message": base_message,
            "suggested_solutions": self.get_generic_solutions(),
            "auto_fix_possible": False,
            "urgency_level": "low",
            "issue_type": "unknown_issue"
        }

    def analyze_error_message(self, error_str: str, context: str) -> Dict[str, Any]:
        """Analyze error message for keywords"""
        error_keywords = {
            "memory": ("I need more memory to work with!", "memory_issue"),
            "disk": ("Your computer needs more disk space!", "disk_space"),
            "firewall": ("Your firewall might be blocking me!", "firewall_issue"),
            "proxy": ("I can't connect through your proxy settings!", "proxy_issue"),
            "certificate": ("There's a security certificate issue!", "certificate_issue"),
            "unicode": ("There's a text encoding issue! I'll fix it." , "encoding_issue"),
            "encoding": ("There's a text encoding issue! I'll fix it.", "encoding_issue")
        }

        for keyword, (message, issue_type) in error_keywords.items():
            if keyword in error_str.lower():
                return {
                    "friendly_message": message,
                    "suggested_solutions": self.get_solutions_for_issue(issue_type),
                    "auto_fix_possible": True,
                    "urgency_level": "medium",
                    "issue_type": issue_type
                }

        # Generic fallback
        return {
            "friendly_message": "Something unexpected happened, but let's fix it!",
            "suggested_solutions": self.get_generic_solutions(),
            "auto_fix_possible": True,
            "urgency_level": "low",
            "issue_type": "unexpected_error"
        }

    def get_solutions_for_issue(self, issue_type: str) -> List[str]:
        """Get specific solutions for issue type"""
        solutions = {
            "memory_issue": [
                "Close some programs to free up memory",
                "Restart your computer to clear memory",
                "The game doesn't need much memory, this should fix it!"
            ],
            "disk_space": [
                "Free up some disk space (the game needs about 500MB)",
                "Empty your recycle bin",
                "Delete some old files or photos"
            ],
            "firewall_issue": [
                "Add this program to your firewall exceptions",
                "Temporarily disable your firewall",
                "Make sure your antivirus isn't blocking me"
            ],
            "proxy_issue": [
                "Check your internet connection settings",
                "Try using a different network",
                "The game works offline too!"
            ],
            "certificate_issue": [
                "Check your computer's date and time settings",
                "Try again in a few minutes",
                "Let me use a different connection method"
            ],
            "encoding_issue": [
                "I'll automatically fix the text settings",
                "This is a common issue - I've got you covered!",
                "The game will work perfectly in any language"
            ]
        }

        return solutions.get(issue_type, self.get_generic_solutions())

    def get_generic_solutions(self) -> List[str]:
        """Get generic solutions that work for most issues"""
        solutions = [
            "🔄 Restart your computer (this fixes most issues!)",
            "📁 Move the game to your Documents folder",
            "🔒 Right-click and select 'Run as administrator'",
            "💾 Check you have enough disk space (500MB needed)",
            "🌐 Make sure your internet is working"
        ]

        # Add platform-specific solutions
        system = platform.system()
        if system == "Windows":
            solutions.extend([
                "🪟 Try Windows compatibility mode",
                "🛡️ Check Windows Defender settings"
            ])
        elif system == "Darwin":  # macOS
            solutions.extend([
                "🍎 Install Xcode Command Line Tools",
                "🔐 Allow apps from anywhere in Security settings"
            ])
        elif system == "Linux":
            solutions.extend([
                "🐧 Install python3-dev package",
                "🔧 Use your package manager to install dependencies"
            ])

        return solutions

    def get_urgency_level(self, priority: int) -> str:
        """Convert priority to urgency level"""
        if priority <= 2:
            return "high"
        elif priority <= 5:
            return "medium"
        else:
            return "low"

    def get_system_info(self) -> Dict[str, str]:
        """Get useful system information"""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": platform.python_version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "total_ram": self.get_total_ram(),
            "available_space": self.get_available_space()
        }

    def get_total_ram(self) -> str:
        """Get total system RAM"""
        try:
            if platform.system() == "Windows":
                import ctypes
                kernel32 = ctypes.windll.kernel32
                c_ulonglong = ctypes.c_ulonglong
                kernel32.GetPhysicallyInstalledSystemMemory.restype = ctypes.c_ulonglong
                kernel32.GetPhysicallyInstalledSystemMemory.argtypes = [ctypes.POINTER(c_ulonglong)]
                memory = c_ulonglong()
                kernel32.GetPhysicallyInstalledSystemMemory(ctypes.byref(memory))
                return f"{memory.value / (1024**2):.1f} GB"
            else:
                # For Unix-like systems
                result = subprocess.run(['grep', 'MemTotal', '/proc/meminfo'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    mem_kb = int(result.stdout.split()[1])
                    return f"{mem_kb / (1024**2):.1f} GB"
        except:
            pass
        return "Unknown"

    def get_available_space(self) -> str:
        """Get available disk space"""
        try:
            if platform.system() == "Windows":
                import ctypes
                free_bytes = ctypes.c_ulonglong(0)
                total_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                    ctypes.c_wchar_p('C:\\'),
                    ctypes.pointer(free_bytes),
                    ctypes.pointer(total_bytes),
                    None
                )
                return f"{free_bytes.value / (1024**3):.1f} GB"
            else:
                result = subprocess.run(['df', '-h', '.'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\\n')
                    if len(lines) > 1:
                        parts = lines[1].split()
                        if len(parts) >= 4:
                            return parts[3]
        except:
            pass
        return "Unknown"

    def log_error(self, error_info: Dict[str, Any]):
        """Log error for debugging"""
        try:
            log_entry = {
                "timestamp": error_info["timestamp"],
                "issue_type": error_info.get("issue_type", "unknown"),
                "friendly_message": error_info["friendly_message"],
                "urgency": error_info["urgency_level"],
                "system_info": error_info["system_info"]
            }

            # Append to log file
            log_path = self.error_log_file
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\\n')

        except Exception as e:
            # Don't let logging errors cause more errors
            print(f"Could not log error: {e}")

    def create_auto_fix_script(self, error_info: Dict[str, Any]) -> str:
        """Create a script to automatically fix common issues"""
        issue_type = error_info.get("issue_type", "unknown")
        system = error_info["system_info"]["os"]

        script_commands = []

        if issue_type == "missing_module":
            script_commands.extend([
                "echo Installing missing Python packages...",
                "python -m pip install --upgrade pip",
                "python -m pip install flask flask-cors anthropic requests"
            ])

        elif issue_type == "permission_issue":
            if system == "Windows":
                script_commands.extend([
                    "echo Taking ownership of game folder...",
                    "icacls . /grant %USERNAME%:F /T",
                    "echo Folder permissions fixed!"
                ])
            else:
                script_commands.extend([
                    "echo Setting proper permissions...",
                    "sudo chown -R $USER:$USER .",
                    "chmod -R 755 ."
                ])

        elif issue_type == "network_issue":
            script_commands.extend([
                "echo Testing network connection...",
                "ping -c 1 google.com || echo Network appears to be down",
                "echo Trying offline mode..."
            ])

        return "\\n".join(script_commands)

    def format_error_report(self, error_info: Dict[str, Any], include_tech_details: bool = False) -> str:
        """Format a user-friendly error report"""
        report = []

        # Header
        report.append("🎲 Oops! Something went wrong with your adventure game!")
        report.append("=" * 60)
        report.append("")

        # Friendly message
        report.append(f"📋 What happened: {error_info['friendly_message']}")
        report.append("")

        # Solutions
        if error_info['suggested_solutions']:
            report.append("🔧 Let's fix this together:")
            for i, solution in enumerate(error_info['suggested_solutions'], 1):
                report.append(f"{i}. {solution}")
            report.append("")

        # Auto-fix info
        if error_info.get('auto_fix_possible', False):
            report.append("🤖 I can automatically fix this for you!")
            report.append("Would you like me to try the automatic fix?")
            report.append("")

        # Urgency indicator
        urgency = error_info.get('urgency_level', 'low')
        urgency_emojis = {'high': '🚨', 'medium': '⚠️', 'low': 'ℹ️'}
        report.append(f"{urgency_emojis.get(urgency, 'ℹ️')} Urgency level: {urgency.upper()}")
        report.append("")

        if include_tech_details:
            report.append("🛠️ Technical details (for support):")
            report.append(f"Error type: {error_info['error_type']}")
            report.append(f"Timestamp: {error_info['timestamp']}")
            if error_info.get('issue_type'):
                report.append(f"Issue type: {error_info['issue_type']}")
            report.append("")

        # Footer
        report.append("🌟 Don't give up - your adventure is waiting for you!")
        report.append("💬 Need more help? Contact support at help@mynfini.com")

        return "\\n".join(report)

def main():
    """Test the error handler"""
    print("🧪 Testing MYNFINI Error Handler")
    print("=" * 40)

    handler = FriendlyErrorHandler()

    # Test with various errors
    test_errors = [
        ModuleNotFoundError("No module named 'flask'"),
        PermissionError("Access denied"),
        ConnectionError("Connection refused"),
        FileNotFoundError("Config file not found"),
        ValueError("Invalid configuration")
    ]

    for error in test_errors:
        print(f"\\n❌ Testing with {type(error).__name__}:")
        error_info = handler.handle_error(error, "Launcher test")
        print(handler.format_error_report(error_info))
        print("-" * 30)

if __name__ == '__main__':
    main()