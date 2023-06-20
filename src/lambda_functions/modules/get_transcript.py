import json
import uuid
import os
from telegram_tools.download_audio import download_audiofile
from utils.upload_to_s3 import upload_file_to_s3
from services.transcribe import transcribe_audio
from utils.generate_id import generate_random_uuid

SLACK_TOKEN = os.environ['SLACK_TOKEN']
AUDIO_INPUT_BUCKET_NAME = os.environ['AUDIO_INPUT_BUCKET_NAME']
TEXT_OUTPUT_BUCKET_NAME = os.environ['TEXT_OUTPUT_BUCKET_NAME']

def get_transcript(body, audio_file_key, AUDIO_INPUT_BUCKET_NAME):
  hash_prefix = generate_random_uuid()
  
  # aqui precisa fazer uma verificação pra ver se na resposta json do telegram tem o audio, se tiver continua o código
  try:
    if "files" in body["event"] and body["event"]["files"] and "url_private_download" in body["event"]["files"][0]:
      audio_url = body["event"]["files"][0]["url_private_download"]
      audio_file = download_audiofile(audio_url, SLACK_TOKEN)
      
      # object_key = audio_url.split('/')[-1]
      # print(f'obj_key from get_transcript {object_key}')

      # object_key = hash_prefix + '_' + object_key
      
      print(f'audio_file_key from get_transcript.py: {audio_file_key}')
      
      print('transcription STARTED')
      transcription = transcribe_audio(AUDIO_INPUT_BUCKET_NAME, audio_file_key)
      print('transcription COMPLETED')
      
      transcript_dictonary = json.loads(transcription)           
      transcript = transcript_dictonary["results"]["transcripts"][0]["transcript"]
      print(f'Iterated over transcript_dictonary. The transcript content is: {transcript}')
  
      return transcript
    
  except Exception as e:
    print(f'Something malfunctioned in get_transcript.py: {str(e)}')