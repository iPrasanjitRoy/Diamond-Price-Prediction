import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass


## Intialize The Data Ingestion Configuration


## DataIngestionconfig IS A Data Class Created Using The Dataclass Decorator From The Dataclasses Module
## It Has Three Class Variables With Default Values Representing File Paths For Training, Testing, And Raw Data
## Data Classes Are A Feature Introduced In Python 3.7 That Provides A Decorator (@dataclass) For Quickly And Concisely Creating Classes Primarily Meant To Store Data


@dataclass
class DataIngestionconfig:
    train_data_path = os.path.join("artifacts", "train.csv")
    test_data_path = os.path.join("artifacts", "test.csv")
    raw_data_path = os.path.join("artifacts", "raw.csv")


## Create A Data Ingestion Class

## DataIngestion IS A Class That Handles The Data Ingestion Process
## It Initializes An Instance Of DataIngestionConfig In Its Constructor
## The Initiate_Data_Ingestion Method Performs Reads A CSV File, Saves The Raw Dataset, Splits The Dataset Into Training And Testing, Saves The Training And Testing Sets To  CSV Files

## os.path.dirname Gives You The Directory In Which The Raw Data File Will Be Stored


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionconfig()

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion Method Starts")

        try:
            df = pd.read_csv(os.path.join("notebooks/data", "gemstone.csv"))
            logging.info("Dataset Read AS Pandas Dataframe")

            os.makedirs(
                os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True
            )

            df.to_csv(self.ingestion_config.raw_data_path, index=False)

            logging.info("Train Test Split")
            train_set, test_set = train_test_split(df, test_size=0.30, random_state=42)

            train_set.to_csv(
                self.ingestion_config.train_data_path, index=False, header=True
            )
            test_set.to_csv(
                self.ingestion_config.test_data_path, index=False, header=True
            )

            logging.info("Ingestion Of Data IS Completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            logging.info("Error Occured In Data Ingestion Config")
