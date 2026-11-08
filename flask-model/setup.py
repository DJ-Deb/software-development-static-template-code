
from setuptools import setup, find_packages
from pathlib import Path

BASE_DIR = Path(__file__).parent

REQUIREMENTS_FILE = BASE_DIR / "requirements.txt"
README_FILE = BASE_DIR / "README.md"


def get_requirements(file_path: Path) -> list[str]:
    requirements = []

    if not file_path.exists():
        return requirements

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if line == "-e .":
                continue

            requirements.append(line)

    return requirements


LONG_DESCRIPTION = (
    README_FILE.read_text(encoding="utf-8")
    if README_FILE.exists()
    else "Machine Learning Project"
)


setup(
    name="ml-project",
    version="0.0.1",
    description="Machine Learning Project",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",

    packages=find_packages(),

    install_requires=get_requirements(REQUIREMENTS_FILE),

    python_requires=">=3.9",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    include_package_data=True,
    zip_safe=False,
)
