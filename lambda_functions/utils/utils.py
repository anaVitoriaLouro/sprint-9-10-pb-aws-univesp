import boto3
import json

def create_http_response(status_code, body):
    """
    Cria uma resposta HTTP válida.

    Parâmetros:
    - status_code (int): O código de status da resposta.
    - body (dict): O corpo da resposta.

    Retorna:
    Um dicionário contendo a resposta HTTP com o status code, corpo e cabeçalhos.

    """
    response = {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
    return response
   
def get_image_creation_date(bucket, imageName):
    """
    Obtém a data de criação de uma imagem no bucket do Amazon S3.

    Args:
        bucket (str): Nome do bucket do Amazon S3.
        imageName (str): Nome da imagem.

    Returns:
        str: Data de criação da imagem no formato '%d-%m-%Y %H:%M:%S'.
    """
    s3 = boto3.client('s3')
    
    response = s3.head_object(Bucket=bucket, Key=imageName)
    creation_date = response['LastModified'].strftime('%d-%m-%Y %H:%M:%S')
    
    return creation_date