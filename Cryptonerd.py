# Cryptonerd - A Rule-Based Cryptocurrency Investment Chatbot
# Author: Mwangi Chira
# Description: A friendly chatbot that provides crypto investment advice based on profitability and sustainability

import re
import random
# import nltk
# from nltk.tokenize import word_tokenize

class Cryptonerd:
    def __init__(self):
        """Initialize the Cryptonerd chatbot with personality and data"""
        self.name = "Cryptonerd"
        
        # Predefined cryptocurrency database
        self.crypto_db = {
            "Bitcoin": {
                "symbol": "BTC",
                "price_trend": "rising",
                "market_cap": "high",
                "energy_use": "high",
                "sustainability_score": 3,
                "description": "The original cryptocurrency, but energy-intensive"
            },
            "Ethereum": {
                "symbol": "ETH",
                "price_trend": "stable",
                "market_cap": "high",
                "energy_use": "medium",
                "sustainability_score": 6,
                "description": "Smart contract platform with improving efficiency"
            },
            "Cardano": {
                "symbol": "ADA",
                "price_trend": "rising",
                "market_cap": "medium",
                "energy_use": "low",
                "sustainability_score": 8,
                "description": "Research-driven, eco-friendly blockchain"
            },
            "Solana": {
                "symbol": "SOL",
                "price_trend": "rising",
                "market_cap": "medium",
                "energy_use": "low",
                "sustainability_score": 7,
                "description": "Fast and energy-efficient blockchain"
            },
            "Dogecoin": {
                "symbol": "DOGE",
                "price_trend": "volatile",
                "market_cap": "medium",
                "energy_use": "medium",
                "sustainability_score": 4,
                "description": "Meme coin with community support"
            }
        }
        
        # Greeting messages
        self.greetings = [
            "Hey there! 🚀 I'm Cryptonerd, your friendly crypto advisor!",
            "Welcome to the crypto universe! 💎 Ready to explore some coins?",
            "Greetings, future crypto millionaire! 🌟 Let's find your perfect match!"
        ]
        
        # Farewell messages
        self.farewells = [
            "Happy investing! 🚀 Remember: DYOR (Do Your Own Research)!",
            "May the crypto gods be with you! 💎 Stay safe out there!",
            "Until next time, crypto warrior! 🌟 Don't forget - only invest what you can afford to lose!"
        ]

    def greet(self):
        """Display a random greeting message"""
        return random.choice(self.greetings)

    def farewell(self):
        """Display a random farewell message"""
        return random.choice(self.farewells)

    def get_sustainable_crypto(self):
        """Find the most sustainable cryptocurrency"""
        best_crypto = max(self.crypto_db, key=lambda x: self.crypto_db[x]["sustainability_score"])
        score = self.crypto_db[best_crypto]["sustainability_score"]
        return f"🌱 **{best_crypto} ({self.crypto_db[best_crypto]['symbol']})** is your best bet for sustainability!\n" \
               f"Sustainability Score: {score}/10\n" \
               f"Why: {self.crypto_db[best_crypto]['description']}"

    def get_profitable_crypto(self):
        """Find cryptocurrencies with rising trends and high market cap"""
        profitable_coins = []
        for crypto, data in self.crypto_db.items():
            if data["price_trend"] == "rising" and data["market_cap"] in ["high", "medium"]:
                profitable_coins.append(crypto)
        
        if profitable_coins:
            recommendations = "\n".join([f"• **{coin} ({self.crypto_db[coin]['symbol']})** - {self.crypto_db[coin]['description']}" 
                                       for coin in profitable_coins])
            return f"📈 **Rising Stars for Profitability:**\n{recommendations}"
        else:
            return "🤔 Hmm, the market seems uncertain right now. Consider waiting for better trends!"

    def get_balanced_recommendation(self):
        """Find crypto that balances profitability and sustainability"""
        best_crypto = None
        best_score = 0
        
        for crypto, data in self.crypto_db.items():
            # Calculate composite score (profitability + sustainability)
            profit_score = 3 if data["price_trend"] == "rising" else 1
            market_score = 2 if data["market_cap"] == "high" else 1
            sustainability_score = data["sustainability_score"]
            
            composite_score = (profit_score + market_score + sustainability_score) / 3
            
            if composite_score > best_score:
                best_score = composite_score
                best_crypto = crypto
        
        if best_crypto:
            return f"⚖️ **Best Balanced Choice: {best_crypto} ({self.crypto_db[best_crypto]['symbol']})**\n" \
                   f"Composite Score: {best_score:.1f}/5\n" \
                   f"Why: {self.crypto_db[best_crypto]['description']}\n" \
                   f"Sustainability: {self.crypto_db[best_crypto]['sustainability_score']}/10"

    def get_crypto_info(self, crypto_name):
        """Get detailed information about a specific cryptocurrency"""
        # Check if the crypto exists in our database (case-insensitive)
        crypto_key = None
        for key in self.crypto_db.keys():
            if key.lower() == crypto_name.lower() or self.crypto_db[key]['symbol'].lower() == crypto_name.lower():
                crypto_key = key
                break
        
        if crypto_key:
            data = self.crypto_db[crypto_key]
            return f"📊 **{crypto_key} ({data['symbol']}) Analysis:**\n" \
                   f"• Price Trend: {data['price_trend'].title()} {'📈' if data['price_trend'] == 'rising' else '📊' if data['price_trend'] == 'stable' else '⚠️'}\n" \
                   f"• Market Cap: {data['market_cap'].title()}\n" \
                   f"• Energy Use: {data['energy_use'].title()}\n" \
                   f"• Sustainability Score: {data['sustainability_score']}/10 🌱\n" \
                   f"• Description: {data['description']}"
        else:
            return f"🤷‍♂️ Sorry, I don't have data on '{crypto_name}' yet. Try Bitcoin, Ethereum, Cardano, Solana, or Dogecoin!"

    def analyze_query(self, user_input):
        """Main logic to analyze user queries and provide appropriate responses"""
        # Convert to lowercase for easier matching
        query = user_input.lower()
        
        # Remove common words and clean the query
        query = re.sub(r'\b(the|a|an|is|are|what|which|how|can|you|should|i|me|my)\b', '', query)
        query = query.strip()
        
        # Rule-based response logic
        if any(word in query for word in ['hi', 'hello', 'hey', 'greet', 'start']):
            return self.greet() + "\n\n💡 Ask me about:\n• Sustainable cryptos\n• Profitable investments\n• Specific coin analysis\n• Balanced recommendations"
        
        elif any(word in query for word in ['bye', 'goodbye', 'exit', 'quit', 'thanks', 'thank you']):
            return self.farewell()
        
        elif any(word in query for word in ['sustainable', 'green', 'eco', 'environment', 'energy']):
            return self.get_sustainable_crypto() + "\n\n⚠️ **Disclaimer:** Crypto investments are risky. Always do your own research!"
        
        elif any(word in query for word in ['profit', 'money', 'rising', 'trending', 'growing', 'gains']):
            return self.get_profitable_crypto() + "\n\n⚠️ **Disclaimer:** Past performance doesn't guarantee future results!"
        
        elif any(word in query for word in ['balanced', 'best', 'recommend', 'advice', 'suggest']):
            return self.get_balanced_recommendation() + "\n\n⚠️ **Disclaimer:** This is not financial advice. Invest responsibly!"
        
        elif any(word in query for word in ['bitcoin', 'btc', 'ethereum', 'eth', 'cardano', 'ada', 'solana', 'sol', 'dogecoin', 'doge']):
            # Extract the crypto name from the query
            for crypto in self.crypto_db:
                if crypto.lower() in query or self.crypto_db[crypto]['symbol'].lower() in query:
                    return self.get_crypto_info(crypto) + "\n\n⚠️ **Disclaimer:** Always verify information from multiple sources!"
        
        elif any(word in query for word in ['help', 'what can you do', 'commands']):
            return "🤖 **I can help you with:**\n" \
                   "• Find sustainable cryptocurrencies 🌱\n" \
                   "• Identify profitable trends 📈\n" \
                   "• Get balanced investment recommendations ⚖️\n" \
                   "• Analyze specific coins (Bitcoin, Ethereum, Cardano, Solana, Dogecoin) 📊\n\n" \
                   "**Try asking:** 'What's the most sustainable crypto?' or 'Tell me about Bitcoin'"
        
        else:
            return "🤔 I'm not sure I understand. Try asking about:\n" \
                   "• 'What's the most sustainable crypto?'\n" \
                   "• 'Which coins are profitable?'\n" \
                   "• 'Tell me about Ethereum'\n" \
                   "• 'Give me a balanced recommendation'\n" \
                   "• Type 'help' for more options!"

def main():
    """Main function to run the chatbot"""
    print("=" * 60)
    print("🚀 WELCOME TO CRYPTONERD CHATBOT 🚀")
    print("=" * 60)
    
    # Initialize the chatbot
    bot = Cryptonerd()
    
    # Display initial greeting
    print(bot.greet())
    print("\n💡 Type 'help' to see what I can do, or 'bye' to exit.\n")
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check if user wants to exit
            if user_input.lower() in ['bye', 'goodbye', 'exit', 'quit']:
                print(f"\n{bot.name}: {bot.farewell()}")
                break
            
            # Skip empty inputs
            if not user_input:
                print(f"\n{bot.name}: 🤔 You didn't say anything! Try asking me about crypto!")
                continue
            
            # Get bot response
            response = bot.analyze_query(user_input)
            print(f"\n{bot.name}: {response}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n{bot.name}: {bot.farewell()}")
            break
        except Exception as e:
            print(f"\n{bot.name}: 🤖 Oops! Something went wrong. Let's try again!")
            print(f"Error: {str(e)}")

# Run the chatbot
if __name__ == "__main__":
    main()