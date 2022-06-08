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
            implementation_rating INTEGER DEFAULT 1000,
            dp_rating INTEGER DEFAULT 1000,
            graph_rating INTEGER DEFAULT 1000,
            math_rating INTEGER DEFAULT 1000,
            datastructure_rating INTEGER DEFAULT 1000,
            greedy_rating INTEGER DEFAULT 1000);
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS CHALLENGES
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id INTEGER NOT NULL,
            problemname TEXT NOT NULL,
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
            SELECT cf_handle, implementation_rating, datastructure_rating, graph_rating, math_rating, dp_rating, greedy_rating FROM USERS 
            WHERE discord_id = ?
        '''
        res = self.conn.execute(sql, (discord_id,))
        texts = ["handle", "implementation", "data structures", "graphs", "math", "dp", "greedy"]
        ratings = res.fetchone()
        print(F"Current rating: {ratings}")
        return list(zip(texts, ratings))
    
    def update_ratings(self, discord_id, ratings):
        print(F"Update rating: {ratings}")
        texts = ["implementation_rating", "datastructure_rating", "graph_rating", "math_rating", "dp_rating" , "greedy_rating"]
        for text, rating in list(zip(texts, ratings)):
            sql = "UPDATE USERS SET {} = ? WHERE discord_id = ?".format(text)
            self.conn.execute(sql, (rating, discord_id))
        self.conn.commit()
        
    def insert_challenge(self, discord_id : int, problemname : str, time : int):
        sql = ''' 
            INSERT INTO CHALLENGES(discord_id, problemname, time)
            VALUES(?,?,?)
        '''
        challenge = (discord_id, problemname, time)
        print(challenge)
        self.conn.execute(sql, challenge)
        self.conn.commit()

    def get_challenge(self, discord_id : int):
        sql = '''
            SELECT problemname, time FROM CHALLENGES
            WHERE discord_id = ?
        '''
        res = self.conn.execute(sql, (discord_id,))
        return res.fetchone()
    
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
    db.conn.execute("DROP TABLE challenges")
    db.conn.commit()
