from datetime import datetime
import locale
from backend.properties import AppProperties as Props
import os
import sys

#Formato para guardar los nombres de los participantes
def fullname_format(value):
    fullname_formated : str = value.upper()
    return fullname_formated


def get_date():
    # Configura el locale para español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    # Obtiene la fecha actual
    today = datetime.now()

    return today


def format_date(date):
    # Formatea la fecha para mostrar el mes y el año
    fecha_formateada = date.strftime("%B de %Y")

    return fecha_formateada


# Cifrar la contraseña
def encrypt_password(password):
    return Props.CIPHER_SUITE.encrypt(str.encode(password))

# Descifrar la contraseña
def decrypt_password(encrypted_password):
    decrypt_byte = Props.CIPHER_SUITE.decrypt(encrypted_password)
    return decrypt_byte.decode()

## Codificar contraseña
#def encode_password(encrypted_password):
#    return base64.b64encode(encrypted_password).decode('utf-8')
#
## Decodificar de base64
#def decode_password(encoded_password):
#    return base64.b64decode(encoded_password)


# Formato para ID en nombre de archivo
def id_format(id):
    min_length = 4

    formatted_id = str(id).zfill(min_length)

    return formatted_id


# Generar descripción (preferencias de usuario para certificado)
def generate_description(template, porcentaje, organizacion):
    # Reemplazar los placeholders en la plantilla
    description = template.format(porcentaje=porcentaje, organizacion=organizacion)
    return description