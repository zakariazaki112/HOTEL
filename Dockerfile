FROM ubuntu:22.04

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ['streamlit', 'run', 'Accueil.py']