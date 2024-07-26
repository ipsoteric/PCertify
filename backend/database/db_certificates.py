from .db_create import DatabaseManagement
from backend.properties import AppProperties as Props
from .db_courses import DBCourse


class DBCertificate():

    db_table=Props.DB_TABLE_CERTIFICATES_NAME

    @classmethod
    def save_certificate(cls, fullname : str, email : str, course, date):
        #Aplicar formato
        email_cleanned = email.lower()
        id_course = DBCourse.get_record(course)

        DatabaseManagement.cursor.execute(f'''
            INSERT INTO {cls.db_table} (fullname, email, courses_id, create_date, is_send, image)
            VALUES(?, ?, ?, ?, ?, ?)
        ''', (fullname, email_cleanned, id_course, date, 0, "certificadoprueba.jpg"))

        DatabaseManagement.connection.commit()

    

    @classmethod
    def get_certificates(cls):
        courses = Props.DB_TABLE_COURSES_NAME
        DatabaseManagement.cursor.execute(f'''
        SELECT ce.id, ce.fullname, ce.email, ce.is_send, {courses}.name, ce.image, ce.create_date FROM {cls.db_table} ce
        INNER JOIN {courses} ON ce.courses_id = {courses}.id
        ''')

        certificates = DatabaseManagement.cursor.fetchall()

        return certificates
    


    @classmethod
    def get_last_id(cls):
        query = f"SELECT MAX(id) FROM {cls.db_table}"
        DatabaseManagement.cursor.execute(query)

        result = DatabaseManagement.cursor.fetchone()[0]

        return result if result is not None else 1
    
    

    @classmethod
    def get_selected_certificates(cls, id_list):
        placeholders = ', '.join('?' for _ in id_list)
        query = f"SELECT * FROM {cls.db_table} WHERE id IN ({placeholders})"
        DatabaseManagement.cursor.execute(query, id_list)

        records_selected = DatabaseManagement.cursor.fetchall()

        return records_selected
    


    @classmethod
    def delete_certificates(cls, id_list):
        placeholders = ', '.join('?' for _ in id_list)
        query = f"DELETE FROM {cls.db_table} WHERE id IN ({placeholders})"
        DatabaseManagement.cursor.execute(query, id_list)
        DatabaseManagement.connection.commit()
