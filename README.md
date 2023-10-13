# Crawler para notícias do time Esporte Clube Bahia

Ao executar o programa, serão extraídas as notícias mais recentes do dia de três sites de notícias do time, sendo essas notícias escritas
no banco de dados.

## Como funciona

As notícias são extraídas dos seguintes sites:

- https://www.ecbahia.com/noticias-do-bahia
- https://ge.globo.com/ba/futebol/times/bahia/
- https://www.bahianoticias.com.br/esportes/bahia

Após serem extraídas, as notícias são escritas no arquivo da pasta *json* do mesmo diretório que a pasta *src*, com os seguinte nome:
- noticias.json

As notícias nos arquivos JSON estão no seguinte formato:

```console
{
    "12/10/2023": {
        "ecBahia": [
            {
                "titulo": "Ratão celebra inicio pelo Bahia e diz ainda não estar em seu 'momento ideal'",
                "link": "https://www.ecbahia.com/entrevista/ratao-celebra-inicio-pelo-bahia-e-diz-ainda-nao-estar-em-seu-momento-ideal"
            }
        ],
        "geBahia": [
            {
                "titulo": "Bahia celebra Dia das Crianças com fotos da infância de Ceni e elenco",
                "link": "https://ge.globo.com/ba/futebol/times/bahia/noticia/2023/10/12/bahia-celebra-dia-das-criancas-com-fotos-que-resgatam-infancia-de-rogerio-ceni-e-dos-atletas-confira.ghtml"
            }
        ],
        "bahiaNoticias": [
            {
                "titulo": "Marcelo de Lima Henrique apita duelo entre Bahia e Inter na Fonte Nova",
                "link": "https://www.bahianoticias.com.br/esportes/bahia/29594-marcelo-de-lima-henrique-apita-duelo-entre-bahia-e-inter-na-fonte-nova"
            }
        ]
    }
}
```

Já no banco de dados MongoDB, cada data registro estará assim, com nenhuma com data repetida:

```console
{
    "data": "12/10/2023",
    "noticias": 
        "ecBahia": [
            {
                "titulo": "Ratão celebra inicio pelo Bahia e diz ainda não estar em seu 'momento ideal'",
                "link": "https://www.ecbahia.com/entrevista/ratao-celebra-inicio-pelo-bahia-e-diz-ainda-nao-estar-em-seu-momento-ideal"
            }
        ],
        "geBahia": [
            {
                "titulo": "Bahia celebra Dia das Crianças com fotos da infância de Ceni e elenco",
                "link": "https://ge.globo.com/ba/futebol/times/bahia/noticia/2023/10/12/bahia-celebra-dia-das-criancas-com-fotos-que-resgatam-infancia-de-rogerio-ceni-e-dos-atletas-confira.ghtml"
            }
        ],
        "bahiaNoticias": [
            {
                "titulo": "Marcelo de Lima Henrique apita duelo entre Bahia e Inter na Fonte Nova",
                "link": "https://www.bahianoticias.com.br/esportes/bahia/29594-marcelo-de-lima-henrique-apita-duelo-entre-bahia-e-inter-na-fonte-nova"
            }
        ]
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