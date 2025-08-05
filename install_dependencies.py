#!/usr/bin/env python3
"""
Dependency installer for ProshivkaTool
Installs all required packages for the application
"""

import subprocess
import sys
import platform
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def install_system_dependencies():
    """Install system-level dependencies for specific platforms"""
    system = platform.system()
    print(f"🖥️  Detected system: {system}")
    
    if system == "Linux":
        print("🔧 Installing Linux system dependencies...")
        try:
            # Ubuntu/Debian
            if os.path.exists("/etc/debian_version"):
                subprocess.check_call(
                    ["sudo", "apt-get", "install", "-y", 
                     "python3-tk", "python3-dev", 
                     "libsdl1.2-dev", "libsdl-image1.2-dev", 
                     "libsdl-mixer1.2-dev", "libsdl-ttf2.0-dev", 
                     "portaudio19-dev"]
                )
            # Fedora/CentOS
            elif os.path.exists("/etc/redhat-release"):
                subprocess.check_call(
                    ["sudo", "dnf", "install", "-y", 
                     "python3-tkinter", "python3-devel", 
                     "SDL-devel", "SDL_image-devel", 
                     "SDL_mixer-devel", "SDL_ttf-devel", 
                     "portaudio-devel"]
                )
            print("✅ Linux dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Linux dependencies")
            return False
    
    elif system == "Darwin":  # macOS
        print("🍎 Installing macOS system dependencies...")
        try:
            # Install Homebrew if not installed
            if not os.path.exists("/usr/local/bin/brew"):
                subprocess.check_call(
                    '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                    shell=True
                )
            # Install dependencies
            subprocess.check_call(["brew", "install", "portaudio", "sdl2", "sdl2_image", "sdl2_mixer", "sdl2_ttf"])
            print("✅ macOS dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install macOS dependencies")
            return False
    
    elif system == "Windows":
        print("🪟 Windows detected - no additional system dependencies required")
        return True
    
    return False

def main():
    """Install all required dependencies"""
    print("="*50)
    print("🚀 Installing ProshivkaTool dependencies")
    print("="*50)
    
    # First install system-level dependencies
    sys_success = install_system_dependencies()
    
    # Python packages to install
    packages = [
        "pygame>=2.5.0",           # For music player
        "pillow>=10.0.0",           # For image processing
        "pyinstaller",              # For creating executables
        "pywin32; platform_system=='Windows'",  # Windows API integration
        "pyaudio",                  # Audio backend
        "requests",                 # For potential future web features
        "setuptools",               # For package management
        "wheel"                     # For building packages
    ]
    
    print("\n📦 Installing Python packages...")
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print("\n" + "="*50)
    print(f"📊 Installation summary:")
    print(f"- System dependencies: {'✅' if sys_success else '❌'}")
    print(f"- Python packages: {success_count}/{len(packages)} installed")
    
    if sys_success and success_count == len(packages):
        print("\n🎉 All dependencies installed successfully!")
        print("You can now run: python ProshivkaTool.py")
    else:
        print("\n⚠ Some components failed to install:")
        if not sys_success:
            print("- System dependencies installation failed")
        if success_count < len(packages):
            print(f"- {len(packages) - success_count} Python packages failed to install")
        
        print("\nTroubleshooting tips:")
        print("1. Make sure you have Python 3.8+ installed")
        print("2. Try running as administrator/root")
        print("3. Update pip: python -m pip install --upgrade pip")
        
        # Platform-specific troubleshooting
        system = platform.system()
        if system == "Windows":
            print("4. Install Microsoft Build Tools: https://aka.ms/buildtools")
        elif system == "Linux":
            print("4. Try: sudo apt update && sudo apt upgrade")
        elif system == "Darwin":
            print("4. Make sure Xcode Command Line Tools are installed: xcode-select --install")
    
    print("="*50)

if __name__ == "__main__":
    main()