import os 
import sys 
from dataclasses import dataclass 
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier 
import pandas as pd 
from src.exception import CustomException 
from src.logger import get_logger 
logger = get_logger(__name__) 
from src.utils import evaluate_models, load_object, save_object 

@dataclass 
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl") 

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig() 
    def initiate_model_trainer(self, train_array , test_array):
        try:
            logger.info("Spliting train and test input data")
            X_train,y_train, X_test , y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1] 
            )
            models = {
                "LogisiticRegression": LogisticRegression(max_iter=100),
                "DecisionTree": DecisionTreeClassifier(random_state=42),
                "RandomForest":RandomForestClassifier(random_state=42, n_estimators=50),
                "KNeighboursClassifier":KNeighborsClassifier(n_neighbors=5) 
            }
            model_report: dict = evaluate_models(
                X_train, y_train , X_test , y_test,models
            )

            best_model_score = max(model_report.values()) 
            best_model_name = max(model_report, key= model_report.get) 
            best_model = models[best_model_name] 
            logger.info(f"Best Model saved as model.pkl ::: {best_model_name}") 
            save_object(
             file_path=self.model_trainer_config.trained_model_file_path,obj=best_model)
            logger.info(f"Best Model saved: {best_model_name}") 
            return best_model_name, best_model_score

            
        except Exception as e :
            raise CustomException(e,sys) 

