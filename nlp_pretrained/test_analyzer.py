from nlp_pretrained.sentiment_analyzer import analyze_sentiment


print("=" * 60)
print("           VADER SENTIMENT ANALYZER TEST")
print("=" * 60)


# Example 1: Positive sentence
print("\nExample 1: Positive Sentence")
text = "I absolutely love this product. It is amazing!"
result = analyze_sentiment(text)

print(f"Text       : {text}")
print(f"Positive   : {result['pos']:.3f}")
print(f"Negative   : {result['neg']:.3f}")
print(f"Neutral    : {result['neu']:.3f}")
print(f"Compound   : {result['compound']:.3f}")
print(f"Urgency    : {result['urgency_hint']}")


# Example 2: Negative sentence
print("\nExample 2: Negative Sentence")
text = "This service is terrible. I am extremely disappointed."
result = analyze_sentiment(text)

print(f"Text       : {text}")
print(f"Positive   : {result['pos']:.3f}")
print(f"Negative   : {result['neg']:.3f}")
print(f"Neutral    : {result['neu']:.3f}")
print(f"Compound   : {result['compound']:.3f}")
print(f"Urgency    : {result['urgency_hint']}")


# Example 3: Neutral sentence
print("\nExample 3: Neutral Sentence")
text = "The meeting is scheduled for Monday at 10 AM."
result = analyze_sentiment(text)

print(f"Text       : {text}")
print(f"Positive   : {result['pos']:.3f}")
print(f"Negative   : {result['neg']:.3f}")
print(f"Neutral    : {result['neu']:.3f}")
print(f"Compound   : {result['compound']:.3f}")
print(f"Urgency    : {result['urgency_hint']}")


print("\n" + "=" * 60)
print("                TEST COMPLETED")
print("=" * 60)