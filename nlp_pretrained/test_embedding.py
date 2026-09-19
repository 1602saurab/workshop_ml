from nlp_pretrained.embedding import most_similar_words, word_similarity


print("=" * 60)
print("        GLOVE WORD EMBEDDING TEST")
print("=" * 60)


# Example 1: Find words similar to "king"
print("\nExample 1: Most similar words to 'king'")
result = most_similar_words("king", topn=5)

for word, score in result:
    print(f"{word:<15} -> {score:.4f}")


# Example 2: Find words similar to "computer"
print("\nExample 2: Most similar words to 'computer'")
result = most_similar_words("computer", topn=5)

for word, score in result:
    print(f"{word:<15} -> {score:.4f}")


# Example 3: Compare similarity between two words
print("\nExample 3: Similarity between 'king' and 'queen'")
score = word_similarity("king", "queen")

print(f"Similarity Score = {score:.4f}")


print("\n" + "=" * 60)
print("             TEST COMPLETED")
print("=" * 60)