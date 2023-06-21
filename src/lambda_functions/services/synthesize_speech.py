import io
import os
import sys
import uuid
import boto3
from utils.generate_id import generate_random_uuid
from botocore.exceptions import BotoCoreError, ClientError
#from contextlib import closing

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
    

'''
  # Access the audio stream from the response
  if "AudioStream" in response:
    # Note: Closing the stream is important because the service throttles on the
    # number of parallel connections. Here we are using contextlib.closing to
    # ensure the close method of the stream object will be called automatically
    # at the end of the 'with' statement's scope.
    with closing(response["AudioStream"]) as stream:
      # Create a BytesIO object to store the audio in memory
      audio_data = io.BytesIO()
      audio_data.write(stream.read())
      audio_data.seek(0)

      # Upload the synthesized audio file to S3
      s3_bucket = bucket_name
      s3_key = str(object_prefix) + "_synthesized_audio.mp3"

    try:
      s3.upload_fileobj(audio_data, s3_bucket, s3_key)
      print("Synthesized audio uploaded to S3 successfully.")
    except (BotoCoreError, ClientError) as error:
      print(f"Error uploading the synthesized audio to S3: {error}")
      sys.exit(-1)

  else:
    # The response didn't contain audio data, exit gracefully
    print("Could not stream audio")
    sys.exit(-1)
'''