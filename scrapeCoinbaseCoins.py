import praw
import pandas as pd
import os
from datetime import datetime

# Initialize Reddit API
reddit = praw.Reddit(
    client_id="pUVm7A9U6tsiyxPLXKbpOg",  # Your client ID
    client_secret="TkKqUTg56ROnA5uxfpTQjirk0OLUdA",  # Your client secret
    user_agent="CryptoSentimentScraper by u/TraditionalWeird3416"  # Your user agent
)

# Check if Reddit instance is read-only
print("Read-only mode:", reddit.read_only)

# Ensure the output folder exists
output_folder = "coinScrapeData"
os.makedirs(output_folder, exist_ok=True)

# Load the list of coins from the CSV file
coin_data = pd.read_csv("coinbaseCoins.csv")  # Assuming columns: Symbol,Name

# Iterate through each coin
for _, row in coin_data.iterrows():
    symbol = row["Symbol"]
    name = row["Name"]

    print(f"Processing {symbol} ({name})...")

    # Combine symbol and name into a single query
    search_query = f"{symbol} {name}"
    
    # Search for the coin in Reddit
    search_results = reddit.subreddit("all").search(search_query, sort="new", limit=100)
    
    posts = []
    
    for post in search_results:
        # Append post data
        posts.append({
            "Post Title": post.title,
            "Subreddit": post.subreddit.display_name,
            "Post ID": post.id,
            "Created Time": datetime.fromtimestamp(post.created_utc),  # Convert to readable datetime
            "Upvotes": post.score,
            "Upvote Ratio": post.upvote_ratio,
            "Comments Count": post.num_comments,
            "Post URL": post.url,
            "Author": post.author.name if post.author else None,
            "Flair": post.link_flair_text,
            "Post Text": post.selftext,
        })

    # Convert the data to a DataFrame
    df = pd.DataFrame(posts)

    # Save the data to a CSV file
    output_file = os.path.join(output_folder, f"{symbol}.csv")
    df.to_csv(output_file, index=False)
    print(f"Data for {symbol} saved to {output_file}")
