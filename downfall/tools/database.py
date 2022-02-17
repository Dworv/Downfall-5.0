
import sqlite3
from tools.embed import create_error_embed

con = sqlite3.connect('C:/Dworv Stuff/Coding/lapsus/downfall/downfall.db')
c = con.cursor()

class DBFail:
    def __init__(self, message):
        self.message = message
        self.embeds = create_error_embed(self.message)
    
    def __bool__(self):
        return False

# user stuff

class UserTrait:
    ID = 'user_id'
    EDITOR_LEVEL = 'editor_level'
    YOUTUBE = 'youtube'
    BIO = 'bio'

async def new_user(user_id, editor_level, youtube, bio):
    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (user_id, editor_level, youtube, bio))
        con.commit()
    except:
        return DBFail("Failed to create user.")

async def modify_user(user_id, trait, entry):
    try:
        c.execute("UPDATE users SET ? = ? WHERE user_id = ?", (trait, entry, user_id))  
        con.commit()
    except:
        return DBFail("Failed to modify user.")

async def get_user(user_id):
    try:
        c.execute("SELECT * FROM users WHERE user_id = ?", (user_id))
        return c.fetchone()
    except:
        return DBFail("Failed to get user.")

async def all_users():
    try:
        c.execute("SELECT * FROM users")
        return c.fetchall()
    except:
        return DBFail("Failed to get all users.")

async def delete_user(user_id):
    try:
        c.execute("DELETE FROM users WHERE user_id = ?", (user_id))
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

async def new_application(user_id, url, prerecs):
    try:
        c.execute("INSERT INTO applications (status, user_id, url, prerecs) VALUES (?, ?, ?, ?)", (-1, user_id, url, prerecs))
        con.commit()
    except:
        return DBFail("Failed to create application.")

async def modify_application(application_id, trait, entry):
    try:
        c.execute("UPDATE applications SET ? = ? WHERE application_id = ?", (trait, entry, application_id))  
        con.commit()
    except:
        return DBFail("Failed to modify application.")

async def get_application(application_id):
    try:
        c.execute("SELECT * FROM applications WHERE application_id = ?", (application_id))
        return c.fetchone()
    except:
        return DBFail("Failed to get application.")

async def all_applications():
    try:
        c.execute("SELECT * FROM applications")
        return c.fetchall()
    except:
        return DBFail("Failed to get all applications.")

async def delete_application(application_id):
    try:
        c.execute("DELETE FROM applications WHERE application_id = ?", (application_id))
        con.commit()
    except:
        return DBFail("Failed to delete application.")


