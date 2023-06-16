# Função responsável por executar e fazer a interação com o Lex

import asyncio
import boto3
from upload_utils import upload_file_to_s3
from transcription_utils import wait_for_transcription_completion

def lambda_handler(event, context):
    try:
        # Extrai dados de entrada do usuário
        input_text = event['input_text']

        # Cria instâncias dos clientes fora da função lambda (escopo global)
        session = boto3.Session()
        lex_runtime = session.client('lex-runtime')
        rekognition = session.client('rekognition')
        translate = session.client('translate')
        transcribe = session.client('transcribe')



        # Processamento da entrada
        response = lex_runtime.postText(
            botName='YourBotName',
            botAlias='YourBotAlias',
            userId='User1',
            inputText=input_text
        )

        # Verifica se há uma imagem na entrada
        if response.get('dialogState') == 'ElicitSlot' and response.get('slotToElicit') == 'ImageSlot':
            # Faz o upload da imagem para o Amazon S3 e obtém a URL
            image_url = upload_file_to_s3('path/to/image.jpg', 'bucket-name', 'image.jpg')

            # Usa o Amazon Rekognition para analisar a imagem
            rekognition_response = rekognition.detect_text(
                Image={'S3Object': {'Bucket': 'bucket-name', 'Name': 'image.jpg'}}
            )
            detected_text = rekognition_response['TextDetections'][0]['DetectedText']

            # Traduza o texto, se necessário
            translation_response = translate.translate_text(
                Text=detected_text,
                SourceLanguageCode='auto',
                TargetLanguageCode='pt'
            )

        # Verifica se há áudio na entrada
        if response.get('dialogState') == 'ElicitSlot' and response.get('slotToElicit') == 'AudioSlot':
            # Faz o upload do áudio para o Amazon S3 e obtém a URL
            audio_url = upload_file_to_s3('path/to/audio.wav', 'bucket-name', 'audio.wav')

            # Usa o Amazon Transcribe para transcrever o áudio
            transcribe_response = transcribe.start_transcription_job(
                TranscriptionJobName='transcription-job',
                LanguageCode='pt',
                Media={'MediaFileUri': audio_url},
                OutputBucketName='bucket-name'
            )

            # Aguarda a conclusão da transcrição de forma assíncrona
            loop = asyncio.get_event_loop()
            loop.run_until_complete(wait_for_transcription_completion('transcription-job'))

            # Obtém o resultado da transcrição
            transcription_result_url = transcribe.get_transcription_job(
                TranscriptionJobName='transcription-job'
            )['TranscriptionJob']['Transcript']['TranscriptFileUri']

            transcription_response = session.client('s3').get_object(
                Bucket='bucket-name',
                Key=transcription_result_url[transcription_result_url.find('/')+1:]
            )['Body'].read().decode('utf-8')
            transcribed_text = json.loads(transcription_response)['results']['transcripts'][0]['transcript']

            # Usa o texto transcrito como entrada para o Amazon Lex Runtime Service
            response = lex_runtime.postText(
                botName='YourBotName',
                botAlias='YourBotAlias',
                userId='User1',
                inputText=transcribed_text
            )
        # Retornar a resposta da função lambda
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    
    except Exception as e:
        # Tratamento de erros
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }