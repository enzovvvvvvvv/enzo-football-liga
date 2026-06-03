from google import genai
import tweepy
import schedule
import time
import os

# Configuration Gemini
client_gemini = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Configuration X/Twitter
client_x = tweepy.Client(
    consumer_key=os.environ.get("X_API_KEY"),
    consumer_secret=os.environ.get("X_API_SECRET"),
    access_token=os.environ.get("X_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("X_ACCESS_TOKEN_SECRET")
)

def generer_tweet():
    prompt = """Tu gères le compte X @EnzoFootballLiga spécialisé en comparaisons historiques Liga et Serie A.

Génère UN tweet en français avec une comparaison historique surprenante entre deux joueurs de Liga ou Serie A.

Règles :
- Maximum 280 caractères
- Commence par un emoji
- Inclus des stats précises et réelles
- Provoque le débat
- Termine par un hashtag court comme #Liga ou #SerieA
- PAS de guillemets autour du tweet

Exemples de style :
⚽ Ronaldinho à 24 ans : 15 buts 20 passes en Liga. Yamal au même âge : 18 buts 22 passes. La nouvelle légende est déjà là ? #Liga

🔥 Totti a joué 25 saisons en Serie A. Aucun joueur moderne ne dépasse 15. Le football a changé. #SerieA"""

    reponse = client_gemini.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    tweet = reponse.text.strip()

    if len(tweet) > 280:
        tweet = tweet[:277] + "..."

    try:
        client_x.create_tweet(text=tweet)
        print(f"Tweet posté : {tweet}")
    except Exception as e:
        print(f"Erreur X : {e}")

schedule.every().day.at("09:00").do(generer_tweet)

print("Agent EnzoFootballLiga démarré ✅")
generer_tweet()

while True:
    schedule.run_pending()
    time.sleep(60)
