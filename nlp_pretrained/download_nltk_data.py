import nltk 
import sys 
from src.logger import get_logger 
logger = get_logger(__name__) 
from src.exception import CustomException 
REQUIRED_RESOURCES = [
    "punkt", ##it is used for sentence/word based tokenization
    "punkt_tab",  ## This is newer version of tokenization 
    "averaged_perceptron_tagger", ## This is used for POS-TAGGING
    "averaged_perceptron_tagger_eng" , ##This is newer version of POS-TAGGER 
    "maxnet_ne_chunker" , ## THIS IS FOR NER(NAMED ENTITY RECOGNITION) 
    "maxnet_ne_chunker_tab", ## This is newer version of NER
    "words", ## this is used for convert our word into Lexical format . 
    "vader_lexicon",## This is is used for sentiment analysis(text = positive , negative , neutral) 
    "stopwords" , ## it will provide common stopword list[the, is. a, an ,of ,and] 
    "wordnet" , ## this is used for understanding the relationship of context . 
]

if __name__ == "__main__":
    logger.info("Downloading NLTK pretrained models/data....")
    print("Downloading NLTK pretrained models/data....")
    for i in REQUIRED_RESOURCES:
        try:
            nltk.download(i) 
            
        except Exception as e :
            raise CustomException(e,sys) 
    logger.info("All models download")