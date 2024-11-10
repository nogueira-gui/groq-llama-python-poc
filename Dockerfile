# Use uma imagem Python como base
FROM python:3.11-slim

# Define a variável de ambiente para o Flask, apontando para o caminho completo
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV GROQ_API_KEY=$GROQ_API_KEY

WORKDIR /app

COPY app .

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run"]
