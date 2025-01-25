import pandas as pd

# Load the dataset
df = pd.read_csv("bitcoin_mentions_with_comments.csv")

# Define keywords indicating an ad
ad_keywords = [
    "bonus", "referral", "earn free", "promotion", "signup", "get paid", 
    "promo code", "special offer", "cashback", "discount", "save", "coupon"
]

# Create a boolean mask to filter ads
df['is_ad'] = df['Post Text'].str.contains('|'.join(ad_keywords), case=False, na=False) | df['Post Title'].str.contains('|'.join(ad_keywords), case=False, na=False)

# Filter out ads
df_cleaned = df[~df['is_ad']].drop(columns=['is_ad'])

# Save cleaned dataset
df_cleaned.to_csv("reddit_posts_cleaned.csv", index=False)

print("Cleaned dataset saved to reddit_posts_cleaned.csv")
