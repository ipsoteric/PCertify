import os
import shutil
from backend.properties import AppProperties as Props


class LocalHandle():

    #Encuentra y devuelve la ruta a la carpeta de archivos con la que trabajará el programa
    @classmethod
    def get_default_resources_path(cls):
            folder_name = Props.APP_RESOURCES_FOLDER_NAME
            paths = {}

            media_folder = os.path.join(os.environ['USERPROFILE'], 'Documents')
            app_resources_path = os.path.join(media_folder, folder_name)

            if not os.path.exists(app_resources_path):
                os.makedirs(app_resources_path)

            paths["resources_folder_path"] = app_resources_path
            paths["certificates_folder_path"] = cls.create_certificates_folder(app_resources_path)
            paths["QRcodes_folder_path"] = cls.create_codes_folder(app_resources_path)
            paths["template_folder_path"] = cls.create_template_folder(app_resources_path)
            #copiar plantilla y obtener ruta
            paths["template_path"] = cls.load_template(paths["template_folder_path"])
            
            return paths
    

    @classmethod
    def create_certificates_folder(cls, resources_path):

            certificates_folder_name = "certificados"
            certificates_folder_path = os.path.join(resources_path, certificates_folder_name)
            if not os.path.exists(certificates_folder_path):
                os.makedirs(certificates_folder_path)

            return certificates_folder_path
    

    @classmethod
    def create_codes_folder(cls, resources_path):

            qrcodes_folder_name = "qrcodigos"
            qrcodes_folder_path = os.path.join(resources_path, qrcodes_folder_name)
            if not os.path.exists(qrcodes_folder_path):
                os.makedirs(qrcodes_folder_path)
            return qrcodes_folder_path
    

    @classmethod
    def create_template_folder(cls, resources_path):
            
            template_folder_name = "plantilla"
            template_folder_path = os.path.join(resources_path, template_folder_name)
            if not os.path.exists(template_folder_path):
                os.makedirs(template_folder_path)

            return template_folder_path
    

    @classmethod
    def load_template(cls, template_folder_path):
        filename = Props.TEMPLATE_NAME
        source_file = Props.TEMPLATE_IMAGE_PATH
        destination_file = os.path.join(template_folder_path, filename)
        cls.copy_file(source_file, destination_file)
        return destination_file
        


    @classmethod
    def copy_file(cls, src, dest):
        shutil.copy(src, dest)
    


    @classmethod
    def create_directory(cls, path):
        if not os.path.exists(path):
            os.makedirs(path)



    @classmethod
    def generate_db_directorys(cls, paths):
        resources_path = paths[0]
        certificates_path = paths[1]
        qrcodes_path = paths[2]
        templates_path = os.path.join(resources_path,"plantilla")

        cls.create_directory(path=resources_path)
        cls.create_directory(path=certificates_path)
        cls.create_directory(path=qrcodes_path)
        cls.create_directory(path=templates_path)