"""
Music Player GUI Components for ProshivkaTool
"""
import tkinter as tk
from tkinter import ttk
import pygame
import threading
import time
import os
from PIL import Image, ImageTk

class MusicPlayerWidget(tk.Frame):
    """Standalone music player widget that can be embedded in any tkinter application"""
    
    def __init__(self, parent, music_player, **kwargs):
        super().__init__(parent, **kwargs)
        self.music_player = music_player
        self.update_active = True
        
        # Configure widget styling
        self.configure(bg='#2e2e3e', relief='raised', bd=2)
        
        self.create_widgets()
        self.start_update_loop()
        
    def create_widgets(self):
        """Create all music player widgets"""
        # Header
        self.header_frame = tk.Frame(self, bg='#2e2e3e')
        self.header_frame.pack(fill=tk.X, pady=(10, 5))
        
        self.title_label = tk.Label(self.header_frame,
                                   text="♫ Music Player",
                                   font=('Arial', 14, 'bold'),
                                   fg='#4facfe',
                                   bg='#2e2e3e')
        self.title_label.pack()
        
        # Track display
        self.track_frame = tk.Frame(self, bg='#2e2e3e')
        self.track_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.track_label = tk.Label(self.track_frame,
                                   text="No track loaded",
                                   font=('Arial', 10),
                                   fg='#ffffff',
                                   bg='#2e2e3e',
                                   wraplength=200,
                                   justify='center')
        self.track_label.pack()
        
        # Progress section
        self.progress_frame = tk.Frame(self, bg='#2e2e3e')
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Time labels
        self.time_frame = tk.Frame(self.progress_frame, bg='#2e2e3e')
        self.time_frame.pack(fill=tk.X)
        
        self.current_time_label = tk.Label(self.time_frame,
                                          text="00:00",
                                          font=('Arial', 8),
                                          fg='#e0e0e0',
                                          bg='#2e2e3e')
        self.current_time_label.pack(side=tk.LEFT)
        
        self.total_time_label = tk.Label(self.time_frame,
                                        text="00:00",
                                        font=('Arial', 8),
                                        fg='#e0e0e0',
                                        bg='#2e2e3e')
        self.total_time_label.pack(side=tk.RIGHT)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame,
                                          variable=self.progress_var,
                                          maximum=100,
                                          length=200)
        self.progress_bar.pack(fill=tk.X, pady=2)
        
        # Control buttons
        self.control_frame = tk.Frame(self, bg='#2e2e3e')
        self.control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Button styling
        button_style = {
            'font': ('Arial', 12),
            'bg': '#4facfe',
            'fg': 'white',
            'relief': 'flat',
            'bd': 0,
            'width': 3,
            'height': 1
        }
        
        self.prev_btn = tk.Button(self.control_frame,
                                 text="⏮",
                                 command=self.prev_track,
                                 **button_style)
        self.prev_btn.pack(side=tk.LEFT, padx=2)
        
        self.play_pause_btn = tk.Button(self.control_frame,
                                       text="▶",
                                       command=self.toggle_play_pause,
                                       **button_style)
        self.play_pause_btn.pack(side=tk.LEFT, padx=2)
        
        self.next_btn = tk.Button(self.control_frame,
                                 text="⏭",
                                 command=self.next_track,
                                 **button_style)
        self.next_btn.pack(side=tk.LEFT, padx=2)
        
        self.stop_btn = tk.Button(self.control_frame,
                                 text="⏹",
                                 command=self.stop_music,
                                 **button_style)
        self.stop_btn.pack(side=tk.LEFT, padx=2)
        
        # Volume control
        self.volume_frame = tk.Frame(self, bg='#2e2e3e')
        self.volume_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(self.volume_frame,
                text="Volume",
                font=('Arial', 9),
                fg='#e0e0e0',
                bg='#2e2e3e').pack()
        
        self.volume_var = tk.DoubleVar(value=self.music_player.volume * 100)
        self.volume_scale = ttk.Scale(self.volume_frame,
                                    from_=0, to=100,
                                    variable=self.volume_var,
                                    command=self.change_volume,
                                    orient=tk.HORIZONTAL)
        self.volume_scale.pack(fill=tk.X, pady=2)
        
        # Playlist info
        self.playlist_frame = tk.Frame(self, bg='#2e2e3e')
        self.playlist_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.playlist_info = tk.Label(self.playlist_frame,
                                     text=f"Tracks: {len(self.music_player.playlist)}",
                                     font=('Arial', 8),
                                     fg='#a0a0a0',
                                     bg='#2e2e3e')
        self.playlist_info.pack()
        
        # Refresh button
        self.refresh_btn = tk.Button(self.playlist_frame,
                                    text="Refresh Playlist",
                                    command=self.refresh_playlist,
                                    font=('Arial', 8),
                                    bg='#00f2fe',
                                    fg='white',
                                    relief='flat',
                                    bd=0,
                                    pady=2)
        self.refresh_btn.pack(fill=tk.X, pady=2)
        
        # Add hover effects to buttons
        self.add_button_hover_effects()
    
    def add_button_hover_effects(self):
        """Add hover effects to buttons"""
        buttons = [self.prev_btn, self.play_pause_btn, self.next_btn, 
                  self.stop_btn, self.refresh_btn]
        
        for btn in buttons:
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#00f2fe'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#4facfe'))
    
    def toggle_play_pause(self):
        """Toggle play/pause"""
        if not self.music_player.playlist:
            return
            
        if self.music_player.playing and not self.music_player.paused:
            self.music_player.pause()
            self.play_pause_btn.config(text="▶")
        elif self.music_player.playing and self.music_player.paused:
            self.music_player.unpause()
            self.play_pause_btn.config(text="⏸")
        else:
            if self.music_player.play():
                self.play_pause_btn.config(text="⏸")
    
    def stop_music(self):
        """Stop music"""
        self.music_player.stop()
        self.play_pause_btn.config(text="▶")
        self.progress_var.set(0)
    
    def next_track(self):
        """Next track"""
        if self.music_player.next_track():
            self.play_pause_btn.config(text="⏸")
    
    def prev_track(self):
        """Previous track"""
        if self.music_player.prev_track():
            self.play_pause_btn.config(text="⏸")
    
    def change_volume(self, value):
        """Change volume"""
        volume = float(value) / 100
        self.music_player.set_volume(volume)
    
    def refresh_playlist(self):
        """Refresh music playlist"""
        self.music_player.load_playlist()
        self.playlist_info.config(text=f"Tracks: {len(self.music_player.playlist)}")
    
    def update_display(self):
        """Update music player display"""
        if not self.update_active:
            return
            
        # Update track name
        track_name = self.music_player.get_current_track_name()
        if len(track_name) > 25:
            track_name = track_name[:22] + "..."
        self.track_label.config(text=track_name)
        
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
            progress >= 99):
            self.next_track()
    
    def start_update_loop(self):
        """Start the update loop"""
        def update_loop():
            while self.update_active:
                try:
                    self.update_display()
                    time.sleep(0.5)
                except:
                    break
        
        self.update_thread = threading.Thread(target=update_loop, daemon=True)
        self.update_thread.start()
    
    def destroy(self):
        """Clean up when widget is destroyed"""
        self.update_active = False
        super().destroy()

class MiniMusicPlayer(tk.Frame):
    """Compact music player for embedding in toolbars or status bars"""
    
    def __init__(self, parent, music_player, **kwargs):
        super().__init__(parent, **kwargs)
        self.music_player = music_player
        
        self.configure(bg='#1a1a2e', height=40)
        self.pack_propagate(False)
        
        self.create_compact_widgets()
        self.start_update_loop()
    
    def create_compact_widgets(self):
        """Create compact music player widgets"""
        # Control buttons
        button_style = {
            'font': ('Arial', 10),
            'bg': '#4facfe',
            'fg': 'white',
            'relief': 'flat',
            'bd': 0,
            'width': 2,
            'height': 1
        }
        
        self.prev_btn = tk.Button(self, text="⏮", command=self.prev_track, **button_style)
        self.prev_btn.pack(side=tk.LEFT, padx=2, pady=5)
        
        self.play_pause_btn = tk.Button(self, text="▶", command=self.toggle_play_pause, **button_style)
        self.play_pause_btn.pack(side=tk.LEFT, padx=2, pady=5)
        
        self.next_btn = tk.Button(self, text="⏭", command=self.next_track, **button_style)
        self.next_btn.pack(side=tk.LEFT, padx=2, pady=5)
        
        # Track info
        self.track_info = tk.Label(self,
                                  text="No track",
                                  font=('Arial', 8),
                                  fg='#ffffff',
                                  bg='#1a1a2e',
                                  anchor='w')
        self.track_info.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # Mini volume control
        self.volume_var = tk.DoubleVar(value=self.music_player.volume * 100)
        self.volume_scale = ttk.Scale(self,
                                    from_=0, to=100,
                                    variable=self.volume_var,
                                    command=self.change_volume,
                                    orient=tk.HORIZONTAL,
                                    length=80)
        self.volume_scale.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Add hover effects
        for btn in [self.prev_btn, self.play_pause_btn, self.next_btn]:
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#00f2fe'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#4facfe'))
    
    def toggle_play_pause(self):
        """Toggle play/pause"""
        if not self.music_player.playlist:
            return
            
        if self.music_player.playing and not self.music_player.paused:
            self.music_player.pause()
            self.play_pause_btn.config(text="▶")
        elif self.music_player.playing and self.music_player.paused:
            self.music_player.unpause()
            self.play_pause_btn.config(text="⏸")
        else:
            if self.music_player.play():
                self.play_pause_btn.config(text="⏸")
    
    def next_track(self):
        """Next track"""
        if self.music_player.next_track():
            self.play_pause_btn.config(text="⏸")
    
    def prev_track(self):
        """Previous track"""
        if self.music_player.prev_track():
            self.play_pause_btn.config(text="⏸")
    
    def change_volume(self, value):
        """Change volume"""
        volume = float(value) / 100
        self.music_player.set_volume(volume)
    
    def update_display(self):
        """Update compact display"""
        track_name = self.music_player.get_current_track_name()
        if len(track_name) > 30:
            track_name = track_name[:27] + "..."
        
        status = "Playing" if self.music_player.playing and not self.music_player.paused else "Paused"
        display_text = f"{status}: {track_name}" if self.music_player.playlist else "No tracks"
        
        self.track_info.config(text=display_text)
    
    def start_update_loop(self):
        """Start the update loop"""
        def update():
            try:
                self.update_display()
            except:
                pass
            self.after(1000, update)
        
        update()

class PlaylistManager(tk.Toplevel):
    """Separate window for managing music playlist"""
    
    def __init__(self, parent, music_player):
        super().__init__(parent)
        self.music_player = music_player
        
        self.title("Playlist Manager")
        self.geometry("400x500")
        self.configure(bg='#1a1a2e')
        
        self.create_playlist_widgets()
        self.refresh_playlist_display()
    
    def create_playlist_widgets(self):
        """Create playlist management widgets"""
        # Header
        header = tk.Label(self,
                         text="Music Playlist",
                         font=('Arial', 16, 'bold'),
                         fg='#4facfe',
                         bg='#1a1a2e')
        header.pack(pady=10)
        
        # Playlist listbox
        self.playlist_frame = tk.Frame(self, bg='#1a1a2e')
        self.playlist_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(self.playlist_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.playlist_listbox = tk.Listbox(self.playlist_frame,
                                          yscrollcommand=scrollbar.set,
                                          bg='#2e2e3e',
                                          fg='#ffffff',
                                          selectbackground='#4facfe',
                                          font=('Arial', 10))
        self.playlist_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.playlist_listbox.yview)
        
        # Double-click to play
        self.playlist_listbox.bind('<Double-Button-1>', self.play_selected)
        
        # Control buttons
        button_frame = tk.Frame(self, bg='#1a1a2e')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(button_frame,
                 text="Play Selected",
                 command=self.play_selected,
                 bg='#4facfe',
                 fg='white',
                 relief='flat',
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame,
                 text="Refresh",
                 command=self.refresh_playlist_display,
                 bg='#00f2fe',
                 fg='white',
                 relief='flat',
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame,
                 text="Close",
                 command=self.destroy,
                 bg='#e74c3c',
                 fg='white',
                 relief='flat',
                 font=('Arial', 10)).pack(side=tk.RIGHT, padx=5)
    
    def refresh_playlist_display(self):
        """Refresh the playlist display"""
        self.playlist_listbox.delete(0, tk.END)
        
        for i, track_path in enumerate(self.music_player.playlist):
            track_name = os.path.basename(track_path)
            marker = "♫ " if i == self.music_player.current_track else "  "
            self.playlist_listbox.insert(tk.END, f"{marker}{track_name}")
    
    def play_selected(self, event=None):
        """Play the selected track"""
        selection = self.playlist_listbox.curselection()
        if selection:
            track_index = selection[0]
            self.music_player.play(track_index)
            self.refresh_playlist_display()
