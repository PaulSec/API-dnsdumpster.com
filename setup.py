"""Setup configuration for DNSDumpster API package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="dnsdumpster",
    version="0.11.0",
    description="UNOFFICIAL Python API wrapper for dnsdumpster.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Paul Sec",
    author_email="paulwebsec@gmail.com",
    url="https://github.com/PaulSec/API-dnsdumpster.com",
    download_url="https://github.com/PaulSec/API-dnsdumpster.com/archive/refs/tags/v0.11.0.tar.gz",
    keywords=["dnsdumpster", "dns", "subdomain", "reconnaissance", "security"],
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Bug Reports": "https://github.com/PaulSec/API-dnsdumpster.com/issues",
        "Source": "https://github.com/PaulSec/API-dnsdumpster.com",
        "Documentation": "https://github.com/PaulSec/API-dnsdumpster.com#readme",
    },
)
