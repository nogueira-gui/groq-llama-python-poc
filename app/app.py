from flask import Flask, render_template, request, jsonify
import os
from groq import Groq
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def call_groq(content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Você é uma enfermeira que faz a triagem de pacientes no hospital"
            },
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama-3.2-3b-preview",
    )
    return chat_completion.choices[0].message.content


def classificar_prioridade(result):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Você é uma enfermeira que faz a triagem de pacientes no hospital"
            },
            {
                "role": "user",
                "content": f'Responda apenas com a cor que classifique o paciente: Vermelho, Amarelo e Verde para o seguinte resultado de triagem: {result}'
            }
        ],
        model="llama-3.2-3b-preview",
    )
    return chat_completion.choices[0].message.content


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/triagem', methods=['POST'])
def triagem():
    # Recebe os dados do formulário
    nome = request.form.get("nome")
    idade = request.form.get("idade")
    sintomas = request.form.get("sintomas")

    # Contexto para o modelo Groq
    patient_context = f"O paciente {nome}, com idade {idade}, apresenta os sintomas: {sintomas}."

    # Chama o modelo para processar a triagem
    result = call_groq(patient_context)

    # Classifica a prioridade do paciente
    prioridade = classificar_prioridade(result)

    # Retorna o resultado e a prioridade em formato JSON
    return jsonify({"result": result, "prioridade": prioridade})


if __name__ == '__main__':
    app.run(port=5000)
