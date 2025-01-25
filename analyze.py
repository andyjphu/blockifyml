import pandas as pd
import re
from transformers import pipeline

# Initialize the CryptoBERT classifier
classifier = pipeline("sentiment-analysis", model="ElKulako/cryptobert")

# Preprocessing function to clean text
def preprocess_text(text):
    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Load the dataset
df_existing = pd.read_csv("bitcoin_mentions_with_comments.csv")

# Extract and preprocess the text data
existing_post_titles = df_existing["Post Title"].tolist()
texts = [preprocess_text(text) for text in existing_post_titles if text and len(text) > 10]  # Filter out invalid or short texts

# Classify each text
results = classifier(texts)


bullish_count = 0
bearish_count = 0
neutral_count = 0

# Debug: Print individual results
for idx, (text, result) in enumerate(zip(texts, results)):
    print(result["label"])
    if result["label"] == "Bullish":
        bullish_count += 1
    elif result["label"] == "Bearish":
        bearish_count += 1
    else:
        neutral_count += 1
        
    print(f"{idx + 1}. Text: {text}\nSentiment: {result['label']}, Score: {result['score']:.4f}\n")



# Calculate percentages
total = len(results)


if neutral_count > bullish_count and neutral_count > bearish_count:
    if bullish_count > bearish_count:
        print ("Slightly Bullish")
        
    elif bearish_count > bullish_count:
        print ("Slightly Bearish")
        
        
else:
    
    if bullish_count > bearish_count:
        print ("Bullish")
        
    elif bearish_count > bullish_count:
        print ("Bearish")
        
        
print("Bullish Samples:", bullish_count, "Bearish Samples:", bearish_count, "Neutral Samples:", neutral_count)
