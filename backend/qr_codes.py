#import qrcode
#
#def generate_qr_code(data, file_path):
#    """Genera un código QR y lo guarda en un archivo.
#
#    :param data: Información a codificar en el QR
#    :param file_path: Ruta donde se guardará el archivo de imagen del QR
#    """
#    # Crear un objeto QRCode
#    qr = qrcode.QRCode(
#        version=1,
#        error_correction=qrcode.constants.ERROR_CORRECT_L,
#        box_size=10,
#        border=4,
#    )
#
#    # Agregar datos al QR
#    qr.add_data(data)
#    qr.make(fit=True)
#
#    # Crear una imagen del QR
#    img = qr.make_image(fill='black', back_color='white')
#
#    # Guardar la imagen
#    img.save(file_path)


import qrcode
from PIL import Image, ImageDraw, ImageFont
from backend.properties import AppProperties as Props

def generate_qr_code(data, file_path, text="Descargue su certificado:"):
    # Generar el QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    qr_image = qr.make_image(fill='black', back_color='white').convert('RGB')
    
    # Cargar la imagen de fondo
    background_image = Image.open(Props.APP_QR_BACKGROUND_PATH).convert('RGBA')
    bg_width, bg_height = background_image.size
    
    # Tamaño del QR (ajustado para que sea un poco más grande pero sin tapar el fondo)
    qr_size = min(bg_width, bg_height) // 2  # Ajusta el tamaño del QR como quieras
    qr_size = min(bg_width-240, bg_height-240)
    
    # Redimensionar el QR al tamaño deseado
    qr_image = qr_image.resize((qr_size, qr_size))
    
    # Crear una nueva imagen con el fondo
    combined_image = Image.new('RGBA', (bg_width, bg_height))
    combined_image.paste(background_image, (0, 0))
    
    # Convertir qr_image a 'RGBA' para asegurar que no tenga problemas con la transparencia
    qr_image = qr_image.convert('RGBA')
    
    # Calcular la posición del QR para centrarlo
    qr_x = (bg_width - qr_size) // 2
    qr_y = ((bg_height - qr_size) // 2) + 50
    
    # Pegar el QR en la imagen combinada
    combined_image.paste(qr_image, (qr_x, qr_y), qr_image)
    
    # Agregar texto centrado
    if text:
        draw = ImageDraw.Draw(combined_image)
        try:
            font = ImageFont.truetype("calibri.ttf", 40)
        except IOError:
            font = ImageFont.load_default()
        
        # Calcular el tamaño del texto
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Calcular la posición del texto para centrarlo
        text_x = (bg_width - text_width) // 2
        #text_y = (bg_height - text_height) // 2
        text_y = 70
        
        # Agregar el texto a la imagen
        draw.text((text_x, text_y), text, fill="white", font=font)

    # Guardar la imagen final
    combined_image = combined_image.convert('RGB')
    combined_image.save(file_path)