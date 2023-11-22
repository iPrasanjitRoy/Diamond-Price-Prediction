from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OrdinalEncoder

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

import sys, os
from dataclasses import dataclass
import pandas as pd
import numpy as np

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object


## Data Transformation Config


@dataclass
class DataTransformationconfig:
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")


## Data Transformation Class


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationconfig()

    def get_data_transformation_object(self):
        try:
            logging.info("Data Transformation Initiated")

            # Define Which Columns Should Be Ordinal-Encoded And Which Should Be Scaled
            categorical_cols = ["cut", "color", "clarity"]
            numerical_cols = ["carat", "depth", "table", "x", "y", "z"]

            # Define The Custom Ranking For Each Ordinal Variable
            cut_categories = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
            color_categories = ["D", "E", "F", "G", "H", "I", "J"]
            clarity_categories = [
                "I1",
                "SI2",
                "SI1",
                "VS2",
                "VS1",
                "VVS2",
                "VVS1",
                "IF",
            ]

            logging.info("Pipeline Initiated")

            # Numerical Pipeline
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            )

            # Categorigal Pipeline
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    (
                        "ordinalencoder",
                        OrdinalEncoder(
                            categories=[
                                cut_categories,
                                color_categories,
                                clarity_categories,
                            ]
                        ),
                    ),
                    ("scaler", StandardScaler()),
                ]
            )

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_cols),
                    ("cat_pipeline", cat_pipeline, categorical_cols),
                ]
            )

            return preprocessor

            logging.info("Pipeline Completed")

        except Exception as e:
            logging.info("Error In Data Trnasformation")
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            # Reading Train And Test Data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read Train And Test Data Completed")
            logging.info(f"Train Dataframe Head : \n{train_df.head().to_string()}")
            logging.info(f"Test Dataframe Head  : \n{test_df.head().to_string()}")

            logging.info("Obtaining Preprocessing Object")

            preprocessing_obj = self.get_data_transformation_object()

            target_column_name = "price"
            drop_columns = [target_column_name, "id"]

            ## Features Into Independent And Dependent Features

            input_feature_train_df = train_df.drop(columns=drop_columns, axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=drop_columns, axis=1)
            target_feature_test_df = test_df[target_column_name]

            ## Apply The Transformation

            input_feature_train_arr = preprocessing_obj.fit_transform(
                input_feature_train_df
            )
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            logging.info(
                "Applying Preprocessing Object On Training And Testing Datasets"
            )

            # np.c_ Function From NumPy Is Used To Concatenate The Transformed Input Features And Target Variables, Creating Arrays For Training And Testing Datasets

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            # Importing From Utils

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj,
            )

            logging.info("Processsor Pickle In Created And Saved")

            # self.data_transformation_config.preprocessor_obj_file_path : This Is The File Path Where The Preprocessor Object (Pipeline) Is Saved As A Pickle File

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            logging.info("Exception Occured In The Initiate_Datatransformation")

            raise CustomException(e, sys)
