
from nlp_pretrained.embedding import most_similar_words , word_similarity 
from nlp_pretrained.ner_tagger import extract_entities , get_pos_tags 

if __name__ == "__main__":
    text = "I have fever for 3 days and I am from Mumbai" 
    print(get_pos_tags(text)) 
    print(extract_entities(text)) 
    print("Most similar words:" , most_similar_words("fever")) 
    print("Word similarity:" , word_similarity("fever" , "mumbai"))  