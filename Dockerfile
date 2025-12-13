FROM python:3.9-slim

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD 'streamlit run /home/aira/Projects/TP/Base/Final_Project/app/Accueil.py'