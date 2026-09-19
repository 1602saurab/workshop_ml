# Text ---> polarity score ---> decide setence behaviour(po,neg, neutral) 

import sys 
from nltk.sentiment import SentimentIntensityAnalyzer 
from src.exception import CustomException 
from src.logger import get_logger 
logger = get_logger(__name__) 
_analyzer = None 

def _get_analyzer():
    global _analyzer 
    if _analyzer is None:
        _analyzer = SentimentIntensityAnalyzer() 
    return _analyzer 

def analyze_sentiment(text: str):
    try:
        sia = _get_analyzer() 
        scores = sia.polarity_scores(text) 
        if scores["compound"] <= -0.5:
            urgency_hint = "High" 
        elif scores["compound"] <=  -0.15:
            urgency_hint = "Medium"
        else:
            urgency_hint = "Low" 

        result = {**scores , "urgency_hint": urgency_hint}
        logger.info(f"VADER sentiment for '{text}' : {result}") 
        return result 
    except Exception as e :
        raise CustomException(e,sys)  
 