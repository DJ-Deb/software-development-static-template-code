
import sys
import shutil

from pathlib import Path
from textwrap import dedent

from logger import Logger


logger = Logger(model_name="template_generator")


class Templates:

    @staticmethod
    def get_requirement_template() -> str:
        """Return the content for requirements.txt."""

        return dedent("""
            # Add your project dependencies here
            setuptools
            flask
            dvc
            pandas
            numpy
            scikit-learn
            python-dotenv
        """).lstrip()


class TemplateGenerator:

    ROOT_FILE_LIST = [
        # Application
        "app.py",

        # Docker
        "Dockerfile",
        ".dockerignore",

        # Git
        ".gitignore",

        # Environment
        ".env",

        # Dependencies
        "requirements.txt",
        "pyproject.toml",

        # Documentation
        "README.md",

        # Testing
        "tests/__init__.py",
        "tests/test_data.py",
        "tests/test_model.py",
        "tests/test_pipeline.py",

        # Configuration
        "config/config.yaml",
    ]

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent
        self.template_dir = self.project_root / "file_templates"

    def create_root_files(self):
        for filename in self.ROOT_FILE_LIST:
            filepath = self.project_root / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            if not filepath.exists():
                filepath.touch()
                logger.info(f"Created file: {filepath}")
            else:
                logger.info(f"File already exists: {filepath}")

    def create_requirements(self):
        requirements_path = (self.project_root / "requirements.txt")

        # Only populate if the file is empty.
        if requirements_path.stat().st_size == 0:

            requirements_content = Templates.get_requirement_template()

            requirements_path.write_text(requirements_content, encoding="utf-8")
            logger.info(f"Requirements template generated: {requirements_path}")
        else:
            logger.info("Requirements file already contains content. Skipping.")

    def generate(self, model_name: str):
        try:
            logger.info(f"Starting template generation for: {model_name}")

            # 1. Create root-level files.
            self.create_root_files()

            # 2. Generate requirements.txt if empty.
            self.create_requirements()
            logger.info(f"Template generation completed for: {model_name}")
        except Exception as e:
            logger.exception(f"Template generation failed: {e}")
            raise


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Usage: python template.py <model_name>")

    model_name = sys.argv[1].strip()

    if not model_name:
        raise ValueError("Model name cannot be empty.")

    # Prevent path traversal and invalid directory names.
    if (Path(model_name).name != model_name or model_name in {".", ".."} or "/" in model_name or "\\" in model_name):
        raise ValueError("Invalid model name. Use a single directory name.")

    generator = TemplateGenerator()
    generator.generate(model_name)
