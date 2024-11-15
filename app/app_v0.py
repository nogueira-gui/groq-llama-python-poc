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
    heart_rate = request.form.get('heart_rate')
    blood_pressure = request.form.get('blood_pressure')
    temperature = request.form.get('temperature')
    respiratory_rate = request.form.get('respiratory_rate')
    glucose_level = request.form.get('glucose_level')
    iv_access = request.form.get('iv_access')
    cardiac_arrest = request.form.get('cardiac_arrest')
    fractures = request.form.get('fractures')
    external_bleeding = request.form.get('external_bleeding')

    prompt = f"Patient with vital signs: \n"
    if heart_rate:
        prompt += f"Heart rate: {heart_rate}, \n"
    if blood_pressure:
        prompt += f"Blood pressure: {blood_pressure}, \n"
    if temperature:
        prompt += f"Temperature: {temperature},\n"
    if respiratory_rate:
        prompt += f"Respiratory rate: {respiratory_rate}, \n"
    if glucose_level:
        prompt += f"Glucose level: {glucose_level},\n"
    if iv_access:
        prompt += f"IV access: {iv_access}, \n"
    if cardiac_arrest:
        prompt += f"Cardiac arrest: {cardiac_arrest},\n" 
    if fractures:
        prompt += f"Fractures: {fractures}, \n"
    if external_bleeding:
        prompt += f"External bleeding: {external_bleeding}."
    
    return prompt

def generate_prompt_from_anamnesis_form(request):
    if request.method == 'POST':
        name = request.form['nome']
        age = request.form['idade']

        vital_data = {}
        if request.form['blood_pressure']:
            vital_data['blood_pressure'] = request.form['blood_pressure']
        if request.form['heart_rate']:
            vital_data['heart_rate'] = request.form['heart_rate']
        if request.form['respiratory_rate']:
            vital_data['respiratory_rate'] = request.form['respiratory_rate']
        if request.form['glucose_level']:
            vital_data['glucose_level'] = request.form['glucose_level']
        if request.form['fever']:
            vital_data['fever'] = request.form['fever']

        medical_history = {}
        if request.form['doencas_cronicas']:
            medical_history['chronic_diseases'] = request.form['doencas_cronicas']
        if request.form['medicamentos']:
            medical_history['medications'] = request.form['medicamentos']
        if request.form['alergias']:
            medical_history['allergies'] = request.form['alergias']
        if request.form['local_dor']:
            medical_history['pain_location'] = request.form['local_dor']

        difficulties = {}
        if request.form.get('respirar'):
            difficulties['breathing'] = request.form['respirar']
        if request.form.get('engolir'):
            difficulties['swallowing'] = request.form['engolir']
        if request.form.get('movimentar'):
            difficulties['moving'] = request.form['movimentar']
        if request.form.get('alimentar'):
            difficulties['eating'] = request.form['alimentar']
        if request.form.get('hidratar'):
            difficulties['hydrating'] = request.form['hidratar']
        if request.form.get('miccao'):
            difficulties['urination'] = request.form['miccao']
        if request.form.get('evacuacao'):
            difficulties['bowel_movement'] = request.form['evacuacao']

        signs = {}
        if request.form.get('ansiedade'):
            signs['anxiety'] = request.form.get('ansiedade')
        if request.form.get('estresse'):
            signs['stress'] = request.form.get('estresse')
        if request.form.get('depressao'):
            signs['depression'] = request.form.get('depressao')

        prompt = f'''
        Patient: {name}, {age} years old.
        Vital signs: {vital_data}.
        Medical history: {medical_history}.
        Difficulties: {difficulties}.
        Signs: {signs}.
        '''
        return prompt

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
