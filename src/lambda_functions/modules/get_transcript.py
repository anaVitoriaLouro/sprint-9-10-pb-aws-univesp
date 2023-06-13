import json
import uuid
import os
from utils.download_audio import download_audiofile
from utils.upload_to_s3 import upload_file_to_s3
from services.transcribe import transcribe_audio

SLACK_TOKEN = os.environ['SLACK_TOKEN']
BUCKET_NAME = os.environ['BUCKET_NAME']

def get_transcript(body):
  try:
    if "files" in body["event"] and body["event"]["files"] and "url_private_download" in body["event"]["files"][0]:
      audio_url = body["event"]["files"][0]["url_private_download"]
      audio_file = download_audiofile(audio_url, SLACK_TOKEN)
      
      media_format = audio_url.split('.')[-1]
      print('media__format')
      print(media_format)
      
      hash_name = str(uuid.uuid4().hex)
      
      if media_format == '.mp3':
         object_key = str(hash_name) + '_current_audio.mp3'
      else:
        object_key = str(hash_name) + '_current_audio.mp4'

      upload_file_to_s3(audio_file, BUCKET_NAME, object_key)

      print('transcription STARTED')
      transcription = transcribe_audio(BUCKET_NAME, object_key, hash_name)
      print('transcription COMPLETED')
      
      transcript_dictonary = json.loads(transcription)           
      transcript = transcript_dictonary["results"]["transcripts"][0]["transcript"]
      print(f'Iterated over transcript_dictonary. The transcript content is: {transcript}')
  
      return transcript
    
  except Exception as e:
    return (f'Error occurred: {str(e)}')