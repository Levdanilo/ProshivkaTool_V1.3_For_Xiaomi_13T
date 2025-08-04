# ProshivkaTool

## Overview

ProshivkaTool is a comprehensive Python GUI application designed for Xiaomi 13T firmware flashing operations with an integrated music player. The application features a modern graphical interface built with tkinter, beautiful gradient backgrounds, hierarchical menu navigation for firmware operations, and a fully functional music player that supports multiple audio formats. The tool is specifically designed for managing firmware flashing, bootloader unlocking, recovery installation, and custom ROM operations.

## Recent Changes (January 2025)

- ✅ **Complete GUI Implementation**: Created modern tkinter-based interface with gradient background
- ✅ **Background Image Integration**: Added support for custom background images with fallback gradient generation
- ✅ **Music Player Integration**: Full-featured music player with playlist management, volume control, and playback controls
- ✅ **Error Handling**: Comprehensive audio device error handling for environments without sound
- ✅ **Menu System**: Hierarchical navigation system for firmware operations and tools
- ✅ **Cross-Platform Compatibility**: Designed to work in various environments including Replit

## User Preferences

Preferred communication style: Simple, everyday language.
Language: Russian for UI and communication.

## System Architecture

### Core Architecture Pattern
The application follows a modular component-based architecture with clear separation of concerns:

**Main Application Controller (ProshivkaTool.py)**
- Serves as the central coordinator managing menu systems and user interactions
- Implements an enum-based action system for type-safe operation handling
- Uses a hierarchical MenuItem structure for organizing functionality

**GUI Architecture**
- Built on tkinter as the primary GUI framework
- Modular widget design with separate styling and component files
- Custom styling system (gui_styles.py) implementing modern dark theme aesthetics
- Specialized music player widget (music_player_gui.py) designed for embedding

**Music Player Subsystem**
- Pygame-based audio engine for cross-platform music playback
- Threaded audio processing to prevent GUI blocking
- Playlist management with support for multiple audio formats (MP3, WAV, OGG, FLAC)
- Real-time position tracking and volume control

**Action System Design**
- Enum-based MenuAction system provides type safety and clear operation categories
- Support for multiple operation types: batch file execution, URL handling, executable launching
- Extensible architecture allowing easy addition of new action types

### Design Patterns
- **Strategy Pattern**: Used in MenuAction enum for different operation types
- **Component Pattern**: Modular GUI widgets that can be embedded independently
- **Observer Pattern**: Music player status updates and GUI synchronization

### Threading Model
- Main GUI thread handles user interface interactions
- Separate background thread for music playback and position tracking
- Thread-safe communication between audio engine and GUI components

## External Dependencies

**Core Python Libraries**
- `tkinter` - Primary GUI framework for cross-platform desktop interface
- `pygame` - Audio playback engine and mixer functionality
- `threading` - Background audio processing and non-blocking operations
- `subprocess` - System command execution for batch files and executables
- `webbrowser` - URL opening and web content integration

**Image Processing**
- `PIL (Pillow)` - Image handling and manipulation for GUI assets
- `io` and `base64` - Image data encoding and processing

**System Integration**
- `os` - File system operations and path management
- `sys` - System-specific parameters and functions
- `datetime` - Timestamp and time-based operations

**Audio Format Support**
- MP3, WAV, OGG, and FLAC audio file formats through pygame mixer
- Automatic playlist generation from music directory scanning

**File System Requirements**
- Music files stored in designated music directory
- Automatic directory creation if music folder doesn't exist
- Support for various executable file types and batch scripts