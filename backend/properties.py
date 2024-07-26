from .window import Window
from cryptography.fernet import Fernet
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)



class AppProperties():

    BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    #Carpeta de assets
    ASSETS_DIR = os.path.join(BASE_DIR, 'assets/')

    #Clave secreta
    APP_SECRET_KEY = os.getenv("SECRET_KEY")
    CIPHER_SUITE = Fernet(APP_SECRET_KEY.encode())

    #Metadatos
    APP_NAME : str = "PCertify"
    APP_VERSION : str = "1.0"

    #Dimensión de ventana
    Window.calculate_window_dimentions()
    APP_WIDTH : str = str(Window.get_width())
    APP_HEIGHT : str = str(Window.get_height())
    APP_RESIZABLE_WIDTH : bool = False
    APP_RESIZABLE_HEIGHT : bool = False
    APP_BANNER_PATH : str = os.path.join(ASSETS_DIR, "pcertifybanner3.jpg")
    APP_ICON_PATH : str = os.path.join(ASSETS_DIR, "LOGO2.ico")
    APP_QR_BACKGROUND_PATH : str = os.path.join(ASSETS_DIR, "resources/qr_background_template.jpg")

    #Posición de ventana
    APP_X_POSITION : str = ""
    APP_Y_POSITION : str= ""

    #Menú principal - Opciones
    TEXT_MENU_CREATE_CERTIFICATE = "Generar certificado"
    TEXT_MENU_CREATE_CERTIFICATES = "Generar certificados por lote (No disponible)"
    TEXT_MENU_SEND_MAIL = "Historial de certificados"
    TEXT_MENU_CREATE_COURSE = "Gestionar cursos"
    TEXT_MENU_APP_SETTINGS = "Preferencias de usuario"
    WIDTH_MENU_OPTIONS = 400
    TITLE_MENU_OPTIONS = "Generador de Certificados: Menú principal"
    TEXT_BACK_HOME = "Volver al inicio"
    TEXT_SUBMIT_USER = "Generar certificado"
    TEXT_CREATE_COURSE = "Crear curso"
    TEXT_SAVE_PREF = "Guardar"
    TEXT_UPDATE = "Actualizar"
    TEXT_CANCEL_PREF = "Cancelar"
    TEXT_DELETE = "Eliminar seleccionados"
    TEXT_SELECT_COURSE = "Seleccionar curso"

    #Base de datos
    DB_NAME = "pcertify.db"
    DB_TABLE_CERTIFICATES_NAME = "certificates"
    DB_TABLE_PREFERENCES_NAME = "app_preferences"
    DB_TABLE_CERTIFICATIONS_NAME = "certifications"
    DB_TABLE_COURSES_NAME = "courses"

    #Preferencias de usuario (Labels)
    PREF_COMPANY_NAME = "Compañía:"
    PREF_DIRECTOR_NAME = "Director:"
    PREF_EMAIL = "Correo electrónico:"
    PREF_PASSWORD = "Contraseña"
    PREF_PRE_NAME = "Frase Inicial:"
    PREF_POST_NAME = "Subtítulo:"
    PREF_DESCRIPTION = "Descripción:"
    PREF_RESOURCES_PATH = "Ruta de recursos:"
    PREF_TEMPLATE_PATH = "Ruta Plantilla:"
    PREF_CERTIFICATES_PATH = "Ruta Certificados:"
    PREF_CODES_PATH = "Códigos QR:"
    PREF_PER_APPROVAL = "(%) Aprobación:"
    TEMPLATE_NAME = "PCERTIFY_TEMPLATE.png"
    TEMPLATE_IMAGE_PATH = os.path.join(ASSETS_DIR, "resources", TEMPLATE_NAME)
    #OUTPUT_CERTIFICATES_PATH = "assets/salida_temporal/certificado.pdf"
    #PREF_CERTIFICATIONS_PATH = "Ruta certificaciones"

    #Tipografía
    FONT_FOLDER = os.path.join(ASSETS_DIR, "fonts")
    TEXT_COLOR_BLUE = (32,42,71)
    TEXT_COLOR_BLACK = "black"

    #Certificado - Dibujo
    #TITULO
    TITLE_CERTIFICATE = "CERTIFICADO"
    TITLE_FONT_PATH = os.path.join(FONT_FOLDER, "LinotypeAperto-SemiBold.ttf")
    #PRESENTACION
    PRETEXT_FONT_PATH = os.path.join(FONT_FOLDER, "NivaSmallCaps-Light.ttf")
    #NOMBRE PARTICIPANTE
    USER_FONT_PATH = os.path.join(FONT_FOLDER, "spitzkant-head-light.ttf")
    #SUBTITULO
    SUBTITLE_FONT_PATH = os.path.join(FONT_FOLDER, "OpenSans-Regular.ttf")
    #CURSO
    COURSE_FONT_PATH = os.path.join(FONT_FOLDER, "OpenSans-Semibold.ttf")
    #DESCRIPCION
    DESCRIPTION_FONT_PATH = os.path.join(FONT_FOLDER, "OpenSans-Regular.ttf")
    #FECHA
    DATE_FONT_PATH = os.path.join(FONT_FOLDER, "OpenSans-Regular.ttf")
    #DIRECTOR
    DIRECTOR_FONT_PATH = os.path.join(FONT_FOLDER, "OpenSans-Semibold.ttf")
    DIRECTOR2_FONT_PATH = os.path.join(FONT_FOLDER, "OpenSans-Regular.ttf")

    #Ficheros
    APP_RESOURCES_FOLDER_NAME = "PC Certify"
    #Título para archivo
    FILE_TITLE = "Certificado de Curso"

    #AWS S3
    BUCKET_NAME = 'pcertify-certificates'
    IAM_CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.ini")

