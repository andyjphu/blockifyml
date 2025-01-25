import requests

def get_coinbase_coins_with_names():
    # API endpoint for Coinbase Pro currencies
    url = "https://api.exchange.coinbase.com/currencies"
    
    try:
        # Make the request
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse JSON response
        currencies = response.json()
        
        # Extract coin symbols and their full names
        coins_with_names = {
            currency["id"]: currency.get("name", "Unknown")
            for currency in currencies
        }
        
        print(f"Total Coins Available: {len(coins_with_names)}")
        return coins_with_names
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {}

# Get the coins with names
coins_with_names = get_coinbase_coins_with_names()

# Print the coins and their names
print("Coins on Coinbase with Names:")
for symbol, name in coins_with_names.items():
    print(f"{symbol},{name}")
