import sys 
from nltk import ne_chunk, pos_tag , word_tokenize 
from src.exception import CustomException 
from src.logger import get_logger 
logger = get_logger(__name__) 

# Apple is in London ---> if I perform NER ---> (Apple= 'Orgam=nization') , ('London' = GPE (Location))

def get_pos_tags(text:str):
    try:
        tokens = word_tokenize(text) 
        return pos_tag(tokens) 
    except Exception as e :
        raise CustomException(e, sys) 

def extract_entities(text:str):
    try:
        tagged = get_pos_tags(text) 
        tree = ne_chunk(tagged) 
        entities = {"GPE":[] , "PERSON": [] , "ORGANIZATION":[]}
        for i in tree:
            if hasattr(i, "label"):
                label = i.label() 
                entity_text = " ".join(word for word, _ in i) 
                if label in entities:
                    entities[label].append(entity_text) 
        logger.info(f"NLTK pretrained NER extracted from '{text}' : {entities}") 
        return entities 

    except Exception as e :
        raise CustomException(e,sys) 
