
FROM ubuntu:latest

WORKDIR /app
COPY . /app
RUN apt-get update -y && apt-get install -y pip
RUN pip install streamlit
RUN streamlit run Accueil.py