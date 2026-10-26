from setuptools import setup, find_packages

setup(
    name="linux-system-monitor",
    version="1.0.0",
    author="Abhijit Uday Naik",
    author_email="naikabhi081004@gmail.com",
    description="High-performance Linux system monitoring, socket diagnostics, and log parsing CLI utility",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Abhijit0810/linux-system-monitor",
    packages=find_packages(),
    install_requires=[
        "psutil>=5.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=6.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "linux-mon=src.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)
