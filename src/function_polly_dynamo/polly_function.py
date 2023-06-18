import boto3
import dynamo_function

polly = boto3.client('polly')
s3 = boto3.client('s3')

def put_speech(event, context):

    print("Iniciando síntese de texto")

    text = dynamo_function.ddb_raffle()

    response = polly.start_speech_synthesis_task(
        OutputS3BucketName='audio-polly-sprint10',
        OutputS3KeyPrefix='audio_polly.mp3',
        Engine='neural',
        LanguageCode='pt-BR',
        OutputFormat='mp3',
        Text=text,
        VoiceId='Camila'
    )
    print(response)
    print("Arquivo de áudio criado")