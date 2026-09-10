import os 
import sys 
from dataclasses import dataclass 
import pandas as pd 
from sklearn.model_selection import train_test_split 
from src.exception import CustomException 
from src.logger import get_logger 
logger = get_logger(__name__) 

@dataclass 
class DataIngestionConfig:
    raw_data_path: str = os.path.join("artifacts" , "raw.csv") 
    train_data_path: str = os.path.join("artifacts" , "train.csv")
    test_data_path: str = os.path.join("artifacts" , "test.csv") 
    source_csv_path: str = os.path.join("notebook" , "data" , "covid_toy.csv") 


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig() 

    def initiate_data_ingestion(self):
        logger.info("Data Ingestion started....") 
        try:
            df = pd.read_csv(self.ingestion_config.source_csv_path) 
            logger.info(f"Data read successfullywith shape: {df.shape}") 
            os.makedirs(
                os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True
            )
            df.to_csv(self.ingestion_config.raw_data_path,index=False, header=True) 
            logger.info("Performing train-test-split") 
            train_set, test_set = train_test_split(
                df , test_size=0.2, random_state=42 , stratify=df['has_covid']
            )
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True) 
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True) 
            logger.info("Data Ingestion completed successfully...")
            logger.info("Jo log online class le rhe h , unko bhi congration , unka bhi data ingestion ho chuka h , leptop per apna hath rkh kr apne aap ko pawan kare.")
            logger.info("----------")
            logger.info("Jinka net nhi chl rha online me , unka bhi data ingestion complete")
            return {
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            }
        except Exception as e :
            raise CustomException(e,sys) 

if __name__ == "__main__":
    obj = DataIngestion() 
    obj.initiate_data_ingestion() 
 