"""
Setup script for pAI_Lang tooling package.

This script handles the installation and distribution of the pAI_Lang tooling system.
"""

from setuptools import setup, find_packages

setup(
    name="pailang_tooling",
    version="1.2.0",
    description="Tooling for the Promethean AI Language (pAI_Lang)",
    author="Manus AI",
    author_email="info@example.com",
    packages=find_packages(),
    install_requires=[
        "lark-parser>=1.1.5",
        "numpy>=1.20.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "coverage>=7.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
