'''
Este script tem como objetivo realizar a extração do áudio no bucket S3 e converte-lo em texto,

o tratamento é necessário para enviar no formato correto para o bot Lex.

'''
import boto3

def transcribe_audio_to_text(bucket_name, audio_file_name):

    # 1- Configurar cliente do serviço Transcribe
    transcribe_client = boto3.client('transcribe')

    # 2 - Configurar o nome do job de transcrição
    job_name = "transcribe_job"

    # 3 - Definir as configurações de entrada para o job de transcrição
    transcribe_settings = {
        "LanguageCode": "pt-BR", # Escolha do idioma
        "Media": {
            "MediaFileUri": f"s3://{bucket_name}/{audio_file_name}"
        }
    }

    # 4 - Iniciar o job de transcrição
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media=transcribe_settings["Media"],
        MediaFormat="mp3",  # Formato do áudio
        LanguageCode=transcribe_settings["LanguageCode"]
    )

    # 5 - Aguardar a conclusão do job de transcrição
    while True:
        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        if response["TranscriptionJob"]["TranscriptionJobStatus"] in ["COMPLETED", "FAILED"]:
            break

    # 6 - Obter o resultado da transcrição
    if response["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        transcribe_result_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        transcribe_result = boto3.client("s3").get_object(Bucket=bucket_name, Key=transcribe_result_uri.split('/')[-1])
        transcribe_text = transcribe_result["Body"].read().decode("utf-8")
        return transcribe_text
    else:
        print("Falha na transcrição.")
        return None

# 7 - Definção do bucket direcionado
bucket_name = "XxXxX"
audio_file_name = "XxXxX.mp3"
transcribed_text = transcribe_audio_to_text(bucket_name, audio_file_name)

# 8 - Resultado da transcrição
print(transcribed_text)
print(type(transcribed_text))


