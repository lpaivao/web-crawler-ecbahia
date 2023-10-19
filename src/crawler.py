import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database import Database

# Links para os sites de notícias
link_ecBahia = 'https://www.ecbahia.com/noticias-do-bahia'
link_geBahia = 'https://ge.globo.com/ba/futebol/times/bahia/'
link_bahiaNoticias = 'https://www.bahianoticias.com.br/esportes/bahia'

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


    def extract_first_noticia_ecBahia(self):
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
            'data': datetime.now().strftime("%d/%m/%Y"),
            'titulo': titulo,
            'link': link,
            'chamada': chamada,
            'imagem': f"{url_to_img}/{imagem}"
        }

        return noticia_data

    def extract_first_noticia_geBahia(self):

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
            'data': datetime.now().strftime("%d/%m/%Y"),
            'titulo': titulo,
            'link': link,
            'chamada': chamada,
            'imagem': imagem
        }

        return noticia_data
        

    def extract_first_noticia_bahia_noticias(self):

        url_to_img = "https://www.bahianoticias.com.br"

        soup = self.request_data(link_bahiaNoticias)

        noticia = soup.find('div', class_='sc-c22b9e79-0 eVIuxM')

        if not noticia:
            print("Nenhuma notícia encontrada no site geBahia.")
            return None

        titulo = noticia.find('h3', class_='sc-8a384deb-1 kVUytV').text.strip()
        link = "https://www.bahianoticias.com.br" + noticia.find('a')['href']
        chamada = noticia.find('div', class_='sc-c22b9e79-3 gGKeEu').find('p').text.strip()

        # Existem duas tags "src" para a imagem, precisamos pegar a segunda
        imagem = noticia.find('div', class_='imgWrapper').find_all('img')
        imagem = imagem[1].get('src')

        noticia_data = {
            'data': datetime.now().strftime("%d/%m/%Y"),
            'titulo': titulo,
            'link': link,
            'chamada': chamada,
            'imagem': f"{url_to_img}{imagem}"
        }

        return noticia_data

if __name__ == "__main__":
    # Cria uma instância da classe Crawler
    crawler = Crawler()
    db = Database()

    db.insert_noticias_to_db(crawler.extract_first_noticia_ecBahia())
    db.insert_noticias_to_db(crawler.extract_first_noticia_geBahia())
    db.insert_noticias_to_db(crawler.extract_first_noticia_bahia_noticias())
        

    print("-------------------------------------------------------------------------------------------------------------------------")
    
    # Mostra notícia de um dia específico
    noticias_do_dia = db.find_noticias_by_data(datetime.now().strftime("%d/%m/%Y"))

    print("-------------------------------------------------------------------------------------------------------------------------")

    # Mostra notícia de uma faixa de dias
    noticias_por_faixa = db.find_noticias_in_date_range("12/10/2023", "31/12/2023")