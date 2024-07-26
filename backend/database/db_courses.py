from backend.properties import AppProperties as Props
from backend.database.db_create import DatabaseManagement

class DBCourse():
    db_table = Props.DB_TABLE_COURSES_NAME


    @classmethod
    def get_data_name(cls):
        DatabaseManagement.cursor.execute(f'''
        SELECT name FROM {cls.db_table}
        ORDER BY name ASC;
        ''')

        records = DatabaseManagement.cursor.fetchall()
        course_list = []

        for record in records:
            course_list.append(record[0])
        
        return course_list
    

    @classmethod
    def get_data(cls):
        DatabaseManagement.cursor.execute(f'''
            SELECT * FROM {cls.db_table};
        ''')

        courses = DatabaseManagement.cursor.fetchall()

        return courses
    

    @classmethod
    def get_record(cls, name):
        DatabaseManagement.cursor.execute(f'''
        SELECT id FROM {cls.db_table}
        WHERE name = ? ;
        ''', (name, ))

        record = DatabaseManagement.cursor.fetchone()

        return record[0]
    

    @classmethod
    def save(cls, name : str):
        DatabaseManagement.cursor.execute(f'''
            INSERT INTO {cls.db_table} VALUES (null, ?)
        ''', (name.upper(), ))

        DatabaseManagement.connection.commit()


    @classmethod
    def delete_courses(cls, id_list):
        placeholders = ', '.join('?' for _ in id_list)
        query = f"DELETE FROM {cls.db_table} WHERE id IN ({placeholders})"
        DatabaseManagement.cursor.execute(query, id_list)
        DatabaseManagement.connection.commit()