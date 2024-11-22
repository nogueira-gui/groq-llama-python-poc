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

@app.route("/", methods=["GET"])
def health_check():
    try:
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        logging.error(f"Erro na checagem de saúde: {e}")
        return jsonify({"error": "Unhealthy"}), 500
    
@app.route("/.well-known/pki-validation/C52A7DADCA4E70D7A748F6DDA6BC89C4.txt")
def verify():
    return '''97AF1512DBFEA565E270622FF55592C94A4D21B759CAC94D0583FAB92B073013
comodoca.com
eb6a05ae2173450'''

def require_api_key(func):
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if auth and auth == API_KEY:
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
    stage_id = request.form.get('stageId', 'NOME')
    audio_file = request.files.get('audioFile')
    text_model_id = request.form.get('textModelId', 'llama-3.2-3b-preview')
    transcript_model_id = request.form.get('transcriptModelId', 'whisper-large-v3-turbo')
    language_transcript = request.form.get('languageTranscript', 'pt')

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
                model= transcript_model_id,
                response_format="json",
                language=language_transcript
            )
        transcripted_audio = transcription.text
        logging.info("Transcrição de áudio concluída")
    except Exception as e:
        logging.error(f"Erro na transcrição do áudio: {e}")
        return jsonify({"error": f"Transcription failed: {e}"}), 500

    # Gera a resposta com base na etapa atual
    context = get_stage_context(stage_id)
    ai_response = call_groq(groq_client, context, transcripted_audio, text_model_id)

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

def call_groq(client, context, user_input, text_model_id): 
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
            model=text_model_id
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


def speech_with_eleven_labs(message, tts_config):
    return eleven_labs_client.text_to_speech.convert_as_stream(
        voice_id=tts_config['voice_id'],
        optimize_streaming_latency=tts_config['optimize_streaming_latency'],
        output_format=tts_config['output_format'],
        text=message,
        voice_settings=VoiceSettings(
            stability=tts_config['voice_settings']['stability'],
            similarity_boost=tts_config['voice_settings']['similarity'],
            style=tts_config['voice_settings']['style'],
            use_speaker_boost=tts_config['voice_settings']['use_speaker_boost']
        )
    )

@app.route("/speak", methods=["POST"])
@require_api_key
def text_to_speech():
    tts_config = {
        'voice_id': request.form.get('voiceId', 'cyD08lEy76q03ER1jZ7y'),
        'optimize_streaming_latency': request.form.get('optimizeStreamingLatency', "0"),
        'output_format': request.form.get('outputFormat', "mp3_22050_32"),
        'voice_settings': {
            'stability': float(request.form.get('voiceStability', 0.1)),
            'similarity': float(request.form.get('voiceSimilarity', 0.3)),
            'style': float(request.form.get('voiceStyle', 0.2)),
            'use_speaker_boost': bool(request.form.get('useSpeakerBoost', False))
        }
    }
    audio = speech_with_eleven_labs(request.form.get('message'), tts_config)
    return Response(audio, mimetype="audio/wav")


if __name__ == '__main__':
    logging.info("Iniciando o servidor Flask")
    app.run()
