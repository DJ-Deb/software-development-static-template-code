from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

CONFIG_FILE_PATH = PROJECT_ROOT/"config"/"config.yml"

# Here the "Project-name" is to be changed
ARTIFACT_DIR = PROJECT_ROOT/"artifacts"/"Project-name"
