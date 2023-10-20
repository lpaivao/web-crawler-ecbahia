import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database import Database
from bot import Bot
import schedule

# Links para os sites de notícias
link_ecBahia = 'https://www.ecbahia.com/noticias-do-bahia'
link_geBahia = 'https://ge.globo.com/ba/futebol/times/bahia/'
link_bahiaNoticias = 'https://www.bahianoticias.com.br/esportes/bahia'

class Crawler:

    def __init__(self) -> None:
        self.db = Database()
        self.bot = Bot()

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


    def extract_first_noticia_ecBahia(self):

        try:
            url_to_img = "https://www.ecbahia.com"

            soup = self.request_data(link_ecBahia)

            noticia = soup.find('div', class_='item')

            if not noticia:
                print("Nenhuma notícia encontrada no site ecbahia.")
                return None

            titulo = noticia.find('h2').find('a').text.strip()
            link = noticia.find('h2').find('a')['href']
            chamada = noticia.find('p').find('a').text.strip()
            imagem = noticia.find('img')['src']

            noticia_data = {
                'data': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'titulo': titulo,
                'link': link,
                'chamada': chamada,
                'imagem': f"{url_to_img}/{imagem}"
            }

            # Tenta inserir no BD
            response = self.db.insert_noticias_to_db(noticia_data)

            # Se conseguir inserir, é porque a notícia é nova, logo, é para se postar no Twitter
            if response is True:
                self.bot.post(noticia_data)
        
        except Exception as e:
            print(f"Erro na função de extrair: {e}")

    def extract_first_noticia_geBahia(self):

        try:

            soup = self.request_data(link_geBahia)

            noticia = soup.find('div', class_='feed-post-body')

            if not noticia:
                print("Nenhuma notícia encontrada no site geBahia.")
                return None

            titulo = noticia.find('a').find('h2').text.strip()
            link = noticia.find('a')['href']
            chamada = noticia.find('div', class_='feed-post-body-resumo').find('p').text.strip()
            imagem = noticia.find('div', class_='feed-media-wrapper').find('img')['src']

            noticia_data = {
                'data': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'titulo': titulo,
                'link': link,
                'chamada': chamada,
                'imagem': imagem
            }

            # Tenta inserir no BD
            response = self.db.insert_noticias_to_db(noticia_data)

            # Se conseguir inserir, é porque a notícia é nova, logo, é para se postar no Twitter
            if response is True:
                self.bot.post(noticia_data)
        
        except Exception as e:
            print(f"Erro na função de extrair: {e}")
        

    def extract_first_noticia_bahia_noticias(self):

        try:

            url_to_img = "https://www.bahianoticias.com.br"

            soup = self.request_data(link_bahiaNoticias)

            noticia = soup.find('div', class_='sc-c22b9e79-0 eVIuxM')

            if not noticia:
                print("Nenhuma notícia encontrada no site geBahia.")
                return None

            titulo = noticia.find('h3', class_='sc-8a384deb-1 kVUytV').text.strip()
            link = "https://www.bahianoticias.com.br" + noticia.find('a')['href']
            chamada = noticia.find('div', class_='sc-c22b9e79-3 gGKeEu').find('p').text.strip()

            # Limita a chamada a 150 caracteres e adiciona "..." ao final, se necessário
            chamada = chamada[:100] + ('...(continua)' if len(chamada) > 100 else '')

            # Existem duas tags "src" para a imagem, precisamos pegar a segunda
            imagem = noticia.find('div', class_='imgWrapper').find_all('img')
            imagem = imagem[1].get('src')

            noticia_data = {
                'data': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'titulo': titulo,
                'link': link,
                'chamada': chamada,
                'imagem': f"{url_to_img}{imagem}"
            }

            # Tenta inserir no BD
            response = self.db.insert_noticias_to_db(noticia_data)

            # Se conseguir inserir, é porque a notícia é nova, logo, é para se postar no Twitter
            if response is True:
                self.bot.post(noticia_data)
        
        except Exception as e:
            print(f"Erro na função de extrair: {e}")
    
    def execute(self):
        self.extract_first_noticia_ecBahia()
        self.extract_first_noticia_geBahia()
        self.extract_first_noticia_bahia_noticias()

if __name__ == "__main__":

    crawler = Crawler()
        
    def job():
        crawler.execute()

    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()