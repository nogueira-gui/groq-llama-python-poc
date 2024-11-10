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

@app.route('/anamnesis', methods=['GET','POST'])
def anamnesis():
    if request.method == 'POST':
        # Dados Pessoais
        nome = request.form['nome']
        idade = request.form['idade']
        cep = request.form['cep']

        # Sinais Vitais
        blood_pressure = request.form['blood_pressure']
        heart_rate = request.form['heart_rate']
        respiratory_rate = request.form['respiratory_rate']
        glucose_level = request.form['glucose_level']
        febre = request.form.get('febre', 'no')  # Default is 'no' if not checked

        # História Médica
        doencas_cronicas = request.form['doencas_cronicas']
        medicamentos = request.form['medicamentos']
        alergias = request.form['alergias']
        local_dor = request.form['local_dor']

        # Dificuldade em
        respirar = request.form.get('respirar', 'no')
        engolir = request.form.get('engolir', 'no')
        movimentar = request.form.get('movimentar', 'no')
        alimentar = request.form.get('alimentar', 'no')
        hidratar = request.form.get('hidratar', 'no')
        miccao = request.form.get('miccao', 'no')
        evacuacao = request.form.get('evacuacao', 'no')

        # Sinais de
        ansiedade = request.form.get('ansiedade', 'no')
        estresse = request.form.get('estresse', 'no')
        depressao = request.form.get('depressao', 'no')

        # Aqui você pode fazer o que quiser com os dados, como salvar no banco de dados ou processar.

        return render_template('anamnesis_form.html', nome=nome, idade=idade, cep=cep,
                               blood_pressure=blood_pressure, heart_rate=heart_rate,
                               respiratory_rate=respiratory_rate, glucose_level=glucose_level,
                               febre=febre, doencas_cronicas=doencas_cronicas, medicamentos=medicamentos,
                               alergias=alergias, local_dor=local_dor, respirar=respirar,
                               engolir=engolir, movimentar=movimentar, alimentar=alimentar,
                               hidratar=hidratar, miccao=miccao, evacuacao=evacuacao,
                               ansiedade=ansiedade, estresse=estresse, depressao=depressao)
    return render_template('anamnesis_form.html')
if __name__ == '__main__':
    app.run(debug=True)
