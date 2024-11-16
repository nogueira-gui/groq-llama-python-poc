import os
import boto3
from botocore.exceptions import ClientError

def retrieve_secrets_from_ssm():
    secrets = {
        'GROQ_API_KEY': '/easytriage/GROQ_API_KEY',
        'API_KEY': '/easytriage/API_KEY',
        'ELEVEN_LABS_KEY': '/easytriage/ELEVEN_LABS_KEY'
    }

    region_name = "us-east-1"

    # Cliente para o SSM
    ssm_client = boto3.client('ssm', region_name=region_name)

    # Dicionário para armazenar os valores dos segredos recuperados
    retrieved_secrets = {}

    for secret_name, parameter_name in secrets.items():
        try:
            # Recupera o valor do parâmetro de forma simples
            response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
            parameter_value = response['Parameter']['Value']
            os.environ[secret_name] = parameter_value
            retrieved_secrets[secret_name] = parameter_value
            print(f"{secret_name} recuperado com sucesso.")
        except ClientError as e:
            print(f"Erro ao acessar o parâmetro {parameter_name}: {e}")
        except Exception as e:
            print(f"Erro ao recuperar o parâmetro {parameter_name}: {e}")

    # Retorna os segredos recuperados
    return retrieved_secrets
