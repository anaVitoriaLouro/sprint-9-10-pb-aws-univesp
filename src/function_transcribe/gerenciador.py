import boto3

#Cria instâncias dos clientes fora da função lambda (escopo global)
lex_runtime = session.client('lex-runtime')
rekognition = session.client('rekognition')
translate = session.client('translate')
transcribe = session.client('transcribe')

# Entrada do usuário
input_text = input("Digite a entrada do usuário: ")

# Processamento da entrada
#Obs: Colocar informações referentes ao bot
response = lex_runtime.postText(
    botName='YourBotName',
    botAlias='YourBotAlias',
    userId='User1',
    inputText=input_text
)

# Verifica se há uma imagem ou áudio na entrada
if response.get('dialogState') == 'ElicitSlot' and response.get('slotToElicit') == 'ImageSlot':
    # Faz o upload da imagem para o Amazon S3 e obtém a URL
    # Trocar 'bucket-name' para o nome do bucket
    s3_client = session.client('s3')
    s3_client.upload_file('path/to/image.jpg', 'bucket-name', 'image.jpg')
    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': 'bucket-name', 'Key': 'image.jpg'},
         ExpiresIn=3600   #Tempo de expiração da URL em segundos
    )

    # Use o Amazon Rekognition para analisar a imagem
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
    # Trocar 'bucket-name' para o nome do bucket
    s3_client = session.client('s3')
    s3_client.upload_file('path/to/audio.wav', 'bucket-name', 'audio.wav')
    audio_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': 'bucket-name', 'Key': 'audio.wav'},
        ExpiresIn=3600  # Tempo de expiração da URL em segundos
    )

    # Use o Amazon Transcribe para transcrever o áudio
    transcribe_response = transcribe.start_transcription_job(
        TranscriptionJobName='transcription-job',
        LanguageCode='pt',
        Media={'MediaFileUri': audio_url},
        # substituir pelo nome do bucket onde salvar a transcrição
        OutputBucketName='bucket-name'
    )

    # Aguarde a conclusão da transcrição
    transcribe_client = session.client('transcribe')
    while True:
        job_status = transcribe_client.get_transcription_job(
            TranscriptionJobName='transcription-job')
        if job_status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break

    # Obtém o resultado da transcrição
    transcription_result_url = job_status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    transcription_response = session.client('s3').get_object(
        Bucket='bucket-name', Key=transcription_result_url[transcription_result_url.find('/')+1:])['Body'].read().decode('utf-8')
    transcribed_text = json.loads(transcription_response)[
        'results']['transcripts'][0]['transcript']

    # Usa o texto transcrito como entrada para o Amazon Lex Runtime Service
    response = lex_runtime.postText(
        botName='YourBotName',
        botAlias='YourBotAlias',
        userId='User1',
        inputText=transcribed_text
    )

# Interação com o chatbot
print(response['message'])
