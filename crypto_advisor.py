import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime

# Download NLTK data (only needed first time)
nltk.download('punkt_tab')
nltk.download('stopwords')

class CryptoAdvisor:
    def __init__(self):
        # Initialize with some static data that can be supplemented by API
        self.crypto_db = {
            "Bitcoin": {
                "price_trend": "rising",
                "market_cap": "high",
                "energy_use": "high",
                "sustainability_score": 3/10,
                "last_updated": None
            },
            "Ethereum": {
                "price_trend": "stable",
                "market_cap": "high",
                "energy_use": "medium",
                "sustainability_score": 6/10,
                "last_updated": None
            },
            "Cardano": {
                "price_trend": "rising",
                "market_cap": "medium",
                "energy_use": "low",
                "sustainability_score": 8/10,
                "last_updated": None
            }
        }
        
        # CoinGecko API endpoint
        self.api_url = "https://api.coingecko.com/api/v3"
        
        # Preprocess stopwords for NLP
        self.stop_words = set(stopwords.words('english'))
        
        # Disclaimer
        self.disclaimer = "\n⚠️ Disclaimer: Crypto is risky—always do your own research! ⚠️"
    
    def fetch_real_time_data(self, coin_id):
        """Fetch real-time data from CoinGecko API"""
        try:
            endpoint = f"{self.api_url}/coins/{coin_id.lower()}"
            response = requests.get(endpoint)
            data = response.json()
            
            # Update our database with real-time data
            if coin_id in self.crypto_db:
                # Simple trend analysis based on price change percentage
                price_change = data.get('market_data', {}).get('price_change_percentage_24h', 0)
                if price_change > 5:
                    trend = "rising rapidly"
                elif price_change > 0:
                    trend = "rising"
                elif price_change < -5:
                    trend = "falling rapidly"
                elif price_change < 0:
                    trend = "falling"
                else:
                    trend = "stable"
                
                # Market cap categorization
                market_cap = data.get('market_data', {}).get('market_cap', {}).get('usd', 0)
                if market_cap > 10000000000:  # > $10B
                    cap_category = "high"
                elif market_cap > 1000000000:  # > $1B
                    cap_category = "medium"
                else:
                    cap_category = "low"
                
                # Update the database
                self.crypto_db[coin_id].update({
                    "price_trend": trend,
                    "market_cap": cap_category,
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
            return True
        except Exception as e:
            print(f"Error fetching data for {coin_id}: {e}")
            return False
    
    def preprocess_query(self, user_query):
        """Process the user query using NLP techniques"""
        # Tokenize and remove stopwords
        tokens = word_tokenize(user_query.lower())
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        return filtered_tokens
    
    def generate_advice(self, tokens):
        """Generate investment advice based on processed query tokens"""
        advice = ""
        
        # Check for sustainability-related terms
        sustainability_terms = {'sustainable', 'eco', 'environment', 'green', 'energy', 'earth'}
        if any(term in tokens for term in sustainability_terms):
            recommend = max(self.crypto_db.keys(), 
                          key=lambda x: self.crypto_db[x]["sustainability_score"])
            score = self.crypto_db[recommend]["sustainability_score"]
            advice += (f"Based on sustainability, invest in {recommend}! 🌱\n"
                       f"Sustainability score: {score*10}/10\n"
                       f"Energy usage: {self.crypto_db[recommend]['energy_use']}\n")
        
        # Check for profitability-related terms
        profit_terms = {'profit', 'gain', 'earn', 'money', 'return', 'investment'}
        if any(term in tokens for term in profit_terms):
            # Filter coins with rising trend and high market cap
            profitable_coins = [
                coin for coin in self.crypto_db 
                if self.crypto_db[coin]["price_trend"] in ("rising", "rising rapidly") 
                and self.crypto_db[coin]["market_cap"] == "high"
            ]
            
            if profitable_coins:
                advice += "\nFor short-term profitability consider:\n"
                for coin in profitable_coins:
                    advice += (f"- {coin}: Trend: {self.crypto_db[coin]['price_trend'].title()}, "
                              f"Market Cap: {self.crypto_db[coin]['market_cap'].title()}\n")
            else:
                advice += "\nNo coins currently meet strict profitability criteria.\n"
        
        # Check for general advice request
        if not advice or any(term in tokens for term in {'advice', 'suggest', 'recommend'}):
            if not advice:
                # No specific criteria, give balanced recommendation
                balanced_rec = max(self.crypto_db.keys(), 
                                 key=lambda x: (self.crypto_db[x]["sustainability_score"] * 0.6 + 
                                               (1 if self.crypto_db[x]["price_trend"] in ("rising", "rising rapidly") else 0) * 0.4))
                
                advice = (f"For a balanced investment, consider {balanced_rec}:\n"
                         f"- Sustainability: {self.crypto_db[balanced_rec]['sustainability_score']*10}/10\n"
                         f"- Price Trend: {self.crypto_db[balanced_rec]['price_trend'].title()}\n"
                         f"- Market Cap: {self.crypto_db[balanced_rec]['market_cap'].title()}\n")
            
            # Add general market overview
            rising_coins = [coin for coin in self.crypto_db 
                          if "rising" in self.crypto_db[coin]["price_trend"]]
            falling_coins = [coin for coin in self.crypto_db 
                           if "falling" in self.crypto_db[coin]["price_trend"]]
            
            advice += "\nMarket Overview:\n"
            advice += f"- Rising coins: {', '.join(rising_coins) if rising_coins else 'None'}\n"
            advice += f"- Falling coins: {', '.join(falling_coins) if falling_coins else 'None'}\n"
        
        return advice + self.disclaimer
    
    def chat(self):
        """Main chat loop"""
        print("Welcome to Crypto Investment Advisor! (Type 'exit' to quit)")
        
        while True:
            user_query = input("\nHow can I help with your crypto investments? > ")
            
            if user_query.lower() == 'exit':
                print("Goodbye! Remember to diversify your investments.")
                break
            
            # Update data for all coins before processing query
            for coin in self.crypto_db.keys():
                self.fetch_real_time_data(coin)
            
            # Process query and generate response
            tokens = self.preprocess_query(user_query)
            response = self.generate_advice(tokens)
            
            print("\n" + response)

# Run the chatbot
if __name__ == "__main__":
    advisor = CryptoAdvisor()
    advisor.chat()