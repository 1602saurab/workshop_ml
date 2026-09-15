import os 
import sys 
import pickle 
from sklearn.metrics import accuracy_score 
from src.exception import CustomException 
from src.logger import get_logger 
logger = get_logger(__name__) 

def save_object(file_path: str , obj):
    try:
        dir_path = os.path.dirname(file_path) 
        os.makedirs(dir_path , exist_ok=True) 
        with open(file_path , "wb") as file_obj:
            pickle.dump(obj, file_obj) 
        logger.info(f"Object saved successfully at : {file_path}") 
    except Exception as e : 
        raise CustomException(e,sys) 

def load_object(file_path: str):
    try:
        with open(file_path , "rb") as file_obj:
            return pickle.load(file_obj) 
    except Exception as e : 
        raise CustomException(e,sys) 

def evaluate_models(X_train, y_train , X_test , y_test, models:dict):
    try:
        report = {} 
        for model_name , model in models.items():
            model.fit(X_train , y_train) 
            y_pred = model.predict(X_test) 
            test_accuracy = accuracy_score(y_test , y_pred) 
            report[model_name]  = test_accuracy 
            logger.info(f"{model_name} -> Test Accuracy: {test_accuracy:.2f}")
        return report 
    except Exception as e : 
        raise CustomException(e,sys)  

##All done 