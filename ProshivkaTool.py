import os
import subprocess
import webbrowser
import time
import threading
from enum import Enum
import sys
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import io
import base64

# Try to import pygame, but handle audio device errors gracefully
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

class MenuAction(Enum):
    RUN_BAT = 1
    SHOW_LINK = 2
    OPEN_URL = 3
    RUN_EXE = 4
    NOT_WORKING = 5
    MUSIC_PLAYER = 6

class MenuItem:
    def __init__(self, name, action=None, action_data=None, submenu=None, path_segment=None):
        self.name = name
        self.action = action
        self.action_data = action_data
        self.submenu = submenu
        self.path_segment = path_segment or name

class MusicPlayer:
    def __init__(self, music_path):
        self.music_path = music_path
        self.playlist = []
        self.current_track = 0
        self.playing = False
        self.paused = False
        self.start_time = 0
        self.current_position = 0
        self.duration = 0
        self.volume = 0.7
        self.audio_available = False
        
        # Initialize pygame mixer with error handling
        if PYGAME_AVAILABLE:
            try:
                # Try to initialize with different audio drivers
                pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
                pygame.mixer.init()
                pygame.mixer.music.set_volume(self.volume)
                self.audio_available = True
                print("Audio initialized successfully")
            except pygame.error as e:
                print(f"Audio not available: {e}")
                self.audio_available = False
        else:
            print("Pygame not available")
            
        self.load_playlist()
        
    def load_playlist(self):
        """Load playlist from music folder"""
        if not os.path.exists(self.music_path):
            os.makedirs(self.music_path)
            print(f"Created music folder: {self.music_path}")
            return
            
        supported_formats = ('.mp3', '.wav', '.ogg', '.flac')
        self.playlist = []
        for file in os.listdir(self.music_path):
            if file.lower().endswith(supported_formats):
                self.playlist.append(os.path.join(self.music_path, file))
        
        print(f"Loaded tracks: {len(self.playlist)}")
    
    def play(self, track_index=None):
        """Play track"""
        if not self.playlist or not self.audio_available:
            return False
            
        if track_index is not None:
            self.current_track = track_index
            
        try:
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play()
            self.playing = True
            self.paused = False
            self.start_time = time.time()
            
            # Get track duration (approximate)
            try:
                sound = pygame.mixer.Sound(self.playlist[self.current_track])
                self.duration = sound.get_length()
            except:
                self.duration = 180  # Default 3 minutes if can't get duration
            return True
        except Exception as e:
            print(f"Playback error: {e}")
            return False
    
    def stop(self):
        """Stop playback"""
        if self.audio_available:
            try:
                pygame.mixer.music.stop()
            except:
                pass
        self.playing = False
        self.paused = False
        self.current_position = 0
    
    def pause(self):
        """Pause playback"""
        if self.playing and not self.paused and self.audio_available:
            try:
                pygame.mixer.music.pause()
                self.paused = True
                self.current_position = time.time() - self.start_time
            except:
                pass
    
    def unpause(self):
        """Resume playback"""
        if self.playing and self.paused and self.audio_available:
            try:
                pygame.mixer.music.unpause()
                self.paused = False
                self.start_time = time.time() - self.current_position
            except:
                pass
    
    def next_track(self):
        """Next track"""
        if not self.playlist:
            return False
            
        self.current_track = (self.current_track + 1) % len(self.playlist)
        return self.play()
    
    def prev_track(self):
        """Previous track"""
        if not self.playlist:
            return False
            
        self.current_track = (self.current_track - 1) % len(self.playlist)
        return self.play()
    
    def set_volume(self, volume):
        """Set volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        if self.audio_available:
            try:
                pygame.mixer.music.set_volume(self.volume)
            except:
                pass
    
    def get_current_time(self):
        """Get current playback position"""
        if not self.playing:
            return 0
            
        if self.paused:
            return self.current_position
            
        return time.time() - self.start_time
    
    def get_progress(self):
        """Get playback progress in percentage"""
        if self.duration <= 0:
            return 0
        return min(100, max(0, int((self.get_current_time() / self.duration) * 100)))
    
    def format_time(self, seconds):
        """Format time as MM:SS"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def get_current_track_name(self):
        """Get current track filename"""
        if not self.playlist:
            return "No tracks found"
        return os.path.basename(self.playlist[self.current_track])
    
    def get_current_status(self):
        """Get playback status"""
        if not self.playlist:
            return "No tracks in playlist", "", "", 0
            
        filename = os.path.basename(self.playlist[self.current_track])
        current_time = self.format_time(self.get_current_time())
        total_time = self.format_time(self.duration)
        progress = self.get_progress()
        
        if not self.audio_available:
            status = "Audio not available"
        else:
            status = "▶ Playing" if self.playing and not self.paused else "⏸ Paused"
        return f"{status}: {filename}", current_time, total_time, progress

class FlashToolGUI:
    def __init__(self):
        self.base_path = "."  # Use current directory for Replit
        self.music_path = os.path.join(self.base_path, "Music")
        self.current_path = self.base_path
        self.menu_stack = []
        self.music_player = MusicPlayer(self.music_path)
        
        # Initialize main window
        self.root = tk.Tk()
        self.root.title("ProshivkaTool v1.3t for Xiaomi 13T")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Setup styles and menu
        self.setup_styles()
        self.setup_menu()
        self.create_gui()
        
        # Start music update thread
        self.update_music_info()
        
    def setup_styles(self):
        """Setup custom styles for ttk widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles for modern look
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'), 
                       foreground='white',
                       background='#1a1a2e')
        
        style.configure('Subtitle.TLabel', 
                       font=('Arial', 12), 
                       foreground='#e0e0e0',
                       background='#1a1a2e')
        
        style.configure('Menu.TButton',
                       font=('Arial', 10),
                       padding=(10, 5))
        
        style.configure('Music.TButton',
                       font=('Arial', 9),
                       padding=(5, 3))
        
        style.configure('Progress.TProgressbar',
                       background='#4facfe',
                       troughcolor='#2e2e3e',
                       borderwidth=0,
                       lightcolor='#4facfe',
                       darkcolor='#4facfe')
    
    def load_background_image(self):
        """Load and resize the background image"""
        try:
            # Load the attached background image
            bg_path = os.path.join("attached_assets", "30389_1754247107832.jpg")
            if os.path.exists(bg_path):
                img = Image.open(bg_path)
                img = img.resize((1000, 700), Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            else:
                # Fallback to generated gradient
                return self.create_background()
        except Exception as e:
            print(f"Error loading background image: {e}")
            return self.create_background()
    
    def create_background(self):
        """Create gradient background as fallback"""
        width, height = 1000, 700
        
        # Create gradient from blue to pink
        img = Image.new('RGB', (width, height))
        pixels = img.load()
        
        for y in range(height):
            for x in range(width):
                # Calculate gradient position (0.0 to 1.0)
                pos_x = x / width
                pos_y = y / height
                
                # Blue to cyan to pink gradient
                r = int(79 + (255 - 79) * (pos_x * 0.5 + pos_y * 0.5))
                g = int(172 + (105 - 172) * pos_y)
                b = int(254 - (254 - 180) * pos_x)
                
                pixels[x, y] = (r, g, b)
        
        return ImageTk.PhotoImage(img)
    
    def create_gui(self):
        """Create the main GUI"""
        # Create background
        self.bg_image = self.load_background_image()
        
        # Main container with background
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Background label
        self.bg_label = tk.Label(self.main_frame, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Content frame with semi-transparent background
        self.content_frame = tk.Frame(self.main_frame, bg='#1a1a2e', relief='raised', bd=2)
        self.content_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
        
        # Title section
        self.title_frame = tk.Frame(self.content_frame, bg='#1a1a2e')
        self.title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.title_label = ttk.Label(self.title_frame, 
                                   text="ProshivkaTool v1.3t for Xiaomi 13T",
                                   style='Title.TLabel')
        self.title_label.pack()
        
        self.subtitle_label = ttk.Label(self.title_frame,
                                      text="Advanced Firmware Flashing Tool with Music Player",
                                      style='Subtitle.TLabel')
        self.subtitle_label.pack()
        
        # Main content area
        self.main_content = tk.Frame(self.content_frame, bg='#1a1a2e')
        self.main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left side - Menu navigation
        self.menu_frame = tk.Frame(self.main_content, bg='#2e2e3e', relief='raised', bd=1)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Navigation header
        self.nav_header = ttk.Label(self.menu_frame, text="Navigation", style='Title.TLabel')
        self.nav_header.pack(pady=10)
        
        # Menu buttons frame
        self.menu_buttons_frame = tk.Frame(self.menu_frame, bg='#2e2e3e')
        self.menu_buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Right side - Music player
        self.music_frame = tk.Frame(self.main_content, bg='#2e2e3e', relief='raised', bd=1)
        self.music_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        self.create_music_player()
        self.create_menu_buttons()
        
        # Status bar
        self.status_frame = tk.Frame(self.content_frame, bg='#1a1a2e')
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=10)
        
        self.status_label = ttk.Label(self.status_frame, 
                                    text="Ready | Select an option from the menu",
                                    style='Subtitle.TLabel')
        self.status_label.pack()
    
    def create_music_player(self):
        """Create music player controls"""
        # Music player header
        music_header = ttk.Label(self.music_frame, text="♫ Music Player", style='Title.TLabel')
        music_header.pack(pady=10)
        
        # Audio status indicator
        if not self.music_player.audio_available:
            self.audio_status = tk.Label(self.music_frame,
                                       text="⚠ Audio not available in this environment",
                                       font=('Arial', 8),
                                       fg='#f39c12',
                                       bg='#2e2e3e',
                                       wraplength=200)
            self.audio_status.pack(pady=5)
        
        # Track info frame
        self.track_info_frame = tk.Frame(self.music_frame, bg='#2e2e3e')
        self.track_info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.track_name_label = ttk.Label(self.track_info_frame,
                                        text="No track loaded",
                                        style='Subtitle.TLabel',
                                        width=25,
                                        anchor='center')
        self.track_name_label.pack()
        
        # Progress frame
        self.progress_frame = tk.Frame(self.music_frame, bg='#2e2e3e')
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Time labels
        self.time_frame = tk.Frame(self.progress_frame, bg='#2e2e3e')
        self.time_frame.pack(fill=tk.X)
        
        self.current_time_label = ttk.Label(self.time_frame, text="00:00", style='Subtitle.TLabel')
        self.current_time_label.pack(side=tk.LEFT)
        
        self.total_time_label = ttk.Label(self.time_frame, text="00:00", style='Subtitle.TLabel')
        self.total_time_label.pack(side=tk.RIGHT)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame,
                                          variable=self.progress_var,
                                          maximum=100,
                                          style='Progress.TProgressbar')
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Control buttons frame
        self.controls_frame = tk.Frame(self.music_frame, bg='#2e2e3e')
        self.controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Previous button
        self.prev_btn = ttk.Button(self.controls_frame,
                                 text="⏮",
                                 command=self.prev_track,
                                 style='Music.TButton',
                                 width=3)
        self.prev_btn.pack(side=tk.LEFT, padx=2)
        
        # Play/Pause button
        self.play_pause_btn = ttk.Button(self.controls_frame,
                                       text="▶",
                                       command=self.toggle_play_pause,
                                       style='Music.TButton',
                                       width=3)
        self.play_pause_btn.pack(side=tk.LEFT, padx=2)
        
        # Next button
        self.next_btn = ttk.Button(self.controls_frame,
                                 text="⏭",
                                 command=self.next_track,
                                 style='Music.TButton',
                                 width=3)
        self.next_btn.pack(side=tk.LEFT, padx=2)
        
        # Stop button
        self.stop_btn = ttk.Button(self.controls_frame,
                                 text="⏹",
                                 command=self.stop_music,
                                 style='Music.TButton',
                                 width=3)
        self.stop_btn.pack(side=tk.LEFT, padx=2)
        
        # Volume frame
        self.volume_frame = tk.Frame(self.music_frame, bg='#2e2e3e')
        self.volume_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(self.volume_frame, text="Volume", style='Subtitle.TLabel').pack()
        
        self.volume_var = tk.DoubleVar(value=self.music_player.volume * 100)
        self.volume_scale = ttk.Scale(self.volume_frame,
                                    from_=0, to=100,
                                    variable=self.volume_var,
                                    command=self.change_volume,
                                    orient=tk.HORIZONTAL)
        self.volume_scale.pack(fill=tk.X, pady=5)
        
        # Playlist management
        self.playlist_frame = tk.Frame(self.music_frame, bg='#2e2e3e')
        self.playlist_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.refresh_playlist_btn = ttk.Button(self.playlist_frame,
                                             text="Refresh Playlist",
                                             command=self.refresh_playlist,
                                             style='Music.TButton')
        self.refresh_playlist_btn.pack(fill=tk.X)
        
        self.playlist_info_label = ttk.Label(self.playlist_frame,
                                           text=f"Tracks: {len(self.music_player.playlist)}",
                                           style='Subtitle.TLabel')
        self.playlist_info_label.pack(pady=5)
    
    def create_menu_buttons(self):
        """Create menu navigation buttons"""
        # Clear existing buttons
        for widget in self.menu_buttons_frame.winfo_children():
            widget.destroy()
        
        # Get current menu
        current_menu = self.get_current_menu()
        
        # Back button if not at root
        if self.menu_stack:
            back_btn = ttk.Button(self.menu_buttons_frame,
                                text="← Back",
                                command=self.go_back,
                                style='Menu.TButton')
            back_btn.pack(fill=tk.X, pady=2)
        
        # Show current path
        path_text = " > ".join([item.name for item in self.menu_stack] + ["Root"])
        path_label = ttk.Label(self.menu_buttons_frame,
                             text=path_text,
                             style='Subtitle.TLabel',
                             wraplength=200)
        path_label.pack(pady=5)
        
        # Menu items
        for item in current_menu:
            btn = ttk.Button(self.menu_buttons_frame,
                           text=item.name,
                           command=lambda i=item: self.handle_menu_item(i),
                           style='Menu.TButton')
            btn.pack(fill=tk.X, pady=2)
    
    def setup_menu(self):
        """Setup the menu structure"""
        self.main_menu = [
            MenuItem("Firmware Flashing", submenu=[
                MenuItem("Original Boot Firmware", submenu=[
                    MenuItem("HyperOS 1", submenu=[
                        MenuItem("HyperOS 1.0.3.0.UMFMIXM", submenu=[
                            MenuItem("Original.bat", MenuAction.RUN_BAT, "firmware/hyperos1/1.0.3.0/original.bat"),
                            MenuItem("Magisk.bat", MenuAction.RUN_BAT, "firmware/hyperos1/1.0.3.0/magisk.bat")
                        ]),
                        MenuItem("HyperOS 1.0.4.0.UMFMIXM", submenu=[
                            MenuItem("Original.bat", MenuAction.RUN_BAT, "firmware/hyperos1/1.0.4.0/original.bat"),
                            MenuItem("Magisk.bat", MenuAction.RUN_BAT, "firmware/hyperos1/1.0.4.0/magisk.bat")
                        ])
                    ]),
                    MenuItem("HyperOS 2", submenu=[
                        MenuItem("HyperOS 2.0.2.0.VMFMIXM", submenu=[
                            MenuItem("Original.bat", MenuAction.RUN_BAT, "firmware/hyperos2/2.0.2.0/original.bat"),
                            MenuItem("Magisk.bat", MenuAction.RUN_BAT, "firmware/hyperos2/2.0.2.0/magisk.bat")
                        ])
                    ])
                ])
            ]),
            MenuItem("Custom Recovery", submenu=[
                MenuItem("OrangeFox.bat", MenuAction.RUN_BAT, "recovery/orangefox.bat"),
                MenuItem("OrangeFox Boot Image", MenuAction.SHOW_LINK, "recovery/orangefox_vendor_boot.img")
            ]),
            MenuItem("Bootloader Unlock", submenu=[
                MenuItem("MiFlash Unlock", MenuAction.RUN_EXE, "unlock/miflash_unlock.exe"),
                MenuItem("Driver Install", MenuAction.RUN_EXE, "unlock/driver_install.exe"),
                MenuItem("Driver Install 64-bit", MenuAction.RUN_EXE, "unlock/driver_install_64.exe")
            ]),
            MenuItem("Official Firmware", submenu=[
                MenuItem("FastbootTool.exe", MenuAction.RUN_EXE, "fastboot/FastbootTool.exe"),
                MenuItem("HyperOS 2.0.103.0 EEA.bat", MenuAction.RUN_BAT, "firmware/hyperos_2.0.103.0_eea.bat")
            ]),
            MenuItem("About", MenuAction.SHOW_LINK, "ProshivkaTool v1.3t for Xiaomi 13T\nCreated for firmware flashing and device management")
        ]
    
    def get_current_menu(self):
        """Get current menu based on navigation stack"""
        current = self.main_menu
        for item in self.menu_stack:
            if item.submenu:
                current = item.submenu
            else:
                break
        return current
    
    def handle_menu_item(self, item):
        """Handle menu item selection"""
        if item.submenu:
            # Navigate to submenu
            self.menu_stack.append(item)
            self.create_menu_buttons()
            self.update_status(f"Navigated to: {item.name}")
        else:
            # Execute action
            self.execute_action(item)
    
    def execute_action(self, item):
        """Execute menu action"""
        try:
            if item.action == MenuAction.RUN_BAT:
                self.update_status(f"Would execute: {item.action_data}")
                messagebox.showinfo("Action", f"Would run batch file:\n{item.action_data}\n\n(Demo mode - files not present)")
            
            elif item.action == MenuAction.RUN_EXE:
                self.update_status(f"Would execute: {item.action_data}")
                messagebox.showinfo("Action", f"Would run executable:\n{item.action_data}\n\n(Demo mode - files not present)")
            
            elif item.action == MenuAction.SHOW_LINK:
                self.update_status(f"Showing info: {item.name}")
                messagebox.showinfo("Information", item.action_data)
            
            elif item.action == MenuAction.OPEN_URL:
                webbrowser.open(item.action_data)
                self.update_status(f"Opened URL: {item.action_data}")
            
            else:
                self.update_status(f"Unknown action for: {item.name}")
                
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Action failed: {str(e)}")
    
    def go_back(self):
        """Go back in menu navigation"""
        if self.menu_stack:
            self.menu_stack.pop()
            self.create_menu_buttons()
            self.update_status("Navigated back")
    
    def update_status(self, message):
        """Update status bar"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_label.config(text=f"{timestamp} | {message}")
    
    # Music player methods
    def toggle_play_pause(self):
        """Toggle play/pause"""
        if not self.music_player.playlist:
            messagebox.showinfo("Music Player", "No tracks in playlist. Add some music files to the Music folder.")
            return
            
        if not self.music_player.audio_available:
            messagebox.showinfo("Music Player", "Audio not available in this environment.")
            return
            
        if self.music_player.playing and not self.music_player.paused:
            self.music_player.pause()
            self.play_pause_btn.config(text="▶")
            self.update_status("Music paused")
        elif self.music_player.playing and self.music_player.paused:
            self.music_player.unpause()
            self.play_pause_btn.config(text="⏸")
            self.update_status("Music resumed")
        else:
            if self.music_player.play():
                self.play_pause_btn.config(text="⏸")
                self.update_status(f"Playing: {self.music_player.get_current_track_name()}")
    
    def stop_music(self):
        """Stop music"""
        self.music_player.stop()
        self.play_pause_btn.config(text="▶")
        self.progress_var.set(0)
        self.update_status("Music stopped")
    
    def next_track(self):
        """Next track"""
        if self.music_player.next_track():
            self.play_pause_btn.config(text="⏸")
            self.update_status(f"Next track: {self.music_player.get_current_track_name()}")
    
    def prev_track(self):
        """Previous track"""
        if self.music_player.prev_track():
            self.play_pause_btn.config(text="⏸")
            self.update_status(f"Previous track: {self.music_player.get_current_track_name()}")
    
    def change_volume(self, value):
        """Change volume"""
        volume = float(value) / 100
        self.music_player.set_volume(volume)
    
    def refresh_playlist(self):
        """Refresh music playlist"""
        self.music_player.load_playlist()
        self.playlist_info_label.config(text=f"Tracks: {len(self.music_player.playlist)}")
        self.update_status(f"Playlist refreshed - {len(self.music_player.playlist)} tracks found")
    
    def update_music_info(self):
        """Update music player information"""
        try:
            # Update track name
            track_name = self.music_player.get_current_track_name()
            if len(track_name) > 25:
                track_name = track_name[:22] + "..."
            self.track_name_label.config(text=track_name)
            
            # Update time and progress
            current_time = self.music_player.format_time(self.music_player.get_current_time())
            total_time = self.music_player.format_time(self.music_player.duration)
            progress = self.music_player.get_progress()
            
            self.current_time_label.config(text=current_time)
            self.total_time_label.config(text=total_time)
            self.progress_var.set(progress)
            
            # Auto-advance to next track
            if (self.music_player.playing and 
                not self.music_player.paused and 
                progress >= 99 and
                self.music_player.audio_available):
                self.next_track()
                
        except Exception as e:
            print(f"Error updating music info: {e}")
        
        # Schedule next update
        self.root.after(1000, self.update_music_info)
    
    def run(self):
        """Run the application"""
        try:
            self.update_status("Application started successfully")
            self.root.mainloop()
        except Exception as e:
            print(f"Error running application: {e}")
            messagebox.showerror("Error", f"Application error: {e}")

if __name__ == "__main__":
    try:
        app = FlashToolGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        # Show a basic error window even if main GUI fails
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Startup Error", f"Failed to start application:\n{e}")