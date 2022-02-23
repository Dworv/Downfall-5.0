
import sqlite3
from tools.embed import create_error_embed

con = sqlite3.connect('C:/Dworv Stuff/Coding/lapsus/downfall/downfall.db', timeout = 1)
c = con.cursor()

class DBFail:
    def __init__(self, message):
        self.message = message
        self.embeds = create_error_embed(self.message)

# user stuff

class UserTrait:
    ID = 'user_id'
    EDITOR_LEVEL = 'editor_level'
    YOUTUBE = 'youtube'
    BIO = 'bio'

def new_user(user_id, editor_level, youtube, bio):
    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", [int(user_id), editor_level, youtube, bio])
        con.commit()
    except:
        return DBFail("Failed to create user.")

def modify_user(user_id, trait, entry):
    try:
        c.execute("UPDATE users SET ? = ? WHERE user_id = ?", [trait, entry, int(user_id)])  
        con.commit()
    except:
        return DBFail("Failed to modify user.")

def get_user(user_id, create_new = True):
    try:
        c.execute("SELECT * FROM users WHERE user_id = ?", [int(user_id)])
        user = c.fetchone()
    except:
        return DBFail("Failed to get user.")
    if user is not None or not create_new:
        return user
    try:
        new_user(user_id, 0, None, None)
    except:
        return DBFail("Failed to create new user after finding none.")
    c.execute("SELECT * FROM users WHERE user_id = ?", [int(user_id)])
    return c.fetchone()

def all_users():
    try:
        c.execute("SELECT * FROM users")
        return c.fetchall()
    except:
        return DBFail("Failed to get all users.")

def delete_user(user_id):
    try:
        c.execute("DELETE FROM users WHERE user_id = ?", [int(user_id)])
        con.commit()
    except:
        return DBFail("Failed to delete user.")

# application stuff

class ApplicationTrait:
    ID = 'application_id'
    STATUS = 'status'
    USER_ID = 'user_id'
    URL = 'url'
    PRERECS = 'prerecs'

def new_application(user_id, url, prerecs):
    try:
        c.execute("INSERT INTO applications (status, user_id, url, prerecs) VALUES (?, ?, ?, ?)", [-1, int(user_id), str(url), int(prerecs)])
        con.commit()
    except:
        return DBFail("Failed to create application.")
    try:
        c.execute("SELECT * FROM applications WHERE rowid = ?", [c.lastrowid])
        return c.fetchone()[0]
    except:
        return DBFail("Failed to get application ID.")

def modify_application(application_id, trait, entry):
    try:
        c.execute("UPDATE applications SET ? = ? WHERE application_id = ?", [trait, entry, application_id])  
        con.commit()
    except:
        return DBFail("Failed to modify application.")

def get_application(application_id):
    try:
        c.execute("SELECT * FROM applications WHERE application_id = ?", [application_id])
        return c.fetchone()
    except:
        return DBFail("Failed to get application.")

def all_applications():
    try:
        c.execute("SELECT * FROM applications")
        return c.fetchall()
    except:
        return DBFail("Failed to get all applications.")

def delete_application(application_id):
    try:
        c.execute("DELETE FROM applications WHERE application_id = ?", [application_id])
        con.commit()
    except:
        return DBFail("Failed to delete application.")