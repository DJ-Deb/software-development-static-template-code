import sys

from exception import CustomException
from logger import Logger

# change
# model_name with the name of the current model
from model.model_name.constants import MODEL_NAME

from model.model_name.components.data_ingestion import DataIngestion
from model.model_name.components.data_validation import DataValidation
from model.model_name.components.data_transformation import DataTransformation
from model.model_name.components.model_trainer import ModelTrainer
from model.model_name.components.model_evaluation import ModelEvaluation
# change


class TrainingPipeline:

    def __init__(self):
        self.logger = Logger(model_name=MODEL_NAME)

    def initiate(self, data):
        self.logger.info(f"Starting {MODEL_NAME} training pipeline")

        try:
            # 1. Data Ingestion
            data = DataIngestion().initiate(data)

            # 2. Data Validation
            validated_data = DataValidation().initiate(data)

            # 3. Data Transformation
            X_train, X_test, y_train, y_test, preprocessor = DataTransformation().initiate(validated_data, target_column="price")

            # 4. Model Training
            trained_model = ModelTrainer().initiate(X_train, y_train)

            # 5. Model Evaluation
            evaluation_result = ModelEvaluation().initiate(trained_model, X_test, y_test)

            return evaluation_result

        except Exception as e:
            self.logger.exception("Training pipeline failed")
            raise CustomException(f"Training pipeline failed: {e}", sys)