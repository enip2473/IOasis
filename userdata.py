import sqlite3, json

class db:
    def __init__(self): # create an empty user database
        self.conn = sqlite3.connect('test.db')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS USERS
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT NOT NULL,
            cf_handle TEXT ,
            rating TEXT);
        ''')


    def insert(self, username : str, cf_handle : str, rating = {}): # insert a user in database
        sql = ''' 
            INSERT INTO USERS(username,cf_handle,rating)
            VALUES(?,?,?)
        '''
        user = (username, cf_handle, json.dumps(rating))
        self.conn.execute(sql, user)
        self.conn.commit()

    def get_user(self, usr : str):
        sql = ('SELECT * FROM USERS WHERE username = ?')
        res = self.conn.execute(sql, (usr,))
        return res.fetchall()


if __name__ == "__main__":
    db = db()
    db.insert("enip", "enip", {"dp" : 1900, "data_structure" : 100})
    print(db.get_user("enip"))