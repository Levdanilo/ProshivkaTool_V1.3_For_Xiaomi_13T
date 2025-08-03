import os
import subprocess
import webbrowser
import time
import pygame
import threading
from enum import Enum
import sys
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import io
import base64

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
        self.load_playlist()
        
        # Initialize pygame mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.music.set_volume(self.volume)
        
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
        
        if self.playlist:
            print(f"Loaded tracks: {len(self.playlist)}")
    
    def play(self, track_index=None):
        """Play track"""
        if not self.playlist:
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
        pygame.mixer.music.stop()
        self.playing = False
        self.paused = False
        self.current_position = 0
    
    def pause(self):
        """Pause playback"""
        if self.playing and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
            self.current_position = time.time() - self.start_time
    
    def unpause(self):
        """Resume playback"""
        if self.playing and self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            self.start_time = time.time() - self.current_position
    
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
        pygame.mixer.music.set_volume(self.volume)
    
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
            return "No tracks"
        return os.path.basename(self.playlist[self.current_track])
    
    def get_current_status(self):
        """Get playback status"""
        if not self.playlist:
            return "No tracks in playlist", "", "", 0
            
        filename = os.path.basename(self.playlist[self.current_track])
        current_time = self.format_time(self.get_current_time())
        total_time = self.format_time(self.duration)
        progress = self.get_progress()
        
        status = "▶ Playing" if self.playing and not self.paused else "⏸ Paused"
        return f"{status}: {filename}", current_time, total_time, progress

class FlashToolGUI:
    def __init__(self):
        self.base_path = r"C:\ProshivkaTool"
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
    
    def create_background(self):
        """Create gradient background"""
        # Create a gradient background programmatically
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
        self.bg_image = self.create_background()
        
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
        music_header = ttk.Label(self.music_frame, text="Music Player", style='Title.TLabel')
        music_header.pack(pady=10)
        
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
            
            # Separator
            ttk.Separator(self.menu_buttons_frame, orient='horizontal').pack(fill=tk.X, pady=5)
        
        # Menu items
        for item in current_menu:
            btn = ttk.Button(self.menu_buttons_frame,
                           text=item.name,
                           command=lambda i=item: self.handle_menu_action(i),
                           style='Menu.TButton')
            btn.pack(fill=tk.X, pady=2)
    
    def get_current_menu(self):
        """Get current menu items based on navigation stack"""
        current_menu = self.main_menu
        
        for menu_name in self.menu_stack:
            for item in current_menu:
                if item.name == menu_name and item.submenu:
                    current_menu = item.submenu
                    break
        
        return current_menu
    
    def handle_menu_action(self, item):
        """Handle menu item selection"""
        if item.submenu:
            # Navigate to submenu
            self.menu_stack.append(item.name)
            self.create_menu_buttons()
            self.update_status(f"Navigated to: {item.name}")
        elif item.action:
            # Execute action
            self.execute_action(item)
    
    def go_back(self):
        """Go back to previous menu"""
        if self.menu_stack:
            self.menu_stack.pop()
            self.create_menu_buttons()
            self.update_status("Navigated back")
    
    def execute_action(self, item):
        """Execute menu action"""
        try:
            if item.action == MenuAction.RUN_BAT:
                self.run_batch_file(item.action_data)
            elif item.action == MenuAction.RUN_EXE:
                self.run_executable(item.action_data)
            elif item.action == MenuAction.OPEN_URL:
                webbrowser.open(item.action_data)
                self.update_status(f"Opened URL: {item.action_data}")
            elif item.action == MenuAction.SHOW_LINK:
                messagebox.showinfo("Link", f"URL: {item.action_data}")
            elif item.action == MenuAction.NOT_WORKING:
                messagebox.showwarning("Not Available", "This feature is currently not working")
            else:
                self.update_status(f"Executed: {item.name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute {item.name}: {str(e)}")
            self.update_status(f"Error executing: {item.name}")
    
    def run_batch_file(self, file_path):
        """Run batch file"""
        full_path = os.path.join(self.current_path, file_path)
        if os.path.exists(full_path):
            self.update_status(f"Running: {file_path}")
            try:
                # Run in separate thread to prevent GUI freezing
                threading.Thread(target=lambda: subprocess.run([full_path], 
                                                              shell=True, 
                                                              cwd=os.path.dirname(full_path)),
                               daemon=True).start()
                messagebox.showinfo("Success", f"Started: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to run {file_path}: {str(e)}")
        else:
            messagebox.showerror("Error", f"File not found: {full_path}")
    
    def run_executable(self, file_path):
        """Run executable file"""
        full_path = os.path.join(self.current_path, file_path)
        if os.path.exists(full_path):
            self.update_status(f"Running: {file_path}")
            try:
                threading.Thread(target=lambda: subprocess.Popen([full_path], 
                                                                cwd=os.path.dirname(full_path)),
                               daemon=True).start()
                messagebox.showinfo("Success", f"Started: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to run {file_path}: {str(e)}")
        else:
            messagebox.showerror("Error", f"File not found: {full_path}")
    
    def update_status(self, message):
        """Update status bar"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_label.config(text=f"{timestamp} | {message}")
    
    # Music player methods
    def toggle_play_pause(self):
        """Toggle play/pause"""
        if not self.music_player.playlist:
            messagebox.showwarning("No Music", "No tracks found in Music folder")
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
        self.update_status("Playlist refreshed")
    
    def update_music_info(self):
        """Update music player info display"""
        if hasattr(self, 'track_name_label'):
            # Update track name
            track_name = self.music_player.get_current_track_name()
            if len(track_name) > 30:
                track_name = track_name[:27] + "..."
            self.track_name_label.config(text=track_name)
            
            # Update time and progress
            current_time = self.music_player.format_time(self.music_player.get_current_time())
            total_time = self.music_player.format_time(self.music_player.duration)
            progress = self.music_player.get_progress()
            
            self.current_time_label.config(text=current_time)
            self.total_time_label.config(text=total_time)
            self.progress_var.set(progress)
            
            # Check if track ended
            if (self.music_player.playing and 
                not self.music_player.paused and 
                progress >= 99):
                self.next_track()
        
        # Schedule next update
        self.root.after(1000, self.update_music_info)
    
    def setup_menu(self):
        """Setup menu structure"""
        self.main_menu = [
            MenuItem("Firmware Flashing", submenu=[
                MenuItem("Original Boot and Magisk Boot", submenu=[
                    MenuItem("HyperOS 1", submenu=[
                        MenuItem("HyperOS 1.0.3.0.UMFMIXM", submenu=[
                            MenuItem("Original", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 1\HyperOS 1.0.3.0.UMFMIXM\Оригинал.bat"),
                            MenuItem("Magisk", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 1\HyperOS 1.0.3.0.UMFMIXM\Magisk.bat")
                        ]),
                        MenuItem("HyperOS 1.0.4.0.UMFMIXM", submenu=[
                            MenuItem("Original", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 1\HyperOS 1.0.4.0.UMFMIXM\Оригинал.bat"),
                            MenuItem("Magisk", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 1\HyperOS 1.0.4.0.UMFMIXM\Magisk.bat")
                        ]),
                        MenuItem("HyperOS 1.0.5.0.UMFMIXM", submenu=[
                            MenuItem("Original", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 1\HyperOS 1.0.5.0.UMFMIXM\Оригинал.bat"),
                            MenuItem("Magisk", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 1\HyperOS 1.0.5.0.UMFMIXM\Magisk.bat")
                        ]),
                        MenuItem("HyperOS 1.0.6.0.UMFMIXM", submenu=[
                            MenuItem("Original", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 1\HyperOS 1.0.6.0.UMFMIXM\Оригинал.bat"),
                            MenuItem("Magisk", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 1\HyperOS 1.0.6.0.UMFMIXM\Magisk.bat")
                        ]),
                        MenuItem("HyperOS 1.0.9.0.UMFMIXM", submenu=[
                            MenuItem("Original", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 1\HyperOS 1.0.9.0.UMFMIXM\Оригинал.bat"),
                            MenuItem("Magisk", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 1\HyperOS 1.0.9.0.UMFMIXM\Magisk.bat")
                        ]),
                        MenuItem("HyperOS 1.0.10.0.UMFMIXM", submenu=[
                            MenuItem("Original", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 1\HyperOS 1.0.10.0.UMFMIXM\Оригинал.bat"),
                            MenuItem("Magisk", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 1\HyperOS 1.0.10.0.UMFMIXM\Magisk.bat")
                        ])
                    ]),
                    MenuItem("HyperOS 2", submenu=[
                        MenuItem("HyperOS 2.0.2.0.VMFMIXM", submenu=[
                            MenuItem("Original", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 2\HyperOS 2.0.2.0.VMFMIXM\Оригинал.bat"),
                            MenuItem("Magisk", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 2\HyperOS 2.0.2.0.VMFMIXM\Magisk.bat")
                        ]),
                        MenuItem("HyperOS 2.0.3.0.VMFMIXM", submenu=[
                            MenuItem("Original", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 2\HyperOS 2.0.3.0.VMFMIXM\Оригинал.bat"),
                            MenuItem("Magisk", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 2\HyperOS 2.0.3.0.VMFMIXM\Magisk.bat")
                        ]),
                        MenuItem("HyperOS 2.0.103.0.VMFMIXM", submenu=[
                            MenuItem("Original", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 2\HyperOS 2.0.103.0.VMFMIXM\Оригинал.bat"),
                            MenuItem("Magisk", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 2\HyperOS 2.0.103.0.VMFMIXM\Magisk.bat")
                        ]),
                        MenuItem("HyperOS 2.0.104.0.VMFMIXM", submenu=[
                            MenuItem("Original", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 2\HyperOS 2.0.104.0.VMFMIXM\Оригинал.bat"),
                            MenuItem("Magisk", MenuAction.RUN_BAT, r"Прошивка оригинального boot и с вшитым magisk\HyperOS 2\HyperOS 2.0.104.0.VMFMIXM\Magisk.bat")
                        ])
                    ])
                ]),
                MenuItem("Official Firmware Loading", submenu=[
                    MenuItem("HyperOS 2.0.103.0 EEA", MenuAction.RUN_BAT, r"Загрузка прошивки на основе официальной\HyperOS 2.0.103.0 EEA.bat")
                ]),
                MenuItem("Custom Recovery", submenu=[
                    MenuItem("OrangeFox", MenuAction.RUN_BAT, r"Кастом Recovery\OrangeFox.bat")
                ]),
                MenuItem("Official Firmware for Fastboot", submenu=[
                    MenuItem("FastbootTool", MenuAction.RUN_EXE, r"Прошивка официальных прошивок для Fastboot mode\FastbootTool.exe")
                ])
            ]),
            MenuItem("Bootloader Unlock", submenu=[
                MenuItem("MI Flash Unlock", MenuAction.RUN_EXE, r"Разблокировка загрузчика\miflash_unlock.exe"),
                MenuItem("Driver Install", MenuAction.RUN_EXE, r"Разблокировка загрузчика\driver_install.exe"),
                MenuItem("Driver Install 64-bit", MenuAction.RUN_EXE, r"Разблокировка загрузчика\driver_install_64.exe")
            ]),
            MenuItem("Help & Info", submenu=[
                MenuItem("GitHub Repository", MenuAction.OPEN_URL, "https://github.com/example/repo"),
                MenuItem("Documentation", MenuAction.SHOW_LINK, "https://docs.example.com"),
                MenuItem("Support", MenuAction.SHOW_LINK, "https://support.example.com")
            ])
        ]
    
    def run(self):
        """Start the GUI application"""
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        # Start main loop
        self.root.mainloop()

if __name__ == "__main__":
    # Initialize and run the application
    try:
        app = FlashToolGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application: {e}")
