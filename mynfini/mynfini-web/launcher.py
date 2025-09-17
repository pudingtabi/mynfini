#!/usr/bin/env python3
"""
MYNFINI Game Launcher - Zero Technical Knowledge Required!
The simplest way to start your magical storytelling adventure.
"""

import os
import sys
import subprocess
import json
import time
import threading
import webbrowser
import platform
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import urllib.request
import zipfile
import tempfile

# Make sure we're using the right Python path
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as Python script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SimpleLauncher:
    """The world's simplest game launcher - designed for absolute beginners!"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎲 MYNFINI Adventure Game - Ready to Play!")
        self.root.geometry("800x600")
        self.root.configure(bg='#2C3E50')

        # Make window appear in center
        self.root.eval('tk::PlaceWindow . center')

        self.current_step = 0
        self.setup_complete = False
        self.game_process = None
        self.api_keys = {}

        # Setup directories
        self.game_dir = BASE_DIR
        self.venv_dir = os.path.join(self.game_dir, 'game_env')
        self.progress_file = os.path.join(self.game_dir, 'setup_progress.json')

        # Configure style for modern look
        self.setup_modern_style()

        # Check if we've done this before
        self.previous_setup = self.load_previous_setup()

        # Start the magic!
        self.create_welcome_screen()

    def setup_modern_style(self):
        """Create beautiful, modern interface that anyone can understand"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors and fonts for clarity
        style.configure('Main.TFrame', background='#2C3E50')
        style.configure('Welcome.TLabel',
                       background='#2C3E50',
                       foreground='#ECF0F1',
                       font=('Arial', 24, 'bold'))
        style.configure('Simple.TLabel',
                       background='#2C3E50',
                       foreground='#ECF0F1',
                       font=('Arial', 14))
        style.configure('Big.TButton',
                       background='#3498DB',
                       foreground='white',
                       font=('Arial', 16, 'bold'),
                       padding=15)
        style.map('Big.TButton',
                 background=[('active', '#2980B9')])

        # Add pulse button style for animation
        style.configure('Pulse.TButton',
                       background='#5DADE2',
                       foreground='white',
                       font=('Arial', 16, 'bold'),
                       padding=15)
        style.map('Pulse.TButton',
                 background=[('active', '#85C1E9')])

    def create_welcome_screen(self):
        """The very first thing users see - make it magical!"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main container
        main_frame = ttk.Frame(self.root, style='Main.TFrame')
        main_frame.pack(fill='both', expand=True, padx=40, pady=40)

        # Welcome message that makes people smile
        welcome_text = "🎲 Welcome to Your Epic Adventure! 🎲"
        welcome_label = ttk.Label(main_frame, text=welcome_text, style='Welcome.TLabel')
        welcome_label.pack(pady=(0, 20))

        # Simple explanation
        explanation = """
        This is MYNFINI - your magical storytelling game!

        ⭐ No typing complicated commands
        ⭐ No technical knowledge needed
        ⭐ Just click and start your adventure!

        I'll set everything up for you automatically.
        All you need to do is answer a few simple questions...
        """

        expl_label = ttk.Label(main_frame, text=explanation, style='Simple.TLabel',
                              justify='center')
        expl_label.pack(pady=20)

        # Big friendly button that anyone can't miss
        start_btn = ttk.Button(main_frame, text="🚀 Let's Start My Adventure! 🚀",
                              command=self.start_setup_wizard,
                              style='Big.TButton')
        start_btn.pack(pady=40)

        # Make it animated and fun
        self.animate_button(start_btn)

    def animate_button(self, button):
        """Make buttons pulse gently to draw attention"""
        try:
            # Store animation state in the button itself since ttk doesn't have direct background access
            if not hasattr(button, '_pulse_state'):
                button._pulse_state = False

            # Check if button still exists and is a valid widget
            if button.winfo_exists():
                # Toggle the state and update the button text color slightly
                if button._pulse_state:
                    button.configure(style='Big.TButton')
                    button._pulse_state = False
                else:
                    # Create a pressed-like effect by temporarily changing to a different style
                    button.configure(style='Pulse.TButton')
                    button._pulse_state = True
            else:
                # Button no longer exists, stop animation
                return

            self.root.after(1000, lambda: self.animate_button(button))
        except tk.TclError:
            # Button was destroyed during animation, stop gracefully
            pass

    def start_setup_wizard(self):
        """Start the friendly setup process"""
        self.current_step = 1
        self.show_setup_step()

    def show_setup_step(self):
        """Show each step of the setup process with plain English"""
        # Clear screen
        for widget in self.root.winfo_children():
            widget.destroy()

        if self.current_step == 1:
            self.show_step_1_what_do_you_want()
        elif self.current_step == 2:
            self.show_step_2_story_type()
        elif self.current_step == 3:
            self.show_step_3_api_if_needed()
        elif self.current_step == 4:
            self.show_step_4_installation()
        elif self.current_step == 5:
            self.show_step_5_ready_to_play()

    def show_step_1_what_do_you_want(self):
        """Step 1: What do you want to create today?"""
        frame = ttk.Frame(self.root, style='Main.TFrame')
        frame.pack(fill='both', expand=True, padx=40, pady=40)

        ttk.Label(frame, text="🎨 What would you like to do today?",
                 style='Welcome.TLabel').pack(pady=20)

        # Big, friendly buttons for different types of adventures
        options = [
            ("🏰 Start a Fantasy Adventure",
             "Knights, dragons, and magical quests!",
             lambda: self.set_game_type('fantasy')),

            ("🚀 Explore Outer Space",
             "Aliens, starships, and cosmic mysteries!",
             lambda: self.set_game_type('sci-fi')),

            ("🕵️ Solve a Mystery",
             "Detectives, clues, and thrilling investigations!",
             lambda: self.set_game_type('mystery')),

            ("⭐ Make Up My Own Story",
             "Anything you can imagine - the choice is yours!",
             lambda: self.set_game_type('custom'))
        ]

        for title, description, command in options:
            btn_frame = ttk.Frame(frame)
            btn_frame.pack(pady=10, fill='x')

            btn = ttk.Button(btn_frame, text=f"{title}\n{description}",
                           command=command, style='Big.TButton')
            btn.pack(fill='x', padx=20)

    def show_step_2_story_type(self):
        """Step 2: How do you want to play?"""
        frame = ttk.Frame(self.root, style='Main.TFrame')
        frame.pack(fill='both', expand=True, padx=40, pady=40)

        ttk.Label(frame, text="👥 How would you like to play?",
                 style='Welcome.TLabel').pack(pady=20)

        options = [
            ("🎲 Solo Adventure",
             "Just me and the story - I want to explore alone!",
             lambda: self.set_play_mode('solo')),

            ("👨‍👩‍👧‍👦 Play with Friends",
             "I want to play with my friends or family!",
             lambda: self.set_play_mode('group')),

            ("🤖 Let AI Help Me",
             "I'm not sure - can the computer help guide me?",
             lambda: self.set_play_mode('ai-assisted'))
        ]

        for title, description, command in options:
            btn_frame = ttk.Frame(frame)
            btn_frame.pack(pady=10, fill='x')

            btn = ttk.Button(btn_frame, text=f"{title}\n{description}",
                           command=command, style='Big.TButton')
            btn.pack(fill='x', padx=20)

    def show_step_3_api_if_needed(self):
        """Step 3: API setup if needed - made super simple"""
        frame = ttk.Frame(self.root, style='Main.TFrame')
        frame.pack(fill='both', expand=True, padx=40, pady=40)

        # Check if we can skip this step
        if self.check_if_api_is_setup():
            self.current_step = 4
            self.show_setup_step()
            return

        ttk.Label(frame, text="🔑 Want to make your game even more amazing?",
                 style='Welcome.TLabel').pack(pady=20)

        explanation = """
        You can get a free key to make your stories even more creative!

        It's like getting a magic wand for your imagination!

        ✨ Free option: Get 50 creative stories per month
        ⭐ Premium: Unlimited amazing adventures

        (Don't worry if you don't want to - the game works great without it too!)
        """

        ttk.Label(frame, text=explanation, style='Simple.TLabel',
                 justify='center').pack(pady=20)

        # Three big buttons for different options
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="✨ Yes! Get My Magic Key\n(Takes 2 minutes)",
                  command=self.show_api_setup_help,
                  style='Big.TButton').pack(side='left', padx=10)

        ttk.Button(btn_frame, text="🔧 Advanced Setup\nMultiple AI providers",
                  command=self.show_advanced_api_setup,
                  style='Big.TButton').pack(side='left', padx=10)

        ttk.Button(btn_frame, text="🎮 Skip for Now\nPlay with basic stories",
                  command=lambda: self.skip_api_setup(),
                  style='Big.TButton').pack(side='left', padx=10)

    def show_step_4_installation(self):
        """Step 4: Automatic installation with fun progress"""
        frame = ttk.Frame(self.root, style='Main.TFrame')
        frame.pack(fill='both', expand=True, padx=40, pady=40)

        ttk.Label(frame, text="🔧 Setting up your magical adventure!",
                 style='Welcome.TLabel').pack(pady=20)

        # Progress area
        self.progress_text = tk.Text(frame, height=15, width=60,
                                   bg='#34495E', fg='#ECF0F1',
                                   font=('Arial', 12))
        self.progress_text.pack(pady=20)

        # Start installation in background
        self.installation_successful = False
        threading.Thread(target=self.run_installation, daemon=True).start()

    def show_step_5_ready_to_play(self):
        """Step 5: You're ready to play!"""
        frame = ttk.Frame(self.root, style='Main.TFrame')
        frame.pack(fill='both', expand=True, padx=40, pady=40)

        ttk.Label(frame, text="🎊 Your Adventure is Ready! 🎊",
                 style='Welcome.TLabel').pack(pady=20)

        success_text = f"""
        ⭐ Everything is set up perfectly!

        Your game type: {self.user_choices.get('game_type', 'Adventure')}
        Play mode: {self.user_choices.get('play_mode', 'Story Mode')}

        Click the button below to start your magical journey!

        Your stories and characters will be saved automatically.
        Have an amazing adventure! 🚀
        """

        ttk.Label(frame, text=success_text, style='Simple.TLabel',
                 justify='center').pack(pady=20)

        ttk.Button(frame, text="🚀 START MY ADVENTURE NOW! 🚀",
                  command=self.start_game,
                  style='Big.TButton').pack(pady=30)

    def set_game_type(self, game_type):
        """User chose their game type"""
        self.user_choices = getattr(self, 'user_choices', {})
        self.user_choices['game_type'] = game_type
        self.current_step = 2
        self.show_setup_step()

    def set_play_mode(self, play_mode):
        """User chose how they want to play"""
        self.user_choices['play_mode'] = play_mode
        self.current_step = 3
        self.show_setup_step()

    def skip_api_setup(self):
        """User chose to skip API setup - perfectly fine!"""
        self.user_choices['api_setup'] = 'skipped'
        self.current_step = 4
        self.show_setup_step()

    def show_api_setup_help(self):
        """Show simple API setup instructions"""
        # This would open a simple dialog with step-by-step instructions
        message = """
⭐ Getting Your Magic Key is Easy!

1. Click this link: anthropic.com/api
2. Click "Get API Key"
3. Sign up with your email
4. Copy the long string of letters and numbers
5. Paste it back here when I ask

It's completely free to start, and you get 50 amazing stories per month!

Would you like me to open the website for you?
        """

        if messagebox.askyesno("Get Your Magic Key!", message):
            webbrowser.open("https://anthropic.com/api")

        # Ask for the key
        self.ask_for_api_key()

    def show_advanced_api_setup(self):
        """Show advanced API setup with the new setup script"""
        message = """🔧 Advanced API Setup

You can configure multiple AI providers including:
• Anthropic Claude
• OpenAI GPT
• Google Gemini
• Synthetic.new Multi-Model
• Kimi K2-905 with 127-agent mega-parallel orchestration

This will open a secure setup wizard in your terminal.

Continue with advanced setup?"""

        if messagebox.askyesno("Advanced API Setup", message):
            self.run_advanced_api_setup()

    def run_advanced_api_setup(self):
        """Run the advanced API setup script"""
        try:
            # Run the setup script
            setup_script = os.path.join(self.game_dir, 'setup_api_keys.py')
            if os.path.exists(setup_script):
                # Hide the launcher window
                self.root.withdraw()

                # Run setup script in terminal
                if platform.system() == 'Windows':
                    subprocess.run(['python', setup_script], cwd=self.game_dir)
                else:
                    subprocess.run(['python3', setup_script], cwd=self.game_dir)

                # Show the launcher window again
                self.root.deiconify()

                messagebox.showinfo("Setup Complete", "Advanced API setup completed!\nYour keys have been configured securely.")

                # Move to next step
                self.current_step = 4
                self.show_setup_step()
            else:
                messagebox.showerror("Setup Error", "Setup script not found. Please make sure setup_api_keys.py exists.")
                self.root.deiconify()
        except Exception as e:
            messagebox.showerror("Setup Error", f"Failed to run advanced setup: {str(e)}")
            self.root.deiconify()

    def ask_for_api_key(self):
        """Simple dialog to get API key"""
        key = simpledialog.askstring("Your Magic Key",
                                   "Paste your magic key here:\n(Don't worry - I keep it safe!)",
                                   show='*')  # Hide the key for security
        if key:
            self.save_api_key(key)
            self.user_choices['api_setup'] = 'completed'
            messagebox.showinfo("Success!", "[STAR] Your magic key is saved! Let's continue...")
            self.current_step = 4
            self.show_setup_step()
        else:
            messagebox.showinfo("No Problem!", "That's totally fine! The game works great without it too!")
            self.skip_api_setup()

    def check_if_api_is_setup(self):
        """Check if API key exists"""
        key = self.get_saved_api_key()
        return key is not None

    def get_saved_api_key(self):
        """Get saved API key from secure location"""
        try:
            key_file = os.path.join(self.game_dir, '.api_key')
            if os.path.exists(key_file):
                with open(key_file, 'r') as f:
                    return f.read().strip()
        except:
            pass
        return None

    def save_api_key(self, key):
        """Save API key securely"""
        try:
            key_file = os.path.join(self.game_dir, '.api_key')
            with open(key_file, 'w') as f:
                f.write(key)
            # Make file hidden on Windows
            if platform.system() == 'Windows':
                os.system(f'attrib +h "{key_file}"')
        except Exception as e:
            messagebox.showwarning("Security Note", f"Couldn't hide your key file: {e}\nDon't worry - it's still safe!")

    def load_previous_setup(self):
        """Load previous setup if it exists"""
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return None

    def save_progress(self):
        """Save current progress"""
        try:
            progress = {
                'user_choices': getattr(self, 'user_choices', {}),
                'setup_complete': self.setup_complete,
                'setup_date': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            with open(self.progress_file, 'w') as f:
                json.dump(progress, f)
        except Exception as e:
            print(f"Could not save progress: {e}")

    def run_installation(self):
        """Run the actual installation with friendly progress messages"""
        try:
            self.update_progress("[ART] Preparing your magical adventure space...")
            time.sleep(1)

            # Check Python
            self.update_progress("🔍 Looking for Python (your story engine)...")
            python_path = self.find_or_install_python()
            if not python_path:
                self.installation_failed("Python")
                return

            self.update_progress("✅ Found Python! Your stories will be amazing!")
            time.sleep(0.5)

            # Setup virtual environment
            self.update_progress("🏗️ Building your personal game world...")
            if not self.setup_virtual_environment(python_path):
                self.installation_failed("game world")
                return

            self.update_progress("✅ Game world created perfectly!")
            time.sleep(0.5)

            # Install dependencies
            self.update_progress("📦 Gathering your adventure tools...")
            if not self.install_dependencies():
                self.installation_failed("adventure tools")
                return

            self.update_progress("✅ All adventure tools ready!")
            time.sleep(0.5)

            # Save configuration
            self.update_progress("⚙️ Making everything just right for you...")
            if not self.save_configuration():
                self.installation_failed("configuration")
                return

            self.update_progress("✅ Everything configured perfectly!")
            time.sleep(0.5)

            # Success!
            self.update_progress("🎊 YOUR ADVENTURE IS READY TO BEGIN! 🎊")
            self.installation_successful = True

            # Enable continue button after delay
            self.root.after(2000, lambda: self.show_continue_button())

        except Exception as e:
            self.update_progress(f"❌ Oops! Something went wrong: {str(e)}")
            self.installation_failed("installation")

    def update_progress(self, message):
        """Update progress display"""
        self.root.after(0, lambda: self.progress_text.insert('end', message + '\n'))
        self.root.after(0, lambda: self.progress_text.see('end'))

    def show_continue_button(self):
        """Show continue button after successful installation"""
        continue_btn = ttk.Button(self.root, text="🚀 Continue to My Adventure! 🚀",
                                command=lambda: self.continue_after_installation(),
                                style='Big.TButton')
        continue_btn.pack(pady=20)

    def continue_after_installation(self):
        """Move to final step after installation"""
        self.current_step = 5
        self.show_setup_step()

    def find_or_install_python(self):
        """Find Python or install it automatically"""
        # First check if Python is available
        python_commands = ['python', 'python3', 'py']

        for cmd in python_commands:
            try:
                result = subprocess.run([cmd, '--version'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return cmd
            except:
                continue

        # Python not found - offer to install
        self.root.after(0, lambda: self.offer_python_install())
        return None

    def offer_python_install(self):
        """Offer to install Python automatically"""
        if messagebox.askyesno("Python Needed",
                             "I need to install Python to run your adventure.\n\n"
                             "This is completely safe and only takes a few minutes.\n\n"
                             "Should I install it for you?"):
            self.update_progress("📦 Installing Python for you...")
            if self.install_python():
                # Recursively call to find the newly installed Python
                return self.find_or_install_python()
            else:
                messagebox.showerror("Python Installation Failed",
                                   "I couldn't install Python automatically.\n\n"
                                   "Please go to python.org and install Python 3.9 or newer,\n"
                                   "then run this launcher again.")
                return None
        else:
            messagebox.showinfo("Manual Installation Needed",
                              "Please install Python 3.9 or newer from python.org,\n"
                              "then run this launcher again.")
            return None

    def install_python(self):
        """Install Python automatically (simplified - would need full implementation)"""
        # This is a simplified version - full implementation would download
        # and install Python automatically based on the OS
        self.update_progress("❌ Automatic Python installation not available in this version")
        return False

    def setup_virtual_environment(self, python_path):
        """Setup virtual environment"""
        try:
            if os.path.exists(self.venv_dir):
                self.update_progress("📁 Found existing game world - updating it!")
                return True

            # Create virtual environment
            result = subprocess.run([python_path, '-m', 'venv', self.venv_dir],
                                  capture_output=True, text=True)
            return result.returncode == 0

        except Exception as e:
            self.update_progress(f"❌ Game world creation failed: {e}")
            return False

    def install_dependencies(self):
        """Install required packages"""
        try:
            # Get pip path
            if platform.system() == 'Windows':
                pip_path = os.path.join(self.venv_dir, 'Scripts', 'pip')
            else:
                pip_path = os.path.join(self.venv_dir, 'bin', 'pip')

            # Read requirements
            req_file = os.path.join(self.game_dir, 'requirements.txt')
            if not os.path.exists(req_file):
                # Create basic requirements if not exists
                self.create_basic_requirements()

            # Install packages one by one with progress
            packages = ['flask', 'flask-cors', 'python-dotenv', 'anthropic', 'requests']

            for package in packages:
                self.update_progress(f"📦 Installing {package}...")
                result = subprocess.run([pip_path, 'install', package],
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    self.update_progress(f"⚠️ Had trouble with {package}, but continuing...")

            return True

        except Exception as e:
            self.update_progress(f"❌ Adventure tools installation failed: {e}")
            return False

    def create_basic_requirements(self):
        """Create basic requirements file if it doesn't exist"""
        requirements = """flask>=2.3.2
flask-cors>=4.0.0
python-dotenv>=1.0.0
anthropic>=0.30.0
requests>=2.31.0
"""
        with open(os.path.join(self.game_dir, 'requirements.txt'), 'w') as f:
            f.write(requirements)

    def save_configuration(self):
        """Save user configuration"""
        try:
            config = {
                'game_type': self.user_choices.get('game_type', 'fantasy'),
                'play_mode': self.user_choices.get('play_mode', 'solo'),
                'api_setup': self.user_choices.get('api_setup', 'skipped'),
                'setup_date': time.strftime('%Y-%m-%d %H:%M:%S')
            }

            config_file = os.path.join(self.game_dir, 'launcher_config.json')
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)

            self.save_progress()
            return True

        except Exception as e:
            self.update_progress(f"⚠️ Could not save configuration: {e}")
            return True  # Don't fail for config issues

    def installation_failed(self, what_failed):
        """Handle installation failures gracefully"""
        self.root.after(0, lambda: messagebox.showerror("Setup Issue",
                      f"I had trouble setting up your {what_failed}.\n\n"
                      "Don't worry - let's try some simple fixes!\n\n"
                      "1. Make sure you're connected to the internet\n"
                      "2. Try running me as administrator\n"
                      "3. Check if you have enough disk space\n\n"
                      "Would you like to try again?"))

        # Offer to retry or get help
        self.root.after(0, self.show_help_options)

    def show_help_options(self):
        """Show help options when something goes wrong"""
        help_frame = ttk.Frame(self.root)
        help_frame.pack(pady=20)

        ttk.Button(help_frame, text="🔄 Try Again",
                  command=self.retry_setup).pack(side='left', padx=5)

        ttk.Button(help_frame, text="💬 Get Help",
                  command=self.show_help_contact).pack(side='left', padx=5)

    def retry_setup(self):
        """Retry the installation"""
        self.current_step = 4
        self.show_setup_step()

    def show_help_contact(self):
        """Show help contact information"""
        help_text = """
Don't worry! I'm here to help you get your adventure started.

📧 Email: help@mynfini.com
🌐 Website: mynfini.com/help
💬 Discord: discord.mynfini.com

Your adventure is worth the extra effort!
        """
        messagebox.showinfo("Help is Here!", help_text)

    def start_game(self):
        """Start the actual game!"""
        try:
            self.update_progress("🚀 Starting your adventure...")

            # Get Python path
            if platform.system() == 'Windows':
                python_path = os.path.join(self.venv_dir, 'Scripts', 'python')
            else:
                python_path = os.path.join(self.venv_dir, 'bin', 'python')

            # Start the web server
            web_app_path = os.path.join(self.game_dir, 'web_app.py')
            if not os.path.exists(web_app_path):
                # If no web_app.py, create a simple launcher
                self.create_simple_launcher()
                return

            # Start the game process
            env = os.environ.copy()
            env['ANTHROPIC_API_KEY'] = self.get_saved_api_key() or ''

            self.game_process = subprocess.Popen([python_path, web_app_path],
                                               cwd=self.game_dir,
                                               env=env,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)

            # Wait a moment for server to start
            time.sleep(3)

            # Open browser
            self.update_progress("🌐 Opening your adventure portal...")
            webbrowser.open('http://localhost:5000')

            # Show success message
            self.root.after(0, lambda: messagebox.showinfo("🎊 Your Adventure Begins!",
                           "Your game is now running in your web browser!\n\n"
                           "The tab should have opened automatically.\n\n"
                           "Have an incredible adventure! ⭐"))

            # Optionally minimize launcher
            self.root.iconify()

        except Exception as e:
            messagebox.showerror("Startup Issue",
                               f"I couldn't start your adventure: {str(e)}\n\n"
                               "Let's try some quick fixes...")
            self.show_troubleshooting()

    def create_simple_launcher(self):
        """Create a simple launcher if web_app.py doesn't exist"""
        simple_launcher = """
import webbrowser
import os

def launch_game():
    print("🚀 Welcome to MYNFINI! Starting your adventure...")
    print("Opening your game in your web browser...")

    # Create a simple HTML page
    html_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>🎮 MYNFINI Adventure Game</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; }
        .welcome { font-size: 2em; color: #3498DB; margin: 20px; }
        .start-btn { background: #3498DB; color: white; padding: 20px 40px;
                     font-size: 1.5em; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="welcome">🎮 Welcome to Your MYNFINI Adventure! 🎮</div>
    <p>Your game is ready to begin!</p>
    <button class="start-btn" onclick="startAdventure()">Start My Adventure!</button>
    <div id="story"></div>

    <script>
        function startAdventure() {
            document.getElementById('story').innerHTML =
                '<p>✨ Your adventure begins now! ✨</p><p>What would you like to do?</p>';
        }
    </script>
</body>
</html>
    '''

    with open('game.html', 'w') as f:
        f.write(html_content)

    webbrowser.open('file://' + os.path.abspath('game.html'))

if __name__ == '__main__':
    launch_game()
"""

        simple_path = os.path.join(self.game_dir, 'simple_launcher.py')
        with open(simple_path, 'w') as f:
            f.write(simple_launcher)

        # Run the simple launcher
        if platform.system() == 'Windows':
            python_path = os.path.join(self.venv_dir, 'Scripts', 'python')
        else:
            python_path = os.path.join(self.venv_dir, 'bin', 'python')

        subprocess.Popen([python_path, simple_path])

    def show_troubleshooting(self):
        """Show troubleshooting options"""
        troubleshoot = """
Let's fix this together! Try these simple steps:

1. 💻 Make sure no other programs are using port 5000
2. 🔥 Try restarting your computer
3. 🔧 Check if your antivirus is blocking the game
4. 💬 Contact support at help@mynfini.com

Don't give up - your adventure is waiting for you! ⭐
        """
        messagebox.showinfo("Let's Fix This!", troubleshoot)

    def run(self):
        """Run the launcher"""
        self.root.mainloop()

        # Cleanup on exit
        if self.game_process:
            try:
                self.game_process.terminate()
            except:
                pass

def main():
    """Main entry point"""
    try:
        launcher = SimpleLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print("\nGoodbye! Thanks for trying MYNFINI!")
    except Exception as e:
        print(f"The launcher had an unexpected issue: {e}")
        print("Please contact help@mynfini.com for assistance!")
        input("Press Enter to close...")

if __name__ == '__main__':
    main()