from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
from typing import Dict
from typing import List

class Database:
    
    def __init__(self):
        load_dotenv()
        self.client = None

    def connect(self):
        try:
            self.client = MongoClient(os.getenv("DB_URI"))
            # Verifica a conexão bem-sucedida enviando um ping
            self.client.admin.command('ping')
        except Exception as e:
            print(e)

    def insert_noticias_to_db(self, noticia: Dict) -> True | False:
        try:
            self.connect()
            if self.client:
                db = self.client[os.getenv("DB_DATABASE")]
                collection = db.get_collection(os.getenv("DB_COLLECTION"))

                if not collection.find_one({'titulo': noticia['titulo']}):
                    collection.insert_one(noticia)
                    print(f"Notícia com título '{noticia['titulo']}' inserida no banco de dados.")
                    return True
                else:
                    print(f"Sem notícias novas...")
                    return False

        except Exception as e:
            print(f"Erro ao inserir notícias no banco de dados: {e}")
            return False
        finally:
            self.close()


    def close(self):
        if self.client:
            self.client.close()