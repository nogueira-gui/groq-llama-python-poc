import logging
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from groq import Groq
from elevenlabs import ElevenLabs, VoiceSettings

import uuid
import os
from werkzeug.utils import secure_filename
from secrets import retrieve_secrets_from_ssm
from stages import stages

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

secrets = retrieve_secrets_from_ssm()

GROQ_API_KEY = secrets['GROQ_API_KEY']
API_KEY = secrets['API_KEY']
ELEVEN_LABS_KEY = secrets['ELEVEN_LABS_KEY']

eleven_labs_client = ElevenLabs(
    api_key= ELEVEN_LABS_KEY
)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('Authorization')
        if api_key and api_key == API_KEY:
            logging.info("API key válida recebida")
            return func(*args, **kwargs)
        else:
            logging.warning("Tentativa de acesso não autorizada")
            return jsonify({"error": "Unauthorized"}), 401
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/conversation/session', methods=['GET'])
@require_api_key
def conversation_session():
    session_id = str(uuid.uuid4())
    logging.info(f"Nova sessão criada: {session_id}")
    response = {
        "sessionId": session_id,
    }
    return jsonify(response)

@app.route('/conversation/message', methods=['POST'])
@require_api_key
def conversation_message():
    session_id = request.form.get('sessionId')
    stage_id = request.form.get('stageId', 'NOME')  # Começa pela apresentação se for o início
    audio_file = request.files.get('audioFile')

    if not audio_file:
        logging.error("Arquivo de áudio ausente na solicitação")
        return jsonify({"error": "Audio file is required"}), 400

    # Código para salvar e transcrever o áudio
    audio_directory = 'audio'
    if not os.path.exists(audio_directory):
        os.makedirs(audio_directory)
        logging.info(f"Diretório de áudio '{audio_directory}' criado")

    audio_filename = f"{uuid.uuid4()}.mp3"
    audio_path = os.path.join(audio_directory, secure_filename(audio_filename))

    try:
        audio_file.save(audio_path)
        logging.info(f"Áudio salvo com sucesso em {audio_path}")
    except Exception as e:
        logging.error(f"Falha ao salvar o arquivo de áudio: {e}")
        return jsonify({"error": f"Failed to save audio file: {e}"}), 500

    # Transcreve o áudio usando a API do Groq
    groq_client = Groq(api_key=GROQ_API_KEY)
    try:
        with open(audio_path, "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=(audio_path, file.read()),
                model="whisper-large-v3-turbo",
                response_format="json",
                language="pt"
            )
        transcripted_audio = transcription.text
        logging.info("Transcrição de áudio concluída")
    except Exception as e:
        logging.error(f"Erro na transcrição do áudio: {e}")
        return jsonify({"error": f"Transcription failed: {e}"}), 500

    # Gera a resposta com base na etapa atual
    context = get_stage_context(stage_id)
    ai_response = call_groq(groq_client, context, transcripted_audio)

    # Verifica se a resposta está correta para avançar para a próxima etapa
    is_correct = check_response_correctness(stage_id, transcripted_audio)

    next_stage = stages[stage_id]["next"] if is_correct and "next" in stages[stage_id] else stage_id
    logging.info(f"Próxima etapa: {next_stage}")

    response = {
        "sessionId": session_id,
        "transcription": ai_response,
        "nextStage": next_stage
    }
    logging.info(f"Resposta gerada para a sessão {session_id} na etapa {stage_id}")
    return jsonify(response)

def call_groq(client, context, user_input): 
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": context
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            model="llama-3.2-3b-preview",
        )
        logging.info("Resposta da IA gerada com sucesso")
        return chat_completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Erro ao chamar o modelo Groq: {e}")
        return "Erro ao gerar resposta da IA"

# Função para obter mensagem da etapa atual
def get_stage_context(stage_id):
    stage = stages.get(stage_id)
    if stage:
        logging.info(f"Contexto para a etapa {stage_id} obtido")
        return stage["context"]
    logging.warning(f"Etapa desconhecida: {stage_id}")
    return "Etapa desconhecida."

# Função para verificar a resposta com base na lógica da etapa
def check_response_correctness(stage_id, response_text):
    # Lógica de verificação de resposta para cada etapa
    logging.info(f"Verificação da resposta para a etapa {stage_id}")
    return True


@app.route("/speak", methods=["POST"])
def text_to_speech():
    audio = speech_with_eleven_labs(request.form.get('message'))
    return Response(audio, mimetype="audio/wav")

def speech_with_eleven_labs(text):
    return eleven_labs_client.text_to_speech.convert_as_stream(
        voice_id="FGY2WhTYpPnrIDTdsKH5",
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=request.form.get('message'),
        voice_settings=VoiceSettings(
            stability=0.1,
            similarity_boost=0.3,
            style=0.2,
        ),
    )


if __name__ == '__main__':
    logging.info("Iniciando o servidor Flask")
    app.run()
