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

    def insert_noticias_to_db(self, json_data: Dict):
        try:
            self.connect()
            if self.client:
                db = self.client["crawler"]
                collection = db.get_collection("bahianews")
                
                # Percorre as chaves de data no JSON
                for data, noticias in json_data.items():
                    # Verifica se já existem notícias com a mesma data no banco de dados
                    if not collection.find_one({'data': data}):
                        # Se não existir, insere as notícias
                        collection.insert_one({'data': data, 'noticias': noticias})
                        print(f"Notícias para a data {data} inseridas no banco de dados.")
                    else:
                        print(f"Notícias para a data {data} já existem no banco de dados. Não foram inseridas.")
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
                    print(noticias)
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
                    print(noticias)
                
                return noticias
        except Exception as e:
            print(f"Erro ao buscar notícias no BD na faixa de datas: {e}")
        finally:
            self.close()
        return []