FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the app sources (during image build; dev mounts will override at runtime)
COPY . .

# Ensure Python can import modules from /app
ENV PYTHONPATH=/app

EXPOSE 8501
CMD ["streamlit", "run",  "./Accueil.py", "--server.address=0.0.0.0", "--server.port=8501"]