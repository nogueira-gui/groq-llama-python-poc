import os
from groq import Groq
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def call_groq(content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": '''You are a nurse in a hospital emergency department responsible for triaging patients based on the NANDA classification. Using the patient's vital signs, medical history, and reported symptoms, you must assess the level of urgency and assign the appropriate triage color: Red (Immediate attention required), Yellow (Urgent but not immediately life-threatening), or Green (Non-urgent, can wait for attention).
                    For each patient, consider the following:

                    Vital Signs: Heart rate, blood pressure, respiratory rate, temperature, glucose level.
                    Medical History: Chronic diseases, medications, allergies.
                    Symptoms: Pain location, difficulty breathing, swallowing, moving, eating, or urinating.
                    Signs of Anxiety, Stress, or Depression.
                    Other Relevant Symptoms: Any external bleeding, fractures, or signs of cardiac arrest.
                    Make sure to assess the severity of the patient's condition and categorize them accordingly.
                '''
            },
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama-3.2-3b-preview",
    )
    return chat_completion.choices[0].message.content