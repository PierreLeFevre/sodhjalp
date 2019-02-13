from ..database import mysql

class sodUser():

    def __init__(self, token):
        
        cur = mysql.get_db().cursor()
        result = cur.execute("SELECT * FROM Accounts WHERE token=%s", [token])

        rv = cur.fetchone()

        self.token = token

        self.username = rv[1]
        self.created_at = rv[3]
        self.type = rv[4]


    def get_all_posts_from_user(self):

        cur = mysql.get_db().cursor()
        result = cur.execute("SELECT * FROM Posts WHERE id=%s", [self.token])

        if (result < 1):
            return None

        rv = cur.fetchall()

        return str(rv)




