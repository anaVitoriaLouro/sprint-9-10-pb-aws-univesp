import json
import boto3
import requests
import os
import uuid
from utils.upload_to_s3 import upload_file_to_s3
from utils.download_audio import download_audiofile
from modules.get_transcript import get_transcript
from modules.get_speech import get_speech

SLACK_TOKEN = os.environ['SLACK_TOKEN']

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
		print(get_transcript(body))
		get_speech(body)

		return {
			'statusCode': 200,
			'body': 'All jobs have been completed with elegance.'
		}

	except Exception as e:
		print(f'Error occurred: {str(e)}')
		return {
			'statusCode': 500,
			'body': 'Something went abruptly wrong. Call 911.'
		}


def health():
	body = 'health function is working'

	return {
		'statusCode': 200,
		'body': body
	}
