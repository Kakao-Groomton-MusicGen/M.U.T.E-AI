import os
from dotenv import load_dotenv
import boto3

load_dotenv(".env")  # .env 파일 로드
access_key = os.getenv("ACCESS_KEY")
secret_key = os.getenv("SECRET_KEY")
bucket_name = os.getenv("BUCKET_NAME")

def upload_music(file_name):
    s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    # 파일을 S3에 업로드하면서 Content-Disposition 설정
    s3_client.put_object(
        Bucket=bucket_name,
        Key=filename,
        Body=open(filename, 'rb'),
        ContentType='application/octet-stream',
        ContentDisposition=f'attachment; filename="{filename}"'
    )

    return jsonify({"message": "File 업로드 성공", "filename": filename}), 200

