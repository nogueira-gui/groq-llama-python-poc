from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('emergency_screen.html')

@app.route('/vitals', methods=['GET', 'POST'])
def vitals():
    if request.method == 'POST':
        heart_rate = request.form.get('heart_rate')
        blood_pressure = request.form.get('blood_pressure')
        temperature = request.form.get('temperature')
        respiratory_rate = request.form.get('respiratory_rate')
        glucose_level = request.form.get('glucose_level')
        iv_access = request.form.get('iv_access')
        cardiac_arrest = request.form.get('cardiac_arrest')
        fractures = request.form.get('fractures')
        external_bleeding = request.form.get('external_bleeding')

        # Aqui você pode processar ou salvar os dados (salvar no banco, etc.)
        # Exemplo de redirecionamento para página de sucesso
       
    return render_template('vitals_form.html')


@app.route('/emergency', methods=['GET', 'POST'])

def emergency():
    if request.method == 'POST':
        is_emergency = request.form.get('emergency') 
        print(is_emergency)
        if is_emergency == 'yes':
            return redirect(url_for('vitals'))
        else:
            return redirect(url_for('anamnesis'))

@app.route('/anamnesis', methods=['GET', 'POST'])
def anamnesis():
    if request.method == 'POST':
        # Captura os dados da anamnese
        patient_history = request.form.get('patient_history')
        current_symptoms = request.form.get('current_symptoms')
        medications = request.form.get('medications')
        allergies = request.form.get('allergies')
        other_conditions = request.form.get('other_conditions')

        # Process or store the anamnesis data here
        return redirect(url_for('home'))  # Redireciona para a tela inicial ou outra página

    return render_template('anamnesis_form.html')

if __name__ == '__main__':
    app.run(debug=True)
