import boto3
import configparser
import os
from botocore.exceptions import ClientError
import logging
from backend.properties import AppProperties as Props


def load_credentials():
    config = configparser.ConfigParser()
    config.read(Props.IAM_CREDENTIALS_PATH)
    aws_access_key_id = config['default']['aws_access_key_id']
    aws_secret_access_key = config['default']['aws_secret_access_key']
    return aws_access_key_id, aws_secret_access_key


def upload_file(file_path, bucket_name, object_name=None):
    """Subir un archivo a un bucket de S3

    :param file_name: Archivo a subir
    :param bucket: Bucket al que se subirá
    :param object_name: Nombre del objeto en S3. Si no se especifica, se usará el nombre del archivo
    :return: True si el archivo se subió correctamente, de lo contrario False
    """

    # Cargar las credenciales desde un archivo específico
    aws_access_key_id, aws_secret_access_key = load_credentials()

    # Crear la sesión de boto3 con las credenciales cargadas
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name='us-east-1'
    )


    # Crear el cliente de S3
    s3_client = session.client('s3')

    # Si S3 object_name no fue declarado, usar file_name
    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return False

    url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
    return url

## Ejemplo de uso
#file_path = 'path/to/your/file.pdf'
#BUCKE_NAME = 'your-bucket-name'
#OBJECT_NAME = 'file.pdf'
#
#url = upload_file(file_path, BUCKE_NAME, OBJECT_NAME)
#print(f"File uploaded to: {url}")
