import sqlite3
from backend.properties import AppProperties as Props
from backend.local_handle import LocalHandle


class DatabaseManagement():

    db_name = Props.DB_NAME
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    @classmethod
    def create_tables(cls):
        cls.cursor.executescript(f'''
        CREATE TABLE IF NOT EXISTS {Props.DB_TABLE_PREFERENCES_NAME} (
            id INTEGER PRIMARY KEY,
            company_name VARCHAR(100) NOT NULL,
            director_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            pre_name_text TEXT,
            post_name_text TEXT,
            description TEXT,
            perc_approval INTEGER,
            password BLOB,
            resources_folder_path TEXT,
            certificates_folder_path TEXT,
            qrcodes_folder_path TEXT,
            template_path TEXT
        );

        CREATE TABLE IF NOT EXISTS {Props.DB_TABLE_COURSES_NAME} (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS {Props.DB_TABLE_CERTIFICATIONS_NAME} (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            image TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS {Props.DB_TABLE_CERTIFICATES_NAME} (
            id INTEGER PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100),
            is_send INTEGER,
            courses_id INTEGER NOT NULL,
            image VARCHAR(200),
            create_date DATE NOT NULL,
            FOREIGN KEY (courses_id) REFERENCES {Props.DB_TABLE_COURSES_NAME}(id)
        );
        ''')


        # Insertar un registro por defecto si la tabla está vacía
        cls.cursor.execute(f'SELECT COUNT(*) FROM {Props.DB_TABLE_PREFERENCES_NAME}')
        if cls.cursor.fetchone()[0] == 0:

            paths = LocalHandle.get_default_resources_path()
            resources_folder_path = paths["resources_folder_path"]
            certificates_folder_path = paths["certificates_folder_path"]
            qrcodes_folder_path = paths["QRcodes_folder_path"]
            template_path = paths["template_path"]

            cls.cursor.execute(f'''
                INSERT INTO {Props.DB_TABLE_PREFERENCES_NAME} (company_name, director_name, email, pre_name_text, post_name_text, description, perc_approval, password, resources_folder_path, certificates_folder_path, qrcodes_folder_path, template_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('CIED CHILE SPA.', 'VICTOR PEREZ GASPAR', 'vperez@ciedchile.com', 'SE OTORGA EL SIGUIENTE CERTIFICADO A DON:', 'Por haber aprobado satisfactoriamente el curso de:', 'Quien aprueba evaluación de manera teórica y práctica, acreditando habilidad, competencia y destreza necesaria obteniendo una aprobación superior a {porcentaje}% en el global dictado por {organizacion} Número de registro INN: A-11380 - NCh: 2728:2015.', 90, None, resources_folder_path, certificates_folder_path, qrcodes_folder_path, template_path))

            cls.connection.commit()

        else:
            cls.cursor.execute(f'SELECT * FROM {Props.DB_TABLE_PREFERENCES_NAME};')
            result = cls.cursor.fetchone()
            paths = [result[9], result[10], result[11], result[12]]
            LocalHandle.generate_db_directorys(paths)
    

    @classmethod
    def close_connection(cls):
        cls.connection.close()