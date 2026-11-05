import sys
from exception import CustomException
from logger import Logger

import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

# change
#model_name with the name of the current model
from model.model_name.constants import MODEL_NAME
from model.model_name.constants.directories import ARTIFACT_DIR
from model.model_name.constants.values import TRAIN_SIZE, TEST_SIZE, RANDOM_STATE
#change


def create_preprocessor(numerical_columns, categorical_columns):

    # Numerical pipeline
    numerical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median"))
    ])

    # Categorical pipeline
    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent"))
    ])

    # Combine both pipelines
    preprocessor = ColumnTransformer([
        ("numerical", numerical_pipeline, numerical_columns),
        ("categorical", categorical_pipeline, categorical_columns)
    ])

    return preprocessor


class DataTransformation:

    def __init__(self):
        self.logger = Logger(model_name=MODEL_NAME)

    def initiate(self, data, target_column):
        self.logger.info("Starting data transformation component")

        try:
            X = data.drop(columns="")
            Y = data[target_column]

            # Identify column types
            numerical_columns = X.select_dtypes(include=["number"]).columns.tolist()
            categorical_columns = X.select_dtypes(include=["object", "category", "string"]).columns.tolist()

            x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=TEST_SIZE, train_size=TRAIN_SIZE, random_state=RANDOM_STATE)

            preprocessor = create_preprocessor(numerical_columns, categorical_columns)

            x_train_transformed = preprocessor.fit_transform(x_train)
            x_test_transformed = preprocessor.transform(x_test)

            joblib.dump(preprocessor, ARTIFACT_DIR/"preprocessor.joblib")

            self.logger.info(f"Data transformation completed successfully")

            return (
                x_train_transformed,
                x_test_transformed,
                y_train,
                y_test
            )

        except Exception as e:
            self.logger.exception("Data transformation failed")
            raise CustomException(e, sys)