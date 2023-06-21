import os
from telegram_tools.send_audio_message import telegram_send_audio
from telegram_tools.send_image_message import telegram_send_image
from telegram_tools.send_text_message import telegram_send_text
from services.text_rekognition import img2txt
from services.lex_interface import lex_view_message
from services.synthesize_speech import synthesize_speech
from services.transcribe import transcribe_audio

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

# essa função serve pra manejar as mensagens enviadas pelo lex e enviar os resultados de volta pro telegram

def manage_messages(message, session_id, chat_id):
  try:
    # Send message to Lex and wait to get the response
    lex_response = lex_view_message(message, session_id)
    # Print Lex response for debug
    print(f'THIS IS THE LEX RESPONSE: {lex_response}')
    
    #session_state = lex_response['sessionState']
    intent_name = lex_response['sessionState']['intent']['name']
    print(intent_name)
    
    # /     \     /     \     /     \     /     \     /     \     /     \
    ## TRANSCRIBE intent management /1
    # Check to see if we're on the Transcribe Intent, if so, captures the value passed in the slot and executes the Synthesize Audio service
    if intent_name == 'transcribeIntent':
      if lex_response['sessionState']['dialogAction']['type'] == 'ConfirmIntent' and 'value' in lex_response['sessionState']['intent']['slots']['AudioPath']:
        audio_to_process = lex_response['sessionState']['intent']['slots']['AudioPath']['value']['interpretedValue']
        print(f'this is the audio_to_process file_key: {audio_to_process}')
        
        text_from_audio = transcribe_audio(audio_to_process)
        ## A TAREFA DE TRANSCRIÇÃO TÁ FALHANDO POR ERRO DE COMPATIBILIDADE DO ARQUIVO DE AUDIO
          ## ELE VEM DO TELEGRAM COMO .OGA, MAS NÃO CONSEGUI FAZER A CONVERSÃO PRA MP3 AQUI DENTRO DO LAMBDA
            ## O QUE TEM ACONTECIDO É SÓ MUDAR A EXTENSÃO DO ARQUIVO DE .OGA PARA .MP3
              ## NÃO REPRODUZ LOCALMENTE NO WINDOWS MEDIA PLAYER, MAS "JOGANDO O ARQUIVO" NUMA NOVA ABA DO NAVEGADOR ELE REPRODUZ
                ## O TRANSCRIBE NÃO ACEITA ARQUIVO .OGA
                  ## ENGRAÇADO QUE ATÉ OUTRO DIA TAVA FUNCIONANDO DESSA FORMA, AGORA NÃO ESTÁ MAIS
        print(f'this should be the text result: {text_from_audio}')
        
        # This is just a massage to send back to the user before we send the actual audio
        messages = ['Ótimo, acabei de trasncrever sua mensagem de áudio.', 'Estou te enviando o resultado.', text_from_audio]
        telegram_send_text(messages, chat_id)
  
    ## POLLY intent management /2
    # Check to see if we're on the Polly Intent, if so, captures the value passed in the slot and executes the Synthesize Audio service
    if intent_name == 'pollyIntent':
      if lex_response['sessionState']['dialogAction']['type'] == 'ConfirmIntent' and 'value' in lex_response['sessionState']['intent']['slots']['textSpeech']:
        text_to_process = lex_response['sessionState']['intent']['slots']['textSpeech']['value']['interpretedValue']
        print(f'this is the text_to_process: {text_to_process}')
        
        audio_from_text = synthesize_speech(text_to_process)
        print(f'this should be the url: {audio_from_text}')
        
        # This is just a massage to send back to the user before we send the actual audio
        messages = ['Ok, vou gerar um áudio com a partir do seu texto.', 'Pronto, aqui está o áudio criado com base no texto contido na sua mensagem.']
        telegram_send_text(messages, chat_id)
        
        # Send the Syhtnesized audio to the Telegram Chat
        telegram_send_audio(audio_from_text, chat_id, TELEGRAM_TOKEN)

    ## REKOGNITION intent management /3
    # Check to see if we're on the Rekognition Intent, if so, captures the value passed in the slot and executes the DetectTextService service
    if intent_name == 'rekoIntent':
      if lex_response['sessionState']['dialogAction']['type'] == 'ConfirmIntent' and 'value' in lex_response['sessionState']['intent']['slots']['ImagePath']:
        image_to_process = lex_response['sessionState']['intent']['slots']['ImagePath']['value']['interpretedValue']
        print(f'this is the image to proccess: {image_to_process}')
        
        # This processes the image and creates the audiofile
        audio_from_image = img2txt(image_to_process)
        
        # This is just a massage to send back to the user before we send the actual audio
        messages = ['Ok, recebi sua imagem, estou preparando o áudio.', 'Pronto, aqui está o áudio criado com base no que tem escrito na imagem que você me enviou.']
        telegram_send_text(messages, chat_id)
        
        # Now this sends the audio message
        telegram_send_audio(audio_from_image, chat_id, TELEGRAM_TOKEN)
        
        # FALTA ENCERRAR A SESSÃO COM O LEX PRA PODER REINICIAR O SERVIÇO 3 COM UMA IMAGEM DIFERENTE
          # ELE TEM MANTIDO A MESMA IMAGEM PARA GERAR UM PRÓXIMO AUDIO, NÃO CHAMA O SLOT PARA PREENCHER O SLOT NOVAMENTE.
        
    # /     \     /     \     /     \     /     \     /     \     /     \   

    # Check if there are any PlainText messages in the Lex response
    if 'messages' in lex_response:
      messages = [message['content'] for message in lex_response['messages'] if message['contentType'] == 'PlainText']
      if messages:
        # Send the messages to Telegram
        response = telegram_send_text(messages, chat_id)
        # print(f'PRINT LEX RESPONSE FOR DEBUG {response.text}')
        print('resposta do lex foi para o telegram')

        # Return the response as the API response
        return {
          'statusCode': response.status_code,
          'body': response.text
        }
  
  except Exception as e:
    return {
			'statusCode': 500,
			'body': f'Something bad has happened, run to the hills! This is why: {str(e)}'
		}