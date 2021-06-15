import sqlite3, json

class Codeforces:
    def __init__(self): # create an empty user database
        self.conn = sqlite3.connect('users.db')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS USERS
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            password TEXT,
            discord_id INTEGER,
            cf_handle TEXT,
            implementation_rating INTEGER DEFAULT 0,
            dp_rating INTEGER DEFAULT 0,
            graph_rating INTEGER DEFAULT 0,
            math_rating INTEGER DEFAULT 0,
            datastructure_rating INTEGER DEFAULT 0,
            greedy_rating INTEGER DEFAULT 0);
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS CHALLENGES
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id INTEGER NOT NULL,
            problemname TEXT NOT NULL,
            difficulty INTEGER NOT NULL,
            time INTEGER NOT NULL);
        ''')


    def insert_user(self, discord_id, cf_handle : str): # insert a user in database
        if self.get_handle(discord_id) != "":
            print("User exists!")
            return 
        sql = ''' 
            INSERT INTO USERS(discord_id, cf_handle)
            VALUES(?,?)
        '''
        user = (discord_id, cf_handle)
        print(user)
        self.conn.execute(sql, user)
        self.conn.commit()

    def get_handle(self, discord_id):
        sql = 'SELECT cf_handle FROM USERS WHERE discord_id = ?'
        res = self.conn.execute(sql, (discord_id,))
        try:
            handle = res.fetchone()[0]
        except:
            handle = ""
        return handle

    def get_ratings(self, discord_id):
        sql = '''
            SELECT cf_handle, implementation_rating, dp_rating, graph_rating, math_rating, datastructure_rating, greedy_rating FROM USERS 
            WHERE discord_id = ?
        '''
        res = self.conn.execute(sql, (discord_id,))
        texts = ["handle", "implementation", "dp", "graph", "math", "data structure", "greedy"]
        ratings = res.fetchone()
        return list(zip(texts, ratings))
        
    def insert_challenge(self, discord_id : int, problemname : str, difficulty : int, time : int):
        sql = ''' 
            INSERT INTO CHALLENGES(discord_id, problemname, difficulty, time)
            VALUES(?,?,?,?)
        '''
        challenge = (discord_id, problemname, difficulty, time)
        self.conn.execute(sql, challenge)
        self.conn.commit()

    def get_challenge(self, discord_id : int):
        sql = '''
            SELECT problemname, difficulty, time FROM CHALLENGES
            WHERE discord_id = ?
        '''
        res = self.conn.execute(sql, (discord_id,))
        return res.fetchall()
    
    def delete_challenge(self, discord_id : int):
        sql = ''' 
            DELETE FROM CHALLENGES
            WHERE discord_id = ?
        '''
        self.conn.execute(sql, (discord_id, ))
        self.conn.commit()

if __name__ == "__main__":
    db = Codeforces()
    db.insert_user(1234, "enip")
    print(db.get_handle(1234))