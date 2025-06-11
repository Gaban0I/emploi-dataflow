import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from src.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME, REGION

def upload_file_to_s3(local_path: str, s3_path: str) -> bool:
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=REGION
        )
        s3.upload_file(local_path, BUCKET_NAME, s3_path)
        print(f"✅ Fichier '{local_path}' uploadé sur S3 dans '{s3_path}'")
        return True
    except FileNotFoundError:
        print("❌ Fichier local introuvable.")
    except NoCredentialsError:
        print("❌ Identifiants AWS invalides.")
    except ClientError as e:
        print("❌ Erreur S3 :", e)
    return False

# Test simple
if __name__ == "__main__":
    upload_file_to_s3("fichier_test.txt", "test/fichier_test.txt")
