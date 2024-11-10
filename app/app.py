from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from groq_service import call_groq

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('emergency_screen.html')

@app.route('/vitals', methods=['GET', 'POST'])
def vitals():
    return render_template('vitals_form.html')

@app.route('/emergency', methods=['GET', 'POST'])
def emergency():
    if request.method == 'POST':
        is_emergency = request.form.get('emergency')
        if is_emergency == 'yes':
            return redirect(url_for('vitals'))
        else:
            return redirect(url_for('anamnesis'))

@app.route('/anamnesis', methods=['GET','POST'])
def anamnesis():
    return render_template('anamnesis_form.html')

def run_llm_model(patient_context_prompt):
    # Avalia detalhes do paciente
    result = call_groq(patient_context_prompt)
    # Gera a prioridade usando uma chamada específica para classificação
    priority = call_groq(f"Answer only with the color name to classify as Red, Yellow, or Green for the result: {result}")
    return {
        'result': result,
        'priority': priority
    }

def generate_prompt_from_vitals_form(request):
    heart_rate = request.form.get('heart_rate', 'Not provided')
    blood_pressure = request.form.get('blood_pressure', 'Not provided')
    temperature = request.form.get('temperature', 'Not provided')
    respiratory_rate = request.form.get('respiratory_rate', 'Not provided')
    glucose_level = request.form.get('glucose_level', 'Not provided')
    iv_access = request.form.get('iv_access', 'Not provided')
    cardiac_arrest = request.form.get('cardiac_arrest', 'Not provided')
    fractures = request.form.get('fractures', 'Not provided')
    external_bleeding = request.form.get('external_bleeding', 'Not provided')
    return (
        f"Patient with vital signs: "
        f"Heart rate: {heart_rate}, Blood pressure: {blood_pressure}, "
        f"Temperature: {temperature}, Respiratory rate: {respiratory_rate}, "
        f"Glucose level: {glucose_level}, IV access: {iv_access}, "
        f"Cardiac arrest: {cardiac_arrest}, Fractures: {fractures}, "
        f"External bleeding: {external_bleeding}."
    )

def generate_prompt_from_anamnesis_form(request):
    if request.method == 'POST':
        # Personal Data
        name = request.form['nome']
        age = request.form['idade']

        # Vital Signs
        vital_data = {
            'blood_pressure': request.form['blood_pressure'],
            'heart_rate': request.form['heart_rate'],
            'respiratory_rate': request.form['respiratory_rate'],
            'glucose_level': request.form['glucose_level'],
            'fever': request.form.get('febre', 'no')
        }

        # Medical History
        medical_history = {
            'chronic_diseases': request.form['doencas_cronicas'],
            'medications': request.form['medicamentos'],
            'allergies': request.form['alergias'],
            'pain_location': request.form['local_dor']
        }

        # Difficulty in
        difficulties = {
            'breathing': request.form.get('respirar', 'no'),
            'swallowing': request.form.get('engolir', 'no'),
            'moving': request.form.get('movimentar', 'no'),
            'eating': request.form.get('alimentar', 'no'),
            'hydrating': request.form.get('hidratar', 'no'),
            'urination': request.form.get('miccao', 'no'),
            'bowel_movement': request.form.get('evacuacao', 'no')
        }

        # Signs of
        signs = {
            'anxiety': request.form.get('ansiedade', 'no'),
            'stress': request.form.get('estresse', 'no'),
            'depression': request.form.get('depressao', 'no')
        }

        return f'''
        Patient: {name}, {age} years old.
        Vital signs: {vital_data}.
        Medical history: {medical_history}.
        Difficulties: {difficulties}.
        Signs: {signs}.
        '''

@app.route('/result', methods=['GET', 'POST'])
def result_screen():
    if request.method == 'POST':
        if request.form.get('form_id') == 'vitals_form':
            patient_context_prompt = generate_prompt_from_vitals_form(request)
        elif request.form.get('form_id') == 'anamnesis_form':
            patient_context_prompt = generate_prompt_from_anamnesis_form(request)
        data = run_llm_model(patient_context_prompt)
    return render_template('result_screen.html', result=data['result'], priority=data['priority'])

if __name__ == '__main__':
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=5000)
