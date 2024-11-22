# EasyTriage

## Índice
- [Descrição Geral](#descrição-geral)
- [Equipe](#equipe)
- [Requisitos](#requisitos)
- [Configuração e Instalação](#configuração-e-instalação)
- [Arquitetura](#arquitetura)
- [Endpoints da API](#endpoints-da-api)
- [Execução Local](#execução-local)
- [Contribuições](#contribuições)
- [Licença](#licença)

---

## Descrição Geral
O **EasyTriage** é uma aplicação progressiva (PWA) desenvolvida para auxiliar triagens em atendimentos de saúde. 

Foi criado durante o **LLama Impact Hackathon Brazil**, realizado em novembro de 2024, um evento que desafiou as equipes participantes a desenvolver soluções inovadoras para problemas sociais e ambientais em apenas 24 horas.

## Equipe
Este projeto foi desenvolvido em colaboração por:
- **Victoria Cavalcante**
- **Lara Gonçalves da Silva**
- **Guilherme Nogueira**
- **Alberto Henrique Cordeiro**

**Frontend:** Construído com Next.js, acessível publicamente:
  - **Repositório:** [EasyTriage Frontend](https://github.com/nogueira-gui/easytriage-nextjs-pwa)
  - **Aplicação ao Vivo:** [EasyTriage App](
  https://easytriage-nextjs-pwa.vercel.app/)

- **Backend:** Utiliza Flask para gerenciar interações com APIs de IA, transcrição de áudio e geração de voz.

---

## Requisitos

### Frontend
- Node.js versão 16 ou superior
- Yarn ou npm para gerenciamento de pacotes

### Backend
- Python versão 3.10 ou superior
- Bibliotecas necessárias (listadas no `requirements.txt`):
  - `Flask==3.0.3`
  - `Flask-Cors==5.0.0`
  - `groq==0.11.0`
  - `python-dotenv`
  - `elevenlabs`
  - `boto3`
- **AWS CLI** configurado para acessar o AWS SSM Parameter Store.

---

## Configuração e Instalação

### Frontend
1. Clone o repositório:
   ```bash
   git clone https://github.com/nogueira-gui/easytriage-nextjs-pwa.git
   cd easytriage-nextjs-pwa
   ```
2. Instale as dependências:
   ```bash
   npm install
   ```
3. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```

### Backend
1. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure variáveis de ambiente locais ou carregue-as do AWS SSM:
   ```bash
   export FLASK_APP=app.py
   python app.py
   ```

---

## Arquitetura

### Frontend
- Desenvolvido com Next.js para oferecer uma experiência PWA.
- Disponibiliza uma interface interativa para triagens automáticas e entradas de voz.

### Backend
- API RESTful usando Flask.
- Integrações:
  - **Groq**: Para transcrição e processamento de áudio.
  - **ElevenLabs**: Para conversão de texto em áudio.
  - **AWS SSM Parameter Store**: Para gerenciamento seguro de segredos.

---

## Endpoints da API

### 1. Checagem de Saúde
**GET /**

**Resposta:**
```json
{
  "status": "healthy"
}
```

### 2. Criar Sessão
**GET /conversation/session**

**Cabeçalho:**
- Authorization: Chave da API

**Resposta:**
```json
{
  "sessionId": "123e4567-e89b-12d3-a456-426614174000"
}
```

### 3. Processar Mensagem
**POST /conversation/message**

**Cabeçalho:**
- Authorization: Chave da API

**Parâmetros (form-data):**
- `sessionId`: ID da sessão ativa.
- `stageId`: Etapa do atendimento.
- `audioFile`: Arquivo de áudio em formato MP3.
- Outros parâmetros opcionais para os modelos de IA.

**Resposta:**
```json
{
  "sessionId": "123e4567-e89b-12d3-a456-426614174000",
  "transcription": "Texto transcrito",
  "nextStage": "NEXT_STAGE_ID"
}
```

### 4. Gerar Áudio
**POST /speak**

**Cabeçalho:**
- Authorization: Chave da API

**Parâmetros:**
- `message`: Texto a ser convertido em áudio.
- Configurações de voz (opcionais).

**Resposta:** Arquivo de áudio no formato especificado.

---

## Execução Local

1. Configure as variáveis de ambiente necessárias:
   - `GROQ_API_KEY`
   - `API_KEY`
   - `ELEVEN_LABS_KEY`

2. Execute o backend:
   ```bash
   flask run
   ```

3. Execute o frontend:
   ```bash
   npm run dev
   ```

4. Acesse as aplicações localmente:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend: [http://localhost:5000](http://localhost:5000)

---

## Contribuições
Contribuições são bem-vindas!😊 Para colaborar:

1. Faça um fork do repositório.
2. Crie um branch para sua feature ou bugfix.
3. Envie um pull request com suas alterações.

---

## Licença
O EasyTriage é licenciado sob a Licença MIT.