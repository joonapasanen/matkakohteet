import sqlite3
from flask import session
import db
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(username, password):
    password_hash = generate_password_hash(password)
    try:
        sql = "INSERT INTO Users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
        session["username"] = username
        session["user_id"] = db.last_insert_id()
    except sqlite3.IntegrityError:
        return False
    return True

def login_user(username, password):
    sql = "SELECT password_hash, user_id FROM Users WHERE username = ?"
    result = db.query(sql, [username])
    
    if not result:
        return None
    
    password_hash, user_id = result[0]
    
    if check_password_hash(password_hash, password):
        session["username"] = username
        session["user_id"] = user_id
        return True
    else:
        return False

def logout_user():
    if "username" in session:
        del session["username"]
    if "user_id" in session:
        del session["user_id"]
