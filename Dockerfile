# Use uma imagem Python como base
FROM python:3.11-slim

# Define a variável de ambiente para o Flask, apontando para o caminho completo
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV GROQ_API_KEY=$GROQ_API_KEY
ENV API_KEY=$API_KEY
ENV ELEVEN_LABS_KEY=$ELEVEN_LABS_KEY
WORKDIR /app

COPY app .

RUN pip install -r /app/requirements.txt

RUN pip install gunicorn

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
