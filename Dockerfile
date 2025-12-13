FROM python
WORKDIR /app
COPY . /app
RUN echo "Hello"
RUN apt install python3 git
RUN pip install streamlit sqlalchemy mysql-connector-python pandas MySQL
RUN git clone https://github.com/zakariazaki112/HOTEL.git
EXPOSE 8501
CMD ["streamlit", "run", "Accueil.py", "--server.port=8501", "--server.address=0.0.0.0"]