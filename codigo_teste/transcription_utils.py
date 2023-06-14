# Função responsável por aguardar a conclusão do trabalho de transcrição.

import asyncio
import boto3

async def wait_for_transcription_completion(job_name):
    transcribe_client = boto3.client('transcribe')
    while True:
        job_status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        if job_status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        await asyncio.sleep(5)