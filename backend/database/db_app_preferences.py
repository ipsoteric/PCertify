from backend.database.db_create import DatabaseManagement
from backend.properties import AppProperties as Props
from utilities.utilities import encrypt_password, decrypt_password

class DBAppPreferences():

    @classmethod
    def get_data(cls):
        '''0=id, 1=compañía, 2=director, 3=email, 4=texto presentacion, 5=subtítulo, 6=descripción, 7=porcentaje, 8=contraseña, 9=ruta recursos, 10=ruta_certificados, 11=ruta qr, 12=plantilla'''

        DatabaseManagement.cursor.execute(f'''
            SELECT * FROM {Props.DB_TABLE_PREFERENCES_NAME};
        ''')

        preferences = DatabaseManagement.cursor.fetchone()
        encrypted_password = preferences[8]
        
        if encrypted_password:
            try:
                password_decrypt = decrypt_password(encrypted_password)
            except Exception as e:
                #print(f"Error decrypting password: {e}")
                password_decrypt = ''
        else:
            password_decrypt = ''

        preferences_list = list(preferences)
        preferences_list[8] = password_decrypt

        return preferences_list
    


    @classmethod
    def get_specific_data(cls, index):
        '''0=id, 1=compañía, 2=director, 3=email, 4=texto presentacion, 5=subtítulo, 6=descripción, 7=porcentaje, 8=contraseña, 9=ruta recursos, 10=ruta_certificados, 11=ruta qr, 12=plantilla'''
        
        DatabaseManagement.cursor.execute(f'''
            SELECT * FROM {Props.DB_TABLE_PREFERENCES_NAME};
        ''')
        preferences = DatabaseManagement.cursor.fetchone()
        return preferences[index]


    
    @classmethod
    def update(cls, **kwargs):
        company = kwargs.get("company", "COMPAÑIA")
        director = kwargs.get("director", "NOMBRE DEL DIRECTOR")
        email = kwargs.get("email", "alguien@example.com")
        pre_name = kwargs.get("pre_name", "TEXTO DE PRESENTACIÓN")
        post_name = kwargs.get("post_name", "Texto como subtítulo")
        description = kwargs.get("description", "Descripción: usar {{llaves}} para indicar parámetros")
        per_approval = kwargs.get("per_approval", "PORCENTAJE")
        password = kwargs.get("password", "")
        encrypted_password = encrypt_password(password)

        DatabaseManagement.cursor.execute(f'''
        UPDATE {Props.DB_TABLE_PREFERENCES_NAME}
        SET company_name = ? ,
            director_name = ? ,
            email = ? ,
            pre_name_text = ? ,
            post_name_text = ? ,
            description = ? ,
            perc_approval = ?,
            password = ?
        WHERE id = 1
        ''', (company, director, email, pre_name, post_name, description, per_approval, encrypted_password))
        
        DatabaseManagement.connection.commit()