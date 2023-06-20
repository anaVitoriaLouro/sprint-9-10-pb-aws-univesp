#Função responsável por realizar o upload de arquivos para o Amazon S3.

import boto3

def upload_file_to_s3(file_path, bucket_name, key):
    s3_client = boto3.client('s3')
    s3_client.upload_file(file_path, bucket_name, key)
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': key},
        ExpiresIn=3600
    )
    return url