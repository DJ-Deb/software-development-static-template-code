from setuptools import setup, find_packages
from pathlib import Path
from typing import List


# Project Configuration
def get_input(prompt: str, default: str) -> str:
    value = input(f"{prompt} ({default}): ").strip()
    return value or default

print("=" * 10, "ML PROJECT CONFIGURATION", "=" * 10)

# Project Configuration
PROJECT_NAME = get_input("Project Name", "ml-project")

VERSION = "0.0.1"

AUTHOR = get_input("Author", "Your Name")

AUTHOR_EMAIL = get_input("Author Email", "your-email@example.com")

DESCRIPTION = get_input("Description", "Machine Learning Project")

PYTHON_REQUIRES = get_input("Python Version Requirement", ">=3.9")

GITHUB_URL = get_input("GitHub Repository URL", "https://github.com/yourusername/your-repository")

BASE_DIR = Path(__file__).parent

REQUIREMENTS_FILE = BASE_DIR / "requirements.txt"
README_FILE = BASE_DIR / "README.md"

# Constants
HYPHEN_E_DOT = "-e ."

# Display Configuration
print("=" * 10, "PROJECT CONFIGURATION", "=" * 10)
print(f"Project Name: {PROJECT_NAME}")
print(f"Version: {VERSION}")
print(f"Author: {AUTHOR}")
print(f"Author Email: {AUTHOR_EMAIL}")
print(f"Description: {DESCRIPTION}")
print(f"Python Requirement: {PYTHON_REQUIRES}")
print(f"GitHub URL: {GITHUB_URL}")

def get_requirements(file_path: Path) -> List[str]:
    requirements = []

    if not file_path.exists():
        return requirements

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            # Ignore empty lines
            if not line:
                continue

            # Ignore comments
            if line.startswith("#"):
                continue

            # Ignore editable installation
            if line == HYPHEN_E_DOT:
                continue

            requirements.append(line)

    return requirements

if README_FILE.exists():
    with open(README_FILE, "r", encoding="utf-8") as file:
        LONG_DESCRIPTION = file.read()
else:
    LONG_DESCRIPTION = DESCRIPTION

# Setup
setup(
    # Basic information
    name=PROJECT_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",

    # Author
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,

    # Project URLs
    url=GITHUB_URL,

    # Package discovery
    packages=find_packages(),

    # Dependencies
    install_requires=get_requirements(REQUIREMENTS_FILE),

    # Python version
    python_requires=PYTHON_REQUIRES,

    # Metadata
    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",

        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",

        "Operating System :: OS Independent",
    ],

    # Keywords for package indexes
    keywords=[
        PROJECT_NAME,
        "machine-learning",
        "machine-learning-project",
        "artificial-intelligence",
        "data-science",
        "mlops"
    ],

    # Include package data
    include_package_data=True,

    # Zip-safe package
    zip_safe=False,
)
