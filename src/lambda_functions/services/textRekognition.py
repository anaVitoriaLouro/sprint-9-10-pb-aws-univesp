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

    # Obter o ID da conta
    sts_client = boto3.client('sts')
    account_id = sts_client.get_caller_identity()["Account"]
    print(account_id)
    
    try:
        s3.head_object(Bucket=bucket, Key=imageName)

    except botocore.exceptions.ClientError as e:
        # Imagem não encontrada no bucket
        error_message = "Imagem não encontrada no bucket."
        response = create_http_response(500, {"error": error_message})
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
    confidence_threshold = 0.8  # Limiar de confiança
    for text_detection in response['TextDetections']:
        if text_detection['Type'] == 'LINE' and text_detection['Confidence'] > confidence_threshold:
            texts.append(text_detection['DetectedText'])

    text = ' '.join(texts) # Juntar as palavras em uma única frase separadas por espaço


    # Detectar o idioma do texto usando o Amazon Comprehend
    comprehend = boto3.client('comprehend')
    language_response = comprehend.detect_dominant_language(Text=text)
    detected_language = language_response['Languages'][0]['LanguageCode']

    print(detected_language)

    if detected_language != 'pt-BR':
        # Traduzir o texto para o português usando o Amazon Translate
        translate = boto3.client('translate')
        translation_response = translate.translate_text(
            Text=text,
            SourceLanguageCode=detected_language,
            TargetLanguageCode='pt-BR'
        )
        text = translation_response['TranslatedText']


    result = {
        'url_to_image': url_to_image,
        'created_image': get_image_creation_date(bucket, imageName),
        'text': text 
    }

    #Imprime o resultado nos logs do CloudWatch
    print(result)

    # Nome do arquivo de output no S3
    text_output_bucket = f"sprint9-detected-texts-{account_id}"
    base_file_name = imageName.rsplit(".", 1)[0]
    text_output_file = base_file_name + ".txt"

    url_to_image = f"https://{text_output_bucket}.s3.amazonaws.com/{text_output_file}"
    print(url_to_image)

    # Salvar o texto detectado em um arquivo de texto
    s3.put_object(Body=text, Bucket=text_output_bucket, Key=text_output_file)


    # Chamar o serviço Amazon Polly para gerar o áudio a partir do texto
    polly = boto3.client("polly")
    response = polly.synthesize_speech(
        Text=text,
        Engine='neural',
        LanguageCode='pt-BR',
        TextType='text',
        OutputFormat="mp3",
        VoiceId="Camila"
        )

    # Obter os dados do áudio gerado
    audio_data = response["AudioStream"].read()

    # Nome do arquivo de áudio gerado
    audio_file = base_file_name + ".mp3"

    # Salvar o áudio no S3
    s3.put_object(Body=audio_data, Bucket=text_output_bucket, Key=audio_file)

    return create_http_response(200, result)