import os
import boto3
from botocore.exceptions import ClientError


# def get_secrets_from_env(keys):
#     return {key: os.environ[key] for key in keys if key in os.environ}

def retrieve_secrets_from_ssm():
    # keys = ['GROQ_API_KEY', 'API_KEY', 'ELEVEN_LABS_KEY']
    # secrets = get_secrets_from_env(keys)

    # if all(key in secrets for key in keys):
    #     return secrets
        
    secrets = {
        'GROQ_API_KEY': '/easytriage/GROQ_API_KEY',
        'API_KEY': '/easytriage/API_KEY',
        'ELEVEN_LABS_KEY': '/easytriage/ELEVEN_LABS_KEY'
    }

    region_name = "us-east-1"

    ssm_client = boto3.client('ssm', region_name=region_name)

    retrieved_secrets = {}

    for secret_name, parameter_name in secrets.items():
        try:
            response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
            parameter_value = response['Parameter']['Value']
            os.environ[secret_name] = parameter_value
            retrieved_secrets[secret_name] = parameter_value
            print(f"{secret_name} recuperado com sucesso.")
        except ClientError as e:
            print(f"Erro ao acessar o parâmetro {parameter_name}: {e}")
        except Exception as e:
            print(f"Erro ao recuperar o parâmetro {parameter_name}: {e}")

    return retrieved_secrets
