FROM python
WORKDIR /app
COPY . /app
RUN pip install streamlit sqlalchemy mysql-connector-python pandas MySQL pymysql
COPY . . 
EXPOSE 8501
EXPOSE 3306
CMD ["streamlit", "run", "Accueil.py", "--server.port=8501", "--server.address=0.0.0.0"]