#!/usr/bin/env python3
"""
Dependency installer for ProshivkaTool
Installs required packages: pygame and pillow
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def main():
    """Install all required dependencies"""
    print("🚀 Installing ProshivkaTool dependencies...")
    
    packages = [
        "pygame>=2.0.0",
        "pillow>=8.0.0"
    ]
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📦 Installation complete: {success_count}/{len(packages)} packages installed")
    
    if success_count == len(packages):
        print("🎉 All dependencies installed successfully!")
        print("You can now run: python ProshivkaTool.py")
    else:
        print("⚠ Some packages failed to install. Please check the errors above.")

if __name__ == "__main__":
    main()