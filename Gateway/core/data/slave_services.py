import database as db

def get_slave():
    db = get_db()
    user = db.execute(dbquerry.get_user(auth.username)).fetchone()
    
