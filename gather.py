import praw
import pandas as pd
from datetime import datetime

# Initialize Reddit API
reddit = praw.Reddit(
    client_id="pUVm7A9U6tsiyxPLXKbpOg",  # Your client ID
    client_secret="TkKqUTg56ROnA5uxfpTQjirk0OLUdA",  # Your client secret
    user_agent="CryptoSentimentScraper by u/TraditionalWeird3416"  # Your user agent
)

# Check if Reddit instance is read-only
print("Read-only mode:", reddit.read_only)

# Search for "bitcoin" across all subreddits
search_query = "bitcoin"
search_results = reddit.subreddit("all").search(search_query, sort="new", limit=100)

# Collect results into a DataFrame
posts = []

for post in search_results:
    # Get comment mentions
    # comments = []
    # post.comments.replace_more(limit=0)  # Ensure all comments are retrieved
    # for comment in post.comments.list():
    #     if "bitcoin" in comment.body.lower():  # Check if "bitcoin" is mentioned in comments
    #         comments.append(comment.body)
    
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
        # "Bitcoin Mentions in Comments": comments
    })

# Convert to a pandas DataFrame
df = pd.DataFrame(posts)

# Display the DataFrame
print(df)

# Save to a CSV file for further analysis
df.to_csv("bitcoin_mentions_with_comments.csv", index=False)
print("Data saved to bitcoin_mentions_with_comments.csv")
