#!/usr/bin/env python3
"""
Setup script for ProshivkaTool v1.3t
Creates a distributable package of the application
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read dependencies
def read_requirements():
    requirements = [
        "pygame>=2.0.0",
        "pillow>=8.0.0"
    ]
    return requirements

setup(
    name="proshivkatool",
    version="1.3t",
    author="ProshivkaTool Contributors",
    author_email="",
    description="Comprehensive Xiaomi 13T firmware flashing tool with integrated music player",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ProshivkaTool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Hardware",
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "Topic :: Software Development :: User Interfaces",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "proshivkatool=ProshivkaTool:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.jpg", "*.png"],
    },
    keywords="xiaomi firmware flashing gui music player android",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ProshivkaTool/issues",
        "Source": "https://github.com/yourusername/ProshivkaTool",
        "Documentation": "https://github.com/yourusername/ProshivkaTool/blob/main/README.md",
    },
)