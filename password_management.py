import sqlite3
import bcrypt

from main import PMWindow

class PasswordManager:
    def __init__(self, master):
        self.master = master
        
        self.conn = sqlite3.connect("passwords.db")
        self.cursor = self.conn.cursor()

        # checks is the passwords table exists
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='passwords'"
        )

        if self.cursor.fetchone() == None:
            self.create_password_table()

        self.check_for_master_pw()
    
    def create_password_table(self):
        self.cursor.execute("""
            CREATE TABLE passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service VARCHAR(50) NOT NULL,
                user VARCHAR(50),
                password VARCHAR(50) NOT NULL
            )
        """)

        self.conn.commit()
        self.conn.close()

    def check_for_master_pw(self):
        """Checks of there is master password."""
        self.cursor.execute(
            "SELECT * FROM passwords WHERE service='master'"
        )

        if self.cursor.fetchone() == None:
            PMWindow(self.master).add_password_window(mp=True)

    def encrypt_pw(self, pw):
        pw = pw.encode()
        pw = bcrypt.hashpw(pw, bcrypt.gensalt())
        print(pw)
        #return pw
    
    def add_password_to_db(self, service, password, user=""):
        self.cursor.execute(
            "INSERT INTO passwords VALUES (null, ?, ?, ?)",
            [service, user, password]
        )
        self.conn.commit()
        self.conn.close()

    def delete_password(self, id_):
        self.cursor.execute("DELETE FROM passwords WHERE id = ?", id_)