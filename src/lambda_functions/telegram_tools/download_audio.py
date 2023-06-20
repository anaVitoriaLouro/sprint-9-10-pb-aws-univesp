import requests
import json
import os
from io import BytesIO
from utils.upload_to_s3 import upload_file_to_s3

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
AUDIO_INPUT_BUCKET_NAME = os.environ['AUDIO_INPUT_BUCKET_NAME']

def download_audio(file_id, file_unique_id):
    try:
        # This gets the "file_path" of the specified file
        response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile?file_id={file_id}")
        # Check if there was a request error
        response.raise_for_status()
        audiofile_path = response.json()['result']['file_path']

        # Now this downloads the file passed by the user
        audio_file = requests.get(f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{audiofile_path}").content
        
        # Use the given file_unique_id to store the file in a S3Bucket
        audio_file_key = (f'{file_unique_id}.mp3')
        
        upload_file_to_s3(audio_file, AUDIO_INPUT_BUCKET_NAME, audio_file_key)

        print(audio_file_key)
        return audio_file_key
    
    except Exception as e:
        print(f'Impossible to donwload audio file from Telegram: {e}')