import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import io
import os
import sys
import uuid
from utils.generate_id import generate_random_uuid

TEXT_INPUT_BUCKET_NAME = os.environ['TEXT_INPUT_BUCKET_NAME']
SYNTHESIZED_SPEECH_BUCKET_NAME = os.environ['SYNTHESIZED_SPEECH_BUCKET_NAME']

polly = boto3.client("polly")
s3 = boto3.client("s3")

def synthesize_speech(text):
  
  print(f'Texto recebido: {text}')
  object_prefix = generate_random_uuid()
  print(f'Prefixo gerado: {object_prefix}')

  try:
    
    # Nome do arquivo de output no S3
		#base_file_name = image_to_process.rsplit(".", 1)[0]
    text_file_key = object_prefix + ".txt"
		
	# Salva o texto recebido no bucket
    s3.put_object(Body=text, Bucket=TEXT_INPUT_BUCKET_NAME, Key=text_file_key)
    url_to_text = (f'https://{TEXT_INPUT_BUCKET_NAME}.s3.amazonaws.com/{text_file_key}')
    print(f'URL do texto recebido: {url_to_text}')
    
    # Request speech synthesis
    response = polly.synthesize_speech(
        Engine="neural",
        LanguageCode="pt-BR",
        TextType="text",
        Text=text,
        OutputFormat="mp3",
        VoiceId="Camila",
    )
    
    # Obter os dados do áudio gerado
    audio_data = response["AudioStream"].read()
    
    # Nome do arquivo de áudio gerado
    audio_file = object_prefix + ".mp3"
    
    # Salvar o áudio sintetizado no S3
    s3.put_object(Body=audio_data, Bucket=SYNTHESIZED_SPEECH_BUCKET_NAME, Key=audio_file)
    
    # Get audio object URL from S3
    synthesized_speech_url = (f'https://{SYNTHESIZED_SPEECH_BUCKET_NAME}.s3.amazonaws.com/{audio_file}')
    
    # Print audio url for debug
    print(f'This is the synthesized audio url: {synthesized_speech_url}')
    
    return synthesized_speech_url
    
  except (BotoCoreError, ClientError) as error:
        print(f"The service returned an error, exit gracefully: {error}")
        sys.exit(-1)
