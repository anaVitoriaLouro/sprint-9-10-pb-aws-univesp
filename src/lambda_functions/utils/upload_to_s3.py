import boto3

s3 = boto3.client('s3')

def upload_file_to_s3(file_content, bucket_name, object_key):
    try:
        response = s3.put_object(Body=file_content, Bucket=bucket_name, Key=object_key)
        print('File uploaded successfully to S3.')

    except Exception as e:
        print(f'Error uploading file to S3: {e}')
        return None