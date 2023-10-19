from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
from typing import Dict
from typing import List
import json

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

    def insert_noticias_to_db(self, noticia: Dict):
        try:
            self.connect()
            if self.client:
                db = self.client["crawler"]
                collection = db.get_collection("bahianews")

                if not collection.find_one({'titulo': noticia['titulo']}):
                    collection.insert_one(noticia)
                    print(f"Notícia com título '{noticia['titulo']}' inserida no banco de dados.")
                else:
                    print(f"Notícia com título '{noticia['titulo']}' já existe no banco de dados. Não foi inserida novamente.")

        except Exception as e:
            print(f"Erro ao inserir notícias no banco de dados: {e}")
        finally:
            self.close()


    def close(self):
        if self.client:
            self.client.close()

    # Função para buscar notícias por data
    def find_noticias_by_data(self, date: str) -> List[Dict]:
        try:
            self.connect()
            if self.client:
                db = self.client["crawler"]
                collection = db.get_collection("bahianews")
                # Encontra notícias com a data especificada
                noticias = list(collection.find({'data': date}))
                if not noticias:
                    print(f"Nenhuma notícia encontrada no BD para a data ({date}).")
                else:
                    print(f"Notícias encontradas no BD para a data ({date}):")
                    for noticia in noticias:
                        print(noticia['titulo'])
                return noticias
        except Exception as e:
            print(f"Erro ao buscar notícias por data: {e}")
        finally:
            self.close()
        return []

    # Função para buscar notícias em uma faixa de datas
    def find_noticias_in_date_range(self, date_inicio: str, date_fim: str) -> List[Dict]:
        try:
            self.connect()
            if self.client:
                db = self.client["crawler"]
                collection = db.get_collection("bahianews")
                # Encontra notícias com datas dentro do intervalo especificado
                noticias = list(collection.find({
                    'data': {'$gte': date_inicio, '$lte': date_fim}
                }))
                
                if not noticias:
                    print(f"Nenhuma notícia encontrada no BD no intervalo de datas ({date_inicio} a {date_fim}).")
                else:
                    print(f"Notícias encontradas no BD no intervalo de datas ({date_inicio} a {date_fim}):")
                    for noticia in noticias:
                        print(noticia['titulo'])
                
                return noticias
        except Exception as e:
            print(f"Erro ao buscar notícias no BD na faixa de datas: {e}")
        finally:
            self.close()
        return []