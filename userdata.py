import sqlite3, json

class Codeforces:
    def __init__(self): # create an empty user database
        self.conn = sqlite3.connect('users.db')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS USERS
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            guild INTEGER NOT NULL,
            username TEXT NOT NULL,
            cf_handle TEXT ,
            rating TEXT);
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS CHALLENGES
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            guild INTEGER NOT NULL,
            username TEXT NOT NULL,
            problemname TEXT NOT NULL,
            difficulty INTEGER NOT NULL,
            time INTEGER NOT NULL);
        ''')


    def insert(self, guild : int, username : str, cf_handle : str, rating = {}): # insert a user in database
        if self.get_user(guild, username) != []:
            print("User exists!")
            return 
        sql = ''' 
            INSERT INTO USERS(guild, username, cf_handle, rating)
            VALUES(?,?,?,?)
        '''
        user = (guild, username, cf_handle, json.dumps(rating))
        print(user)
        self.conn.execute(sql, user)
        self.conn.commit()

    def get_user(self, guild : int, usr : str):
        sql = ('SELECT * FROM USERS WHERE guild = ? AND username = ?')
        res = self.conn.execute(sql, (guild, usr))
        return res.fetchall()
    
    def insert_challenge(self, guild : int, username : str, problemname : str, difficulty : int, time : int):
        sql = ''' 
            INSERT INTO CHALLENGES(guild, username, problemname, difficulty, time)
            VALUES(?,?,?,?,?)
        '''
        challenge = (guild, username, problemname, difficulty, time)
        self.conn.execute(sql, challenge)
        self.conn.commit()

    def get_challenge(self, guild : int, username : str):
        sql = ('SELECT problemname, difficulty, time FROM CHALLENGES WHERE guild = ? AND username = ?')
        res = self.conn.execute(sql, (guild, username))
        return res.fetchall()
    
    def delete_challenge(self, guild : int, username : str):
        sql = ''' 
            DELETE FROM CHALLENGES
            WHERE guild = ? AND username = ?
        '''
        user = (guild, username)
        self.conn.execute(sql, user)
        self.conn.commit()




if __name__ == "__main__":
    db = Codeforces()
    db.conn.execute("DELETE FROM CHALLENGES")
    db.insert(1234, "enip", "enip", {"dp" : 1900, "data_structure" : 100})
    print(db.get_user(1234, "enip"))
    db.conn.commit()