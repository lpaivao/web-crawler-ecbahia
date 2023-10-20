import tweepy
import os
import gdown
from dotenv import load_dotenv

class Bot:

    def __init__(self) -> None:

        load_dotenv()
        consumer_key = os.getenv("CONSUMER_KEY")
        consumer_key_secret = os.getenv("CONSUMER_KEY_SECRET")
        access_token = os.getenv("ACCESS_TOKEN")
        access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
        bearer_token = os.getenv("BEARER_TOKEN")

        self.client = tweepy.Client(
            consumer_key= consumer_key,
            consumer_secret= consumer_key_secret,
            access_token= access_token,
            access_token_secret= access_token_secret,
            bearer_token= bearer_token
        )

        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_key_secret)

        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)

    def post(self, noticia: dict):
        
        try:

            image_link = noticia['imagem']

            media = None

            if image_link != "":
                path = f"/tmp/{str(noticia['data'])}.jpg"
                gdown.download(image_link, path)
                media = self.api.media_upload(filename=path)
            
            
            post = f"📢 {noticia['titulo']}\n\n📌 {noticia['chamada']}\n\n🔗 Veja mais: {noticia['link']}"

            if media is not None:
                self.client.create_tweet(text=post, media_ids=[media.media_id])
            else:
                self.client.create_tweet(text=post)

            print("Notícia postada no Twitter com sucesso!")
            return True

        except Exception as e:
            print(f"Erro ao tentar postar: {e}")
            return False