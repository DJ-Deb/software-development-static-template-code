import sys
import joblib
from exception import CustomException
from logger import Logger

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

# change
#model_name with the name of the current model
from model.model_name.constants import MODEL_NAME
from model.model_name.constants.directories import ARTIFACT_DIR
#change


class ModelTrainer:

    MODEL_REGISTRY = {
        "LinearRegression": LinearRegression,
        "Ridge": Ridge,
        "Lasso": Lasso,
        "DecisionTreeRegressor": DecisionTreeRegressor,
        "RandomForestRegressor": RandomForestRegressor,
        "GradientBoostingRegressor": GradientBoostingRegressor,
        # .......
    }

    def __init__(self):
        self.logger = Logger(model_name=MODEL_NAME)

    def __save_model(self, model):
        joblib.dump(ARTIFACT_DIR/"trained_model.joblib")

    def initiate(self, X_train, y_train):
        self.logger.info("Initializing model training")
        
        try:
            self.__save_model(model="model obj")
            pass
        except Exception as e:
            self.logger.exception("Model training failed")
            raise CustomException(f"Error during model training: {e}", sys)