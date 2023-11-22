import mysql.connector

class sessionManager:
    def __init__(self, host="localhost", user="root", password="pranavmysql", database="newuserdb"):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        self.create_table()

        

    def create_table(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                username VARCHAR(255) NOT NULL
            )
        ''')      
        self.db.commit()

    def set_current_user(self, username):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO sessions (username) VALUES (%s)", (username, ))
        self.db.commit()

    def get_current_user(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT username FROM sessions ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    
    def remove_session(self, username):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM sessions WHERE username = %s", (username,))
        self.db.commit()