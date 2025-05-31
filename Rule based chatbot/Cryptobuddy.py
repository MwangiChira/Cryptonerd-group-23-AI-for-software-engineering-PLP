
# crypto database
crypto_db={
    "Bitcoin":{
        "price_trend":"rising",
        "market_gap":"high",
        "energy_use":"high",
        "sustainability_score":3/10
    },
    "Ethereum":{
        "price_trend":"stable",
        "market_cap":"high",
        "energy_use":"medium",
        "sustainability_score":6/10,

    },
    "Cardano":{
        "price_trend":"rising",
        "market_cap":"medium",
        "energy_use":"low",
        "sustainability_score":8/10,
    }
}


# CryptoBuddy Chatbot
def chatbot():
    print("Welcome to CryptoBuddy!")
    print("Ask me about trending, sustainable, or profitable cryptocurrencies.")
    print("Type 'exit' to quit.\n")

    while True:
        user_query = input("You: ").lower()

        if user_query == "exit":
            print("CryptoBuddy: Goodbye! Remember, crypto is risky — always do your own research!")
            break

        elif "sustainable" in user_query:
            best = max(crypto_db, key=lambda x: crypto_db[x]["sustainability_score"])
            print(f"CryptoBuddy: I recommend {best}! It has a high sustainability score of {crypto_db[best]['sustainability_score']*10}/10.")

        elif "trending up" in user_query or "rising" in user_query:
            rising_coins = [coin for coin in crypto_db if crypto_db[coin]["price_trend"] == "rising"]
            print(f"CryptoBuddy: These coins are trending up: {', '.join(rising_coins)}")

        elif "profitable" in user_query or "profit" in user_query:
            found = False
            for coin, data in crypto_db.items():
                if( data.get("price_trend")=="rising" and
                   data.get("market_cap")=="high"
                ):
                    print(f"CryptoBuddy: For profitability, consider {coin}. It's trending up with a high market cap.")
                    break
            else:
                print("CryptoBuddy: No coins currently meet the high-profitability rule.")

        elif "energy" in user_query or "eco" in user_query:
            eco_friendly = [coin for coin in crypto_db if crypto_db[coin]["energy_use"] == "low"]
            print(f"CryptoBuddy:These coins are energy-efficient: {', '.join(eco_friendly)}")

        elif "long-term" in user_query or "growth" in user_query or "viability" in user_query:
            for coin, data in crypto_db.items():
                if data["price_trend"] == "rising" and data["sustainability_score"] > 0.7 and data["energy_use"] == "low":
                    print(f"CryptoBuddy:{coin} is trending up and has a top-tier sustainability score. It’s great for long-term growth!")
                    break
            else:
                print("CryptoBuddy: I couldn't find a coin that meets all long-term growth criteria right now.")

        else:
            print("CryptoBuddy: Sorry, I didn’t get that. Try asking about 'sustainability', 'profitability', or 'long-term growth'.")

chatbot ()

