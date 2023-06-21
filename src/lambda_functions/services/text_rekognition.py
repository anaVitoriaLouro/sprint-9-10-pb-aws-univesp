import boto3
import botocore.exceptions
import json
import os
from dotenv import load_dotenv

from utils.utils import get_image_creation_date, create_http_response

load_dotenv()

# Load environment variables
IMAGE_INPUT_BUCKET_NAME = os.environ['IMAGE_INPUT_BUCKET_NAME']
TEXT_OUTPUT_BUCKET_NAME = os.environ['TEXT_OUTPUT_BUCKET_NAME']
SYNTHESIZED_SPEECH_BUCKET_NAME = os.environ['SYNTHESIZED_SPEECH_BUCKET_NAME']

# s3 client connection
s3 = boto3.client('s3')

# Comprehend client connection
comprehend = boto3.client('comprehend')

# Polly client connection 
polly = boto3.client("polly")

print('Entrou no textRekognition')

def img2txt(image_to_process):
    
	# Retrieve the image from S3 to start Rekognition
	try:
		s3.get_object(Bucket=IMAGE_INPUT_BUCKET_NAME, Key=image_to_process)
		# Conecta-se ao AWS Rekognition e seleciona o serviço de reconhecimento de rótulos

		rekognition = boto3.client('rekognition')
		response = rekognition.detect_text(
			Image={
				'S3Object': {
				'Bucket': IMAGE_INPUT_BUCKET_NAME,
				'Name': image_to_process
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

		# Detectar o idioma com base no texto extraido
		language_response = comprehend.detect_dominant_language(Text=text)
		detected_language = language_response['Languages'][0]['LanguageCode']

		print(f'detected_language: {detected_language}')

		# Traduzir o texto para o português usando o Amazon Translate
		if detected_language != 'pt-BR':
			translate = boto3.client('translate')
			translation_response = translate.translate_text(
				Text=text,
				SourceLanguageCode=detected_language,
				TargetLanguageCode='pt-BR'
			)
			text = translation_response['TranslatedText']


		# result = {
		# 	'url_to_image': url_to_image,
		# 	'created_image': get_image_creation_date(bucket, imageName),
		# 	'text': text 
		# }

		# Imprime o resultado nos logs do CloudWatch
		print(f'Texto extraído da imagem: {text}')

		# Nome do arquivo de output no S3
		base_file_name = image_to_process.rsplit(".", 1)[0]
		text_file_key = base_file_name + ".txt"

		# Salvar o texto detectado em um arquivo de texto
		s3.put_object(Body=text, Bucket=TEXT_OUTPUT_BUCKET_NAME, Key=text_file_key)

		url_to_extracted_text = (f'https://{TEXT_OUTPUT_BUCKET_NAME}.s3.amazonaws.com/{text_file_key}')
		print(f'URL do texto extraído da imagem: {url_to_extracted_text}')

		# Chamar o serviço Amazon Polly para gerar o áudio a partir do texto
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

		# Salvar o áudio sintetizado no S3
		s3.put_object(Body=audio_data, Bucket=SYNTHESIZED_SPEECH_BUCKET_NAME, Key=audio_file)

		# Get audio object URL from S3
		synthesized_speech_url = (f'https://{SYNTHESIZED_SPEECH_BUCKET_NAME}.s3.amazonaws.com/{audio_file}')

		# Print audio url for debug
		print(f'This is the synthesized audio url: {synthesized_speech_url}')
		
		return synthesized_speech_url

	except botocore.exceptions.ClientError as e:
		print(f'An error ocurred, please verify: {e}')