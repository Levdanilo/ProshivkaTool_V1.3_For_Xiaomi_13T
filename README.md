# ProshivkaTool v1.3t for Xiaomi 13T

## 🔧 Comprehensive Firmware Flashing Tool with Music Player

ProshivkaTool is a modern Python GUI application designed specifically for Xiaomi 13T firmware operations. It combines professional firmware flashing capabilities with an integrated music player for a pleasant user experience.

![ProshivkaTool Interface](attached_assets/30389_1754247107832.jpg)

## ✨ Features

### 🔌 Firmware Operations
- **Original Boot Firmware**: HyperOS 1.x and 2.x versions
- **Magisk Integration**: Pre-patched firmware with Magisk support
- **Custom Recovery**: OrangeFox recovery installation
- **Bootloader Unlock**: MiFlash unlock tools and drivers
- **Official Firmware**: FastbootTool and official ROM flashing

### 🎵 Integrated Music Player
- Support for MP3, WAV, OGG, and FLAC formats
- Playlist management with auto-refresh
- Volume control and playback controls
- Real-time progress tracking
- Cross-platform audio handling

### 🎨 Modern Interface
- Beautiful gradient background with custom image support
- Hierarchical menu navigation
- Real-time status updates
- Error handling with user-friendly messages
- Responsive design for different screen sizes

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)
- Required packages: `pygame`, `pillow`

### Installation
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install pygame pillow
   ```
3. Run the application:
   ```bash
   python ProshivkaTool.py
   ```

### Adding Music
1. Place your music files in the `Music/` folder
2. Supported formats: `.mp3`, `.wav`, `.ogg`, `.flac`
3. Click "Refresh Playlist" in the music player
4. Enjoy your music while working!

## 📁 Project Structure

```
ProshivkaTool/
├── ProshivkaTool.py          # Main application file
├── gui_styles.py             # GUI styling utilities
├── music_player_gui.py       # Music player components
├── Music/                    # Music files directory
│   ├── README.txt
│   └── sample_music_info.txt
├── attached_assets/          # Background images and assets
│   └── 30389_1754247107832.jpg
└── README.md                 # This file
```

## 🛠 Usage

### Navigation
- Use the menu buttons on the left to navigate through firmware options
- Click "← Back" to return to previous menu levels
- Current path is displayed at the top of the navigation panel

### Firmware Operations
- **Original Firmware**: Flash stock firmware without modifications
- **Magisk Firmware**: Flash firmware with pre-integrated Magisk for root access
- **Recovery**: Install custom recovery (OrangeFox)
- **Bootloader**: Unlock bootloader using official Mi tools

### Music Player
- **Play/Pause**: Toggle music playback
- **Next/Previous**: Navigate through tracks
- **Volume**: Adjust playback volume
- **Stop**: Stop current playback
- **Refresh**: Reload playlist from Music folder

## ⚠ Important Notes

### Audio Compatibility
- Audio playback requires proper audio drivers
- In environments without audio (like Replit), the interface remains functional
- Visual indicators show when audio is unavailable

### Firmware Operations
- This is a demonstration interface - actual firmware files are not included
- Always backup your device before flashing firmware
- Ensure you have the correct firmware for your specific device variant
- Flashing firmware carries inherent risks

## 🔧 Technical Details

### Architecture
- **GUI Framework**: tkinter with custom styling
- **Audio Engine**: pygame mixer
- **Image Processing**: PIL (Pillow)
- **Threading**: Background audio processing
- **Error Handling**: Comprehensive exception management

### Compatibility
- **OS**: Windows, macOS, Linux
- **Python**: 3.7+
- **Audio**: Optional (graceful degradation)

## 📝 Development

### Adding New Firmware
1. Extend the menu structure in `setup_menu()` method
2. Add corresponding action handlers in `execute_action()` method
3. Update the documentation

### Customizing Interface
1. Modify styles in `gui_styles.py`
2. Adjust colors and themes in `setup_styles()` method
3. Replace background image in `attached_assets/` folder

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding support for new firmware versions
- Improving the user interface
- Enhancing audio format support
- Adding new features

## ⚖ License

This project is for educational and personal use. Always comply with your device manufacturer's terms and local laws when modifying firmware.

## 🆘 Support

If you encounter issues:
1. Check that all dependencies are installed
2. Verify Python version compatibility
3. Ensure audio drivers are properly configured
4. Check the console output for error messages

---

**Made with ❤ for the Xiaomi community**