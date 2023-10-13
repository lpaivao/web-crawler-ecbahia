import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from database import Database

# Links para os sites de notícias
link_ecBahia = 'https://www.ecbahia.com/noticias-do-bahia'
link_geBahia = 'https://ge.globo.com/ba/futebol/times/bahia/'
link_bahiaNoticias = 'https://www.bahianoticias.com.br/esportes/bahia'

# Pasta onde serão salvos os arquivos JSON das notícias
caminho_pasta_json = '../json'

# Nomes do arquivo json
nome_json_noticias = 'noticias.json'

class Crawler:

    # Função que faz uma requisição HTTP e retorna o conteúdo da página como objeto BeautifulSoup
    def request_data(self, url: str):
        try:
            # Faz uma solicitação HTTP para a URL e obtém o conteúdo da página
            response = requests.get(url)
            response.raise_for_status()  # Lança uma exceção se a solicitação falhar
            soup = BeautifulSoup(response.text, 'html.parser')  # Analisa o HTML da página
            return soup  # Retorna o objeto BeautifulSoup
        except requests.exceptions.RequestException as e:
            print(f"Erro ao fazer a requisição para {url}: {e}")
            return None

    # Extrai a primeira notícia do site ecbahia.com
    def extract_first_titulo_link_ecBahia(self):
        raw = self.request_data(link_ecBahia)
        if raw:
            noticia = raw.find('a', class_='noticia_titulo')
            return self.extract_titulo_link_from_noticia(noticia, "ecBahia")
        return None

    # Extrai a primeira notícia do site ge.globo.com
    def extract_first_titulo_link_geBahia(self):
        raw = self.request_data(link_geBahia)
        if raw:
            noticia = raw.find('a', class_='feed-post-link gui-color-primary gui-color-hover')
            return self.extract_titulo_link_from_noticia(noticia, "geBahia")
        return None

    # Extrai a primeira notícia do site Bahia Notícias
    def extract_first_titulo_link_bahiaNoticias(self):
        raw = self.request_data(link_bahiaNoticias)
        if raw:
            div = raw.find('div', class_='sc-8a384deb-0')
            return self.extract_titulo_link_from_div(div, "bahiaNoticias")
        return None

    # Extrai o título e o link do site ecBahia ou ge
    def extract_titulo_link_from_noticia(self, noticia, site):
        if noticia:
            titulo_noticia = noticia.text
            link_noticia = noticia['href']
            link_completo = self.get_link_completo(site, link_noticia)
            return {
                "titulo": titulo_noticia,
                "link": link_completo
            }
        return None

    # Extrai o título e o link do site Bahia Notícias
    def extract_titulo_link_from_div(self, div, site):
        if div:
            a_tag = div.find('a')
            if a_tag:
                titulo_noticia = a_tag.find('h3', class_='sc-8a384deb-1 kVUytV').text
                href = a_tag['href']
                link_noticia = self.get_link_completo(site, href)
                return {
                    "titulo": titulo_noticia,
                    "link": link_noticia
                }
        return None

    # Formata o link no site para o site Bahia Notícias, pois o html só fornece parte do link
    # Como por exemplo: /entrevista/ratao-celebra-inicio-pelo-bahia-e-diz-ainda-nao-estar-em-seu-momento-ideal
    def get_link_completo(self, site, link_noticia):
        if site == "ecBahia" or site == "geBahia":
            return link_noticia
        elif site == "bahiaNoticias":
            return 'https://www.bahianoticias.com.br' + link_noticia
        return None

    # Retorna um dicionário com as notícias no formato como está no arquivo JSON, descrito no README
    def extract_titulo_link(self):
        data_atual = datetime.now().strftime("%d/%m/%Y")
        noticias = {data_atual: {}}

        noticia_ecBahia = self.extract_first_titulo_link_ecBahia()
        if noticia_ecBahia:
            noticias[data_atual]["ecBahia"] = [noticia_ecBahia]

        noticia_geBahia = self.extract_first_titulo_link_geBahia()
        if noticia_geBahia:
            noticias[data_atual]["geBahia"] = [noticia_geBahia]

        noticia_bahiaNoticias = self.extract_first_titulo_link_bahiaNoticias()
        if noticia_bahiaNoticias:
            noticias[data_atual]["bahiaNoticias"] = [noticia_bahiaNoticias]

        return noticias  # Retorna apenas as notícias da requisição

    # Escreve as noticias extraídas no arquivo JSON
    def write_noticias_to_json(self, noticias):
        # Define o caminho completo para o arquivo JSON
        caminho_arquivo = os.path.join(caminho_pasta_json, nome_json_noticias)

        try:
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                    try:
                        json_existente = json.load(arquivo)
                    except json.JSONDecodeError:
                        json_existente = {}
            else:
                json_existente = {}

            # Adicione as notícias ao JSON existente
            json_existente.update(noticias)

            with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                arquivo.write(json.dumps(json_existente, ensure_ascii=False, indent=4))
            print(f'Notícias adicionadas ao arquivo "{caminho_arquivo}".')

        except json.JSONDecodeError as e:
            print(f"Erro ao converter o dicionário para JSON: {e}")
        except Exception as e:
            print(f"Erro ao escrever notícias no arquivo JSON: {e}")

if __name__ == "__main__":
    # Cria uma instância da classe Crawler
    crawler = Crawler()
    db = Database()

    # Chama a função para extrair as notícias de todos os sites
    json_data = crawler.extract_titulo_link()

    if json_data:
        # Conecta no banco de dados e insere as notícias
        db.insert_noticias_to_db(json_data)
    
    # Escrever no arquivo JSON
    crawler.write_noticias_to_json(json_data)

    print("--------------------------------------------------------------------------------------------------------------------------------------------")
    
    # Mostra notícia de um dia específico
    noticias_do_dia = db.find_noticias_by_data(datetime.now().strftime("%d/%m/%Y"))

    print("--------------------------------------------------------------------------------------------------------------------------------------------")

    # Mostra notícia de uma faixa de dias
    noticias_por_faixa = db.find_noticias_in_date_range("12/10/2023", "31/12/2023")