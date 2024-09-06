# music_uploader.py
import os
from dotenv import load_dotenv
import boto3

load_dotenv(".env")  # .env 파일 로드
access_key = os.getenv("ACCESS_KEY")
secret_key = os.getenv("SECRET_KEY")
bucket_name = os.getenv("BUCKET_NAME")

def upload_music(filename):
    s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    try:
        # 파일을 S3에 업로드하면서 Content-Disposition 설정
        with open(filename, 'rb') as file:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=filename,
                Body=file,
                ContentType='application/octet-stream',
                ContentDisposition=f'attachment; filename="{filename}"'
            )

        # S3에 업로드된 파일의 URL 생성
        url = f"https://{bucket_name}.s3.amazonaws.com/{filename}"
        return {"message": "File 업로드 성공", "url": url}, 200

    except Exception as e:
        return {"error": str(e)}, 500
