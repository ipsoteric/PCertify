from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from backend.properties import AppProperties as Props
from backend.database.db_app_preferences import DBAppPreferences
from backend.database.db_certificates import DBCertificate
from backend.local_handle import LocalHandle
import textwrap
import os
from datetime import datetime
from utilities.utilities import format_date, id_format, generate_description


def generate_certificate(fullname, course_name, date):
    #template_path = Props.PREF_TEMPLATE_IMAGE_PATH
    #output_pdf_path = Props.PREF_OUTPUT_CERTIFICATES_PATH

    # Crear la carpeta si no existe
    #LocalHandle.create_directory(output_directory)

    preferences = DBAppPreferences.get_data()
    #print(preferences)
    COMPANY = preferences[1]
    DIRECTOR = preferences[2]
    PRE_TEXT = preferences[4]
    FULLNAME : str = fullname
    SUBTITLE = preferences[5]
    COURSE : str = course_name
    PERC_APPROVAL = preferences[7]
    DESCRIPTION = generate_description(template=preferences[6], porcentaje=PERC_APPROVAL, organizacion=COMPANY)
    CERTIFICATES_FOLDER_PATH = preferences[10]
    QR_FOLDER_PATH =  preferences[11]
    TEMPLATE_PATH = preferences[12]

    LocalHandle.create_directory(CERTIFICATES_FOLDER_PATH)
    LocalHandle.create_directory(QR_FOLDER_PATH)

    # Cargar la plantilla
    img = Image.open(TEMPLATE_PATH) if os.path.exists(TEMPLATE_PATH) else Image.open(Props.TEMPLATE_IMAGE_PATH)
    draw = ImageDraw.Draw(img)
    # Obtener el tamaño de la imagen
    img_width, img_height = img.size


    #TITULO DEL DOCUMENTO
    title_text = Props.TITLE_CERTIFICATE
    title_font_path = Props.TITLE_FONT_PATH  # Debes tener una fuente TrueType (.ttf)
    title_font_size = 120
    title_font_color = Props.TEXT_COLOR_BLUE
    title_font = ImageFont.truetype(title_font_path, title_font_size)

    # Calcular la posición del texto para que esté centrado
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_position = ((img_width - text_width) / 2, 200)

    # Añadir el texto a la plantilla
    draw.text(text_position, title_text, font=title_font, fill=title_font_color)

    ## Calcular la escala adecuada para mantener las proporciones
    #page_width, page_height = letter
    ##scale = min(page_width / img_width, page_height / img_height)



    #PRESENTACIÓN
    pretext_text = PRE_TEXT
    pretext_font_path = Props.PRETEXT_FONT_PATH
    pretext_font_size = 37
    pretext_font_color = Props.TEXT_COLOR_BLUE
    pretext_font = ImageFont.truetype(pretext_font_path, pretext_font_size)

    # Calcular la posición del texto para que esté centrado
    bbox = draw.textbbox((0, 0), pretext_text, font=pretext_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_position = ((img_width - text_width) / 2, 375)
    #text_position = ((img_width - text_width) / 2, (img_height - text_height) / 2)

    # Añadir el texto a la plantilla
    draw.text(text_position, pretext_text, font=pretext_font, fill=pretext_font_color)



    #NOMBRE COMPLETO PARTICIPANTE
    user_text = FULLNAME
    user_font_path = Props.USER_FONT_PATH
    user_font_size = 95
    user_font_color = Props.TEXT_COLOR_BLACK
    user_font = ImageFont.truetype(user_font_path, user_font_size)

    # Calcular la posición del texto para que esté centrado
    bbox = draw.textbbox((0, 0), user_text, font=user_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_position = ((img_width - text_width) / 2, 470)

    # Añadir el texto a la plantilla
    draw.text(text_position, user_text, font=user_font, fill=user_font_color)



    #SUBTITULO
    subtitle_text = SUBTITLE
    subtitle_font_path = Props.SUBTITLE_FONT_PATH
    subtitle_font_size = 40
    subtitle_font_color = Props.TEXT_COLOR_BLUE
    subtitle_font = ImageFont.truetype(subtitle_font_path, subtitle_font_size)

    # Calcular la posición del texto para que esté centrado
    bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_position = ((img_width - text_width) / 2, 600)

    # Añadir el texto a la plantilla
    draw.text(text_position, subtitle_text, font=subtitle_font, fill=subtitle_font_color)



    #CURSO
    course_text = COURSE
    course_font_path = Props.COURSE_FONT_PATH
    course_font_size = 40
    course_font_color = Props.TEXT_COLOR_BLUE
    course_font = ImageFont.truetype(course_font_path, course_font_size)

    lines = textwrap.wrap(course_text, width=80)
    # Calcular la posición del texto para que esté centrado
    y = 695
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=course_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_position = ((img_width - text_width) / 2, y)
        draw.text(text_position, line, font=course_font, fill=course_font_color)
        y += text_height + (text_height*0.5)

    ## Calcular la posición del texto para que esté centrado
    #bbox = draw.textbbox((0, 0), course_text, font=course_font)
    #text_width = bbox[2] - bbox[0]
    #text_height = bbox[3] - bbox[1]
    #text_position = ((img_width - text_width) / 2, 725)
#
    ## Añadir el texto a la plantilla
    #draw.text(text_position, course_text, font=course_font, fill=course_font_color)



    #DESCRIPCIÓN
    description_text = DESCRIPTION
    description_font_path = Props.DESCRIPTION_FONT_PATH
    description_font_size = 35
    description_font_color = Props.TEXT_COLOR_BLUE
    description_font = ImageFont.truetype(description_font_path, description_font_size)

    # Dividir el texto en líneas
    lines = textwrap.wrap(description_text, width=90)

    # Calcular la posición del texto para que esté centrado
    y = 790
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=description_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_position = ((img_width - text_width) / 2, y)
        draw.text(text_position, line, font=description_font, fill=description_font_color)
        y += text_height + (text_height*0.5)



    #FECHA
    formated_date = format_date(date=date)
    date_text = f"Iquique, {formated_date}"
    date_font_path = Props.DATE_FONT_PATH
    date_font_size = 32
    date_font_color = Props.TEXT_COLOR_BLUE
    date_font = ImageFont.truetype(date_font_path, date_font_size)

    # Calcular la posición del texto para que esté centrado
    bbox = draw.textbbox((0, 0), date_text, font=date_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_position = ((img_width - text_width) / 2, 980)

    # Añadir el texto a la plantilla
    draw.text(text_position, date_text, font=date_font, fill=date_font_color)



    #DIRECTOR
    director_text = DIRECTOR
    director_font_path = Props.DIRECTOR_FONT_PATH
    director_font_size = 32
    director_font_color = Props.TEXT_COLOR_BLUE
    director_font = ImageFont.truetype(director_font_path, director_font_size)

    # Calcular la posición del texto para que esté centrado
    bbox = draw.textbbox((0, 0), director_text, font=director_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_position = ((img_width - text_width) / 2, 1230)

    # Añadir el texto a la plantilla
    draw.text(text_position, director_text, font=director_font, fill=director_font_color)



    #DIRECTOR 2
    director_text = f"Director {COMPANY}"
    director_font_path = Props.DIRECTOR2_FONT_PATH
    director_font_size = 29
    director_font_color = Props.TEXT_COLOR_BLUE
    director_font = ImageFont.truetype(director_font_path, director_font_size)

    # Calcular la posición del texto para que esté centrado
    bbox = draw.textbbox((0, 0), director_text, font=director_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_position = ((img_width - text_width) / 2, 1270)

    # Añadir el texto a la plantilla
    draw.text(text_position, director_text, font=director_font, fill=director_font_color)



    # Guardar la imagen temporalmente
    id = DBCertificate.get_last_id()
    id_formatted = id_format(id)
    temp_image_path = os.path.join(CERTIFICATES_FOLDER_PATH, "temp_certificate.png")
    img.save(temp_image_path)

    #Configurar archivo de salida
    slug_fullname = FULLNAME.replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    extension_document = ".pdf"
    extension_code = ".png"
    filename_document = f"{id_formatted}_CERTIFICADO_-_{slug_fullname}_{COURSE.replace(" ", "_")}_{timestamp}{extension_document}"
    filename_code = f"{id_formatted}_CERTIFICADO_-_{slug_fullname}_{COURSE.replace(" ", "_")}_{timestamp}{extension_code}"

    #Ruta de destino del archivo
    pdf_output_path = os.path.join(CERTIFICATES_FOLDER_PATH, filename_document)

    # Crear un PDF
    c = canvas.Canvas(pdf_output_path, pagesize=(img_width, img_height))
    c.setAuthor(author=COMPANY)
    c.setCreator(creator=Props.APP_NAME)
    c.setTitle(title=Props.FILE_TITLE)
    c.drawImage(temp_image_path, 0, 0, width=img_width, height=img_height)
    c.showPage()
    c.save()

    #Eliminar archivo temporal
    os.remove(temp_image_path)

    #Ruta para guardar el código QR (se crea en otro módulo)
    qr_file_path = os.path.join(QR_FOLDER_PATH, filename_code)

    response = {"filename":filename_document, "pdf_output_path":pdf_output_path, "qr_file_path":qr_file_path}

    return response