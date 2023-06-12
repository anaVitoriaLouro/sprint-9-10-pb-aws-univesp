import json
import boto3
import requests
import os
import uuid
from utils.upload_to_s3 import upload_file_to_s3
from utils.download_audio import download_audiofile
from services.transcribe import transcribe_audio
from services.synthetize_speech import synthetize_speech

SLACK_TOKEN = os.environ['SLACK_TOKEN']

s3_client = boto3.client('s3')
bucket_name = 'sprint9-10-odhara'

def lambda_handler(event, context):
    body = json.loads(event['body'])
    #print(body)
  
    challenge = body.get('challenge')

    if challenge:
        return {
            'statusCode': 200,
            'body': challenge
        }
        
    try:
        
        if "files" in body["event"] and body["event"]["files"] and "url_private_download" in body["event"]["files"][0]:
            audio_url = body["event"]["files"][0]["url_private_download"]
            audio_file = download_audiofile(audio_url, SLACK_TOKEN)
            
            media_format = audio_url.split('.')[-1]
            print('media__format')
            print(media_format)
            
            hash_name = str(uuid.uuid4())
            
            if media_format == '.mp3':
                object_key = str(hash_name) + 'current_audio.mp3'
            else:
                object_key = str(hash_name) + 'current_audio.mp4'
    
            upload_file_to_s3(audio_file, bucket_name, object_key)
    
            print('transcription STARTED')
            transcription = transcribe_audio(bucket_name, object_key, hash_name)
            print('transcription COMPLETE')
            
            print('passed1')
            transcript_dictonary = json.loads(transcription)
            print(type(transcript_dictonary))
            print(transcript_dictonary)
            print('passed2')
            
            transcript = transcript_dictonary["results"]["transcripts"][0]["transcript"]
            print('iterated over transcript_dictonary')
            print(transcript)
            print('print transcript')
    
        if "text" in body["event"] and body["event"]["text"]:
            text = body["event"]["text"]
    
            print('synthetize_speech STARTED')
            synthetize_speech(text, bucket_name)
            print('synthetize_speech COMPLETE')
        
        return {
            'statusCode': 200,
            'body': "Synthesized audio stored in bucket."
        }
    
    except Exception as e:
        print(f'Error occurred: {str(e)}')
        return {
            'statusCode': 500,
            'body': 'Internal Server Error'
        }
