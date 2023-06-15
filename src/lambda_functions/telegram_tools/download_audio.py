import boto3
import requests
import json
import os
from io import BytesIO
from pydub import AudioSegment

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
AUDIO_INPUT_BUCKET_NAME = os.environ['AUDIO_INPUT_BUCKET_NAME']

def download_audio(file_id, file_unique_id):
    # This gets the "file_path" of the specified file
    response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile?file_id={file_id}")
    audiofile_path = response.json()['result']['file_path']

    # Now this downloads the file passed by the user
    audio_file = requests.get(f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{audiofile_path}").content

    # Convert the default '.oga' format to '.mp3'
    audio = AudioSegment.from_file(audio_file, format="oga")
    mp3_data = audio.export(format="mp3")
    mp3_audio = AudioSegment.from_file(mp3_data, format="mp3")

    # Use the given file_unique_id to store the file in a S3Bucket
    audio_file_key = (f'input_audios/{file_unique_id}.mp3')

    # Connects to the S3 client and uploads the audio to it
    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket=AUDIO_INPUT_BUCKET_NAME, Key=audio_file_key, Body=mp3_audio)

    # Print the url from that file to see if was uploaded correctly
    print(url = s3_client.generate_presigned_url('get_object', Params={'Bucket': AUDIO_INPUT_BUCKET_NAME, 'Key': audio_file_key}, ExpiresIn=1200))

    return audio_file_key