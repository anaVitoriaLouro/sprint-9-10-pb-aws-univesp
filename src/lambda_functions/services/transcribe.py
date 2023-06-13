import boto3
import uuid
import os
from utils.generate_id import generate_random_uuid

# Create a Transcribe client
transcribe = boto3.client('transcribe')

TEXT_OUTPUT_BUCKET_NAME = os.environ['TEXT_OUTPUT_BUCKET_NAME']

def transcribe_audio(bucket_name, object_key, uuid):

    try:
        # Extract the media format from the object_key
        media_format = object_key.split('.')[-1]

        hash_name = generate_random_uuid()
        
        # Configure the transcription job
        transcribe_job = {
            'TranscriptionJobName': hash_name,
            'LanguageCode': 'pt-BR',
            'MediaFormat': media_format,
            'Media': {
                'MediaFileUri': f's3://{bucket_name}/{object_key}'
            },
            'OutputBucketName': TEXT_OUTPUT_BUCKET_NAME
        }

        # Start the transcription job
        response = transcribe.start_transcription_job(**transcribe_job)

        # Wait for the transcription job to complete or fail
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=response['TranscriptionJob']['TranscriptionJobName'])
            if status['TranscriptionJob']['TranscriptionJobStatus'] == 'FAILED':
                failure_reason = status['TranscriptionJob']['FailureReason']
                print(f'TranscriptionJob has failed unexpectedly bescause: {failure_reason}.')
                break

        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            transcribed_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            print('TranscriptionJob has been completed!')
            transcribed_text = boto3.client('s3').get_object(Bucket=bucket_name, Key=transcribed_uri.split('/')[-1])['Body'].read().decode('utf-8')
            return transcribed_text
        else:
            failure_reason = status['TranscriptionJob']['FailureReason']
            raise Exception(f'Transcription failed with delight. Job status: {status["TranscriptionJob"]["TranscriptionJobStatus"]}. And the failure reason is: {failure_reason}')

    except Exception as e:
        raise Exception(f'Transcription failed with error: {str(e)}')