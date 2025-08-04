#!/usr/bin/env python3
"""
ProshivkaTool v1.3t for Xiaomi 13T
Main launcher script for the GUI application

Usage:
    python run.py
    
Or simply double-click this file if Python is properly configured.
"""

import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    missing_deps = []
    
    try:
        import pygame
    except ImportError:
        missing_deps.append("pygame")
    
    try:
        import PIL
    except ImportError:
        missing_deps.append("pillow")
    
    try:
        import tkinter
    except ImportError:
        missing_deps.append("tkinter")
    
    return missing_deps

def main():
    """Main entry point"""
    print("🚀 Starting ProshivkaTool v1.3t for Xiaomi 13T...")
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("📦 Please install missing packages:")
        for dep in missing:
            if dep == "pillow":
                print(f"   pip install {dep}")
            else:
                print(f"   pip install {dep}")
        print("\nOr run: python install_dependencies.py")
        return 1
    
    # Import and run the main application
    try:
        from ProshivkaTool import FlashToolGUI
        print("✅ Dependencies verified, launching GUI...")
        
        app = FlashToolGUI()
        app.run()
        
    except ImportError as e:
        print(f"❌ Error importing ProshivkaTool: {e}")
        print("📁 Make sure ProshivkaTool.py is in the same directory")
        return 1
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())