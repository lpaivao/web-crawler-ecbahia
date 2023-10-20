FROM python:3.11-slim-buster

WORKDIR /crawler

COPY . /crawler

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "crawler.py"]