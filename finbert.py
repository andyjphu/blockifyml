import pandas as pd

from transformers import pipeline

# Load a pretrained model
classifier = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")


# Collect results into a DataFrame
# Load results from CSV file
df_existing = pd.read_csv("bitcoin_mentions_with_comments.csv")

# Extract Post Titles from the existing DataFrame
existing_post_titles = df_existing["Post Title"].tolist()

texts = existing_post_titles


#print(texts)

# Classify each sample
results = classifier(texts)

# Process results
bullish_count = sum(1 for r in results if r['label'] == 'positive')
bearish_count = sum(1 for r in results if r['label'] == 'negative')

# Calculate percentages
bullish_percentage = (bullish_count / len(texts)) * 100
bearish_percentage = (bearish_count / len(texts)) * 100

print("bullish_percentage:", bullish_percentage)
print("bearish_percentage:", bearish_percentage)
# Output the results
if bullish_percentage > 60:
    print("Overall Sentiment: Bullish")
elif bearish_percentage > 60:
    print("Overall Sentiment: Bearish")
else:
    print("Overall Sentiment: Neutral")
