# Crawler para notícias do time Esporte Clube Bahia

Ao executar o programa, serão extraídas as notícias mais recentes do dia de três sites de notícias do time, sendo essas notícias escritas no banco de dados.

## Como funciona

As notícias são extraídas dos seguintes sites:

- https://www.ecbahia.com/noticias-do-bahia
- https://ge.globo.com/ba/futebol/times/bahia/
- https://www.bahianoticias.com.br/esportes/bahia

No banco de dados MongoDB, cada data notícia estará estruturada assim:

```console
{
    "data":"19/10/2023",
    "titulo":"Bahia vence o Inter na Fonte Nova e conquista 2º triunfo seguido na Série A",
    "link":"https://www.ecbahia.com/brasileiro/bahia-vence-o-inter-na-fonte-nova-e-conquista-2-triunfo-seguido-na-serie-a",
    "chamada":"Biel marcou o único gol tricolor no jogo",
    "imagem":"https://www.ecbahia.com/imgs/fotos/bahxint1.jpg"
}
```
## Como executar

1. Baixar o repositório

```console
git clone https://github.com/lpaivao/bot-web-crawler.git
```
2. Instalar as dependências
```console
pip install -r requirements.txt
```
3. Entrar na pasta src
```console
cd src/
```
4. Executar arquivo
```console
python3 crawler.py 
```
