import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from src.exception import CustomException
from src.logger import logging

from src.utils import save_object
from src.utils import evaluate_model

from dataclasses import dataclass
import sys
import os


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initate_model_training(self, train_array, test_array):
        try:
            logging.info(
                "Splitting Dependent And Independent Variables From Train And Test Data"
            )
            # This Selects All Rows And All Columns Except The Last One From Train_Array
            # It Is Assumed That The Last Column In Train_Array Corresponds To The Dependent Variable

            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            models = {
                "LinearRegression": LinearRegression(),
                "Lasso": Lasso(),
                "Ridge": Ridge(),
                "Elasticnet": ElasticNet(),
                "DecisionTree": DecisionTreeRegressor(),
            }

            # This Line Is Explicitly Specifying The Type Of The Variable Model_Report As A Dictionary

            model_report: dict = evaluate_model(
                X_train, y_train, X_test, y_test, models
            )
            print(model_report)
            print(
                "\n====================================================================================\n"
            )
            logging.info(f"Model Report : {model_report}")

            # To Get Best Model Score From Dictionary

            ## This Extracts The Values (Performance Scores) From The Model_Report Dictionary
            ## This Sorts The Performance Scores In Ascending Order
            ## This Retrieves The Maximum Value, Which Corresponds To The Highest Performance Score

            ## This Extracts The Keys (Model Names) From The Model_Report Dictionary
            ## This Finds The Index Of The Maximum Value In The Sorted List Of Performance Scores

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            print(
                f"Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}"
            )
            print(
                "\n====================================================================================\n"
            )
            logging.info(
                f"Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}"
            )

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model,
            )

        except Exception as e:
            logging.info("Exception Occured At Model Training")
            raise CustomException(e, sys)
