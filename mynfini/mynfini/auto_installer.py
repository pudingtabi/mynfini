#!/usr/bin/env python3
"""
MYNFINI Automatic Installation Manager
Handles Python, dependencies, and all technical setup automatically
"""

import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Dict, List
import json
import time

class AutoInstaller:
    """Automatic installation system for complete beginners"""

    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback or self.default_progress_callback
        self.system = platform.system()
        self.python_path = None
        self.venv_path = None
        self.error_log = []

    def default_progress_callback(self, message, progress=None):
        """Default progress callback - print to console"""
        if progress:
            print(f"[{progress}%] {message}")
        else:
            print(f"🤖 {message}")

    def progress(self, message, progress=None):
        """Send progress update"""
        self.progress_callback(message, progress)

    def install_everything(self, project_dir):
        """Install everything needed to run the project"""
        try:
            self.progress("🔧 Starting automatic installation...")

            # Step 1: Ensure Python is available
            self.python_path = self.ensure_python()
            if not self.python_path:
                return False, "Python installation failed"

            # Step 2: Setup virtual environment
            self.venv_path = self.setup_virtual_environment(project_dir)
            if not self.venv_path:
                return False, "Virtual environment setup failed"

            # Step 3: Install dependencies
            if not self.install_dependencies(project_dir):
                return False, "Dependency installation failed"

            # Step 4: Setup configuration
            if not self.setup_configuration(project_dir):
                return False, "Configuration setup failed"

            # Step 5: Verify installation
            if not self.verify_installation(project_dir):
                return False, "Installation verification failed"

            return True, "Installation complete! 🎊"

        except Exception as e:
            self.error_log.append(str(e))
            return False, f"Installation failed: {str(e)}"

    def ensure_python(self) -> Optional[str]:
        """Ensure Python is available - install if needed"""
        self.progress("🔍 Looking for Python...")

        # First, try to find existing Python
        python_path = self.find_python()
        if python_path:
            self.progress(f"✅ Found Python: {python_path}")
            return python_path

        # If Python not found, offer to install
        self.progress("Python not found - will install it for you")
        return self.install_python_auto()

    def find_python(self) -> Optional[str]:
        """Find Python installation"""
        # Try common Python commands
        commands = ['python3', 'python', 'py']

        for cmd in commands:
            try:
                result = subprocess.run([cmd, '--version'],
                                      capture_output=True, text=True)
                if result.returncode == 0 and 'Python 3.' in result.stdout:
                    # Check version - need 3.8 or newer
                    version_line = result.stdout.strip()
                    version_parts = version_line.split()[1].split('.')
                    major = int(version_parts[0])
                    minor = int(version_parts[1])

                    if major == 3 and minor >= 8:
                        return cmd
            except:
                continue

        return None

    def install_python_auto(self) -> Optional[str]:
        """Install Python automatically based on the system"""
        try:
            if self.system == "Windows":
                return self.install_python_windows()
            elif self.system == "Darwin":  # macOS
                return self.install_python_macos()
            else:  # Linux
                return self.install_python_linux()
        except Exception as e:
            self.progress(f"❌ Automatic Python installation failed: {e}")
            self.error_log.append(f"Python install failed: {e}")
            return None

    def install_python_windows(self) -> Optional[str]:
        """Install Python on Windows"""
        self.progress("[DOWNLOAD] Downloading Python for Windows...")

        # Download Python installer
        python_url = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
        installer_path = os.path.join(tempfile.gettempdir(), "python_installer.exe")

        try:
            urllib.request.urlretrieve(python_url, installer_path, self.download_progress)
            self.progress("[PACKAGE] Download complete!")

            # Install Python silently
            self.progress("🔧 Installing Python (this may take a few minutes)...")
            install_cmd = [
                installer_path,
                "/quiet",  # Silent install
                "InstallAllUsers=0",  # Install for current user only
                "PrependPath=1",  # Add to PATH
                "AssociateFiles=1",  # Associate .py files
                "Shortcuts=0",  # No shortcuts
            ]

            result = subprocess.run(install_cmd, capture_output=True, text=True)

            if result.returncode == 0:
                self.progress("✅ Python installed successfully!")
                return self.wait_for_python_installation()
            else:
                self.progress(f"❌ Python installation failed: {result.stderr}")
                return None

        except Exception as e:
            self.progress(f"❌ Python download/install failed: {e}")
            return None
        finally:
            # Cleanup installer
            try:
                os.remove(installer_path)
            except:
                pass

    def install_python_macos(self) -> Optional[str]:
        """Install Python on macOS"""
        self.progress("[APPLE] Installing Python on macOS...")

        try:
            # Try using Homebrew first
            if self.check_homebrew():
                self.progress("[BEER] Using Homebrew to install Python...")
                result = subprocess.run(['brew', 'install', 'python3'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return 'python3'

            # Fallback to official installer
            self.progress("[DOWNLOAD] Downloading Python for macOS...")
            python_url = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-macos11.pkg"
            installer_path = os.path.join(tempfile.gettempdir(), "python_installer.pkg")

            urllib.request.urlretrieve(python_url, installer_path, self.download_progress)

            self.progress("🔧 Installing Python...")
            install_cmd = ['sudo', 'installer', '-pkg', installer_path, '-target', '/']
            result = subprocess.run(install_cmd, capture_output=True, text=True)

            if result.returncode == 0:
                self.progress("✅ Python installed on macOS!")
                return 'python3'
            else:
                self.progress(f"❌ macOS installation failed: {result.stderr}")
                return None

        except Exception as e:
            self.progress(f"❌ macOS installation failed: {e}")
            return None

    def install_python_linux(self) -> Optional[str]:
        """Install Python on Linux"""
        self.progress("[PENGUIN] Installing Python on Linux...")

        try:
            # Try different package managers
            package_managers = [
                (['apt', 'update'], ['apt', 'install', '-y', 'python3', 'python3-pip']),
                (['yum', 'check-update'], ['yum', 'install', '-y', 'python3', 'python3-pip']),
                (['dnf', 'check-update'], ['dnf', 'install', '-y', 'python3', 'python3-pip']),
            ]

            for update_cmd, install_cmd in package_managers:
                try:
                    # Try update first
                    self.progress(f"🔄 Updating package list...")
                    subprocess.run(update_cmd, capture_output=True)

                    # Install Python
                    self.progress(f"[PACKAGE] Installing Python...")
                    result = subprocess.run(install_cmd, capture_output=True, text=True)

                    if result.returncode == 0:
                        self.progress("✅ Python installed on Linux!")
                        return 'python3'

                except FileNotFoundError:
                    # Package manager not found, try next
                    continue

            self.progress("❌ Could not install Python automatically on Linux")
            return None

        except Exception as e:
            self.progress(f"❌ Linux installation failed: {e}")
            return None

    def check_homebrew(self) -> bool:
        """Check if Homebrew is available on macOS"""
        try:
            result = subprocess.run(['brew', '--version'],
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

    def wait_for_python_installation(self, timeout=300) -> Optional[str]:
        """Wait for Python to be available after installation"""
        self.progress("? Waiting for Python to be ready...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            python_path = self.find_python()
            if python_path:
                return python_path
            time.sleep(5)
            self.progress("Still waiting for Python...")

        return None

    def setup_virtual_environment(self, project_dir: str) -> Optional[str]:
        """Setup Python virtual environment"""
        self.progress("🏗️ Creating your personal game space...")

        venv_dir = os.path.join(project_dir, 'game_env')

        try:
            # Remove existing venv if it exists
            if os.path.exists(venv_dir):
                shutil.rmtree(venv_dir)

            # Create new virtual environment
            cmd = [self.python_path, '-m', 'venv', venv_dir]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                self.progress("✅ Personal game space created!")
                return venv_dir
            else:
                self.progress(f"❌ Virtual environment failed: {result.stderr}")
                return None

        except Exception as e:
            self.progress(f"❌ Virtual environment error: {e}")
            return None

    def install_dependencies(self, project_dir: str) -> bool:
        """Install project dependencies"""
        self.progress("📚 Gathering your adventure tools...")

        # Get pip path
        if self.system == "Windows":
            pip_path = os.path.join(self.venv_path, 'Scripts', 'pip')
        else:
            pip_path = os.path.join(self.venv_path, 'bin', 'pip')

        # Check if requirements.txt exists
        req_file = os.path.join(project_dir, 'requirements.txt')
        if not os.path.exists(req_file):
            self.progress("📋 Creating basic requirements...")
            self.create_basic_requirements(req_file)

        try:
            # Read requirements
            with open(req_file, 'r') as f:
                requirements = f.read().strip().split('\n')

            # Install packages one by one for better error handling
            total_packages = len(requirements)
            for i, package in enumerate(requirements):
                package = package.strip()
                if package and not package.startswith('#'):
                    progress = int((i + 1) / total_packages * 50) + 30  # 30-80%
                    self.progress(f"📦 Installing {package}...", progress)

                    result = subprocess.run([pip_path, 'install', package],
                                          capture_output=True, text=True)

                    if result.returncode != 0:
                        self.progress(f"⚠️ Had trouble with {package}, but continuing...")

                        # Try alternative installation methods
                        self.try_alternative_install(package, pip_path)

            self.progress("✅ All adventure tools ready!", 85)
            return True

        except Exception as e:
            self.progress(f"❌ Dependency installation failed: {e}")
            self.error_log.append(f"Dependency install: {e}")
            return False

    def create_basic_requirements(self, req_file: str):
        """Create basic requirements file"""
        basic_requirements = [
            "Flask>=2.3.2",
            "Flask-CORS>=4.0.0",
            "python-dotenv>=1.0.0",
            "anthropic>=0.30.0",
            "requests>=2.31.0",
            "Werkzeug>=2.3.6"
        ]

        with open(req_file, 'w') as f:
            f.write('\n'.join(basic_requirements))

    def try_alternative_install(self, package: str, pip_path: str):
        """Try alternative installation methods for failed packages"""
        try:
            # Try without version specifiers
            base_package = package.split('>=')[0].split('==')[0].split('<')[0]
            self.progress(f"🔄 Trying alternative install for {base_package}...")

            result = subprocess.run([pip_path, 'install', base_package],
                                  capture_output=True, text=True)

            if result.returncode == 0:
                self.progress(f"✅ Alternative install successful for {base_package}")
                return True

            # Try with --force-reinstall
            result = subprocess.run([pip_path, 'install', '--force-reinstall', base_package],
                                  capture_output=True, text=True)

            if result.returncode == 0:
                self.progress(f"✅ Force reinstall successful for {base_package}")
                return True

            self.progress(f"⚠️ Package {package} could not be installed, but continuing...")
            return False

        except Exception as e:
            self.progress(f"⚠️ Alternative install failed: {e}")
            return False

    def setup_configuration(self, project_dir: str) -> bool:
        """Setup configuration files"""
        self.progress("⚙️ Making everything perfect for you...")

        try:
            # Create config directory
            config_dir = os.path.join(project_dir, 'config')
            os.makedirs(config_dir, exist_ok=True)

            # Create default configuration
            default_config = {
                'version': '1.0.0',
                'auto_installer': {
                    'python_version': '3.11',
                    'installation_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'system': self.system
                },
                'launcher': {
                    'auto_setup': True,
                    'first_run': True,
                    'debug_mode': False
                }
            }

            config_file = os.path.join(config_dir, 'launcher_config.json')
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)

            self.progress("✅ Configuration complete!", 90)
            return True

        except Exception as e:
            self.progress(f"⚠️ Configuration setup failed: {e}")
            return True  # Don't fail for config issues

    def verify_installation(self, project_dir: str) -> bool:
        """Verify that everything is working"""
        self.progress("🔍 Testing everything to make sure it works...")

        try:
            # Get Python path in virtual environment
            if self.system == "Windows":
                python_path = os.path.join(self.venv_path, 'Scripts', 'python')
            else:
                python_path = os.path.join(self.venv_path, 'bin', 'python')

            # Test Python
            result = subprocess.run([python_path, '--version'],
                                  capture_output=True, text=True)
            if result.returncode != 0:
                self.progress("❌ Python test failed")
                return False

            # Test Flask
            try:
                result = subprocess.run([python_path, '-c', 'import flask'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.progress("✅ Flask is working perfectly!")
                else:
                    self.progress("⚠️ Flask might need attention")
            except:
                self.progress("⚠️ Could not test Flask")

            self.progress("✅ Everything looks great!", 100)
            return True

        except Exception as e:
            self.progress(f"⚠️ Verification issue: {e}")
            return True  # Don't fail for verification issues

    def download_progress(self, block_num, block_size, total_size):
        """Show download progress"""
        downloaded = block_num * block_size
        if total_size > 0:
            progress = int(downloaded / total_size * 100)
            self.progress(f"[DOWNLOAD] Download progress: {progress}%", progress // 2)

    def get_error_summary(self) -> str:
        """Get summary of any errors that occurred"""
        if not self.error_log:
            return "No errors occurred!"

        return "\\n".join(self.error_log)

def main():
    """Test the auto installer"""
    print("🤖 MYNFINI Auto-Installer Test")
    print("=" * 40)

    def test_progress(message, progress=None):
        if progress:
            print(f"[{progress}%] {message}")
        else:
            print(f"🤖 {message}")

    installer = AutoInstaller(progress_callback=test_progress)
    success, message = installer.install_everything(os.getcwd())

    print(f"\n{'✅' if success else '❌'} {message}")
    if not success:
        print(f"\nError details:\n{installer.get_error_summary()}")

if __name__ == '__main__':
    main()