import json
import boto3
import requests
import os
from services.lex_interface import handle_lex_event
from modules.manage_messages import manage_messages
from telegram_tools.download_audio import download_audio
from telegram_tools.download_image import download_image
from utils.generate_session_id import generate_session_id

from services.textRekognition import img2txt
from telegram_tools.send_audio_message import telegram_send_audio
def manager(event, context):
	print(event)
	try:
		# Handle Telegram event
		if 'body' in event:
			body = json.loads(event['body'])
			chat_id = str(body['message']['chat']['id'])

			# Generate a session ID for the user
			session_id = generate_session_id(chat_id)

			# Handle text, photo & audio messages
			if 'message' in body:
				message = None
				if 'text' in body['message']:
					message = body['message']['text']

				elif 'voice' in body['message']:
					audiofile_id = body['message']['voice']['file_id']
					audiofile_unique_id = body['message']['voice']['file_unique_id']
					# Get the uploaded audiofile from Telegram
					audiofile_key = download_audio(audiofile_id, audiofile_unique_id)
					# Aqui passa pro lex o nome do arquivo, para poder preencher o slot
					message = audiofile_key

				elif 'photo' in body['message']:
					imagefile_id = body['message']['photo'][-1]['file_id']
					imagefile_unique_id = body['message']['photo'][-1]['file_unique_id']
					# Get the uploaded image from Telegram
					imagefile_key = download_image(imagefile_id, imagefile_unique_id)
					# Set the file_key as the message for handling
						# Aqui passa pro lex o nome do arquivo, para poder preencher o slot
					message = imagefile_key
					
					#handle_lex_event(event, context)
					synthesized_speech_url = img2txt(message)
					telegram_send_audio(synthesized_speech_url, chat_id, os.environ['TELEGRAM_TOKEN'])
					#telegram_send_audio(audio_url, chat_id, os.environ['TELEGRAM_TOKEN'])
				

				print('Teste out:')
				print(message)
				# Precisa implementar a partir daqui
				if message is not None:
					return manage_messages(message, session_id, chat_id)
		
		
		# Não existe um 'sessionState' nem 'sessionId' dentro do log do evento. 
		# Dentro do 'body' do log há um 'requestContext', mas seu array não contém sessionState, por isso o if sempre falha
		# Handle Lex event
		if 'sessionId' in event and 'sessionState' in event:
			return handle_lex_event(event, context)

		# For some reason Telegram will only work if the statusCode 200 is sent back with a OK message 
		return {
			'statusCode': 200,
			'body': 'OK'
		}

	except Exception as e:
		print(f'Something went abruptly wrong. Call 911. An error occurred: {str(e)}')

def health():
	body = 'health function is working'

	return {
		'statusCode': 200,
		'body': body
	}