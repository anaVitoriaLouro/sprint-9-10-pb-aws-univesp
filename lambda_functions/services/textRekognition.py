import boto3
import botocore.exceptions
import json
from utils.utils import get_image_creation_date, create_http_response

def img2txt(event, context):

    request_body = json.loads(event['body'])
    bucket = request_body['bucket']
    imageName = request_body['imageName']
    url_to_image = f"https://{bucket}.s3.amazonaws.com/{imageName}"
    
    # Verificar se a imagem existe no bucket
    s3 = boto3.client('s3')
    try:
        s3.head_object(Bucket=bucket, Key=imageName)

    except botocore.exceptions.ClientError as e:
        # Imagem não encontrada no bucket
        error_message = "Imagem não encontrada no bucket."
        response = create_http_response(509, {"error": error_message})
        return response
    
    # Conecta-se ao AWS Rekognition e seleciona o serviço de reconhecimento de rótulos
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_text(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': imageName
            }
        }
    )

    # Extrai os textos detectados e suas confianças
    texts = []
    for text_detection in response['TextDetections']:
        if text_detection['Type'] == 'LINE':
            texts.append({
                'DetectedText': text_detection['DetectedText'],
                'Confidence': text_detection['Confidence']
            })

    result = {
        'url_to_image': url_to_image,
        'created_image': get_image_creation_date(bucket, imageName),
        'texts': texts
    }

    #Imprime o resultado nos logs do CloudWatch
    print(result)

    return create_http_response(200, result)