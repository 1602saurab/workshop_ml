import sys 
from src.components.data_ingestion import DataIngestion 
from src.components.data_transformation import DataTransformation 
from src.components.model_trainer import ModelTrainer 
from src.exception import CustomException 
from src.logger import get_logger 
logger = get_logger(__name__) 

def run_training_pipeline():
    try:
        logger.info("TRAINING PIPELINE STARTED....") 
        #Data Ingestion 
        data_ingestion = DataIngestion() 
        train_path, test_path = data_ingestion.initiate_data_ingestion() 

        #data transformation 
        data_transformation = DataTransformation() 
        train_arr, test_arr , _ = data_transformation.initiate_data_transformation(train_path, test_path)


        #Model training 
        model_trainer = ModelTrainer() 
        best_model_name, best_model_score = model_trainer.initiate_model_trainer(train_arr, test_arr) 

        logger.info(f"TRAINING PIPELINE COMPLETED | BEST MODEL: {best_model_name}, Accuracy: {best_model_score:.2f}") 
        print(f"Training Complete. Best Model: {best_model_name}(accuracy = {best_model_score:.2f})") 
    except Exception as e :
        raise CustomException(e,sys) 

if __name__ == "__main__":
    run_training_pipeline()