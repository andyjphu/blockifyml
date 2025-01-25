import os
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

# Directory containing the CSV files
data_dir = "./coinScrapeData/"
results = []



# Iterate through all CSV files in the directory
for file_name in os.listdir(data_dir):
    if file_name.endswith(".csv"):
        symbol = file_name.split(".")[0]  # Extract symbol from the file name
        file_path = os.path.join(data_dir, file_name)
        print(f"Processing {file_name}...")

        try:
            # Load the dataset
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
            continue       
        
        # Extract and preprocess the text data
        if "Post Title" in df.columns:
            texts = [preprocess_text(text) for text in df["Post Title"].dropna() if len(text) > 10]
            
            # Classify each text
            sentiment_results = classifier(texts)
            
            # Count sentiment results
            bullish_count = sum(1 for r in sentiment_results if r["label"] == "Bullish")
            bearish_count = sum(1 for r in sentiment_results if r["label"] == "Bearish")
            neutral_count = sum(1 for r in sentiment_results if r["label"] == "Neutral")
            
            # Append results
            results.append({
                "Symbol": symbol,
                "Bullish": bullish_count,
                "Bearish": bearish_count,
                "Neutral": neutral_count,
            })
        else:
            print(f"Warning: No 'Post Title' column found in {file_name}")

# Save results to a CSV file
results_df = pd.DataFrame(results)
results_csv_path = "results.csv"
results_df.to_csv(results_csv_path, index=False)
print(f"Sentiment analysis results saved to {results_csv_path}")
