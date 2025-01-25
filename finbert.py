import pandas as pd
import re
from transformers import pipeline

# Initialize the FinBERT classifier
classifier = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")
#classifier = pipeline("ElKulako/cryptobert")

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

# Debug: Print individual results
for idx, (text, result) in enumerate(zip(texts, results)):
    print(result)
    print(f"{idx + 1}. Text: {text}\nSentiment: {result['label']}, Score: {result['score']}\n")

# Count sentiments with thresholds
neutral_threshold = 0.6  # Example threshold for neutral classification
bullish_count = sum(1 for r in results if r['label'] == 'positive' and r['score'] > neutral_threshold)
bearish_count = sum(1 for r in results if r['label'] == 'negative' and r['score'] > neutral_threshold)
neutral_count = len(results) - bullish_count - bearish_count

# Calculate percentages
total = len(results)
bullish_percentage = (bullish_count / total) * 100
bearish_percentage = (bearish_count / total) * 100
neutral_percentage = (neutral_count / total) * 100

# Output the results
print(f"bullish_percentage: {bullish_percentage:.2f}")
print(f"bearish_percentage: {bearish_percentage:.2f}")
print(f"neutral_percentage: {neutral_percentage:.2f}")

if bullish_percentage > 60:
    print("Overall Sentiment: Bullish")
elif bearish_percentage > 60:
    print("Overall Sentiment: Bearish")
else:
    print("Overall Sentiment: Neutral")
