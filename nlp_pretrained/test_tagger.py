from nlp_pretrained.ner_tagger import extract_entities


# Test 1
text1 = "Apple is in London"
result1 = extract_entities(text1)

print("Text:", text1)
print("Entities:", result1)
print()


# Test 2
text2 = "Barack Obama was born in Hawaii"
result2 = extract_entities(text2)

print("Text:", text2)
print("Entities:", result2)
print()


# Test 3
text3 = "Google was founded by Larry Page in California"
result3 = extract_entities(text3)

print("Text:", text3)
print("Entities:", result3)