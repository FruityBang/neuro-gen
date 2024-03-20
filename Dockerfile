FROM python:3.10-slim

RUN pip install poetry==1.8.1 

RUN mkdir -p /app  

COPY . /app

WORKDIR /app

RUN poetry install 
