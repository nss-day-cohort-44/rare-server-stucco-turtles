import sqlite3
import json
from models import User

def create_user(new_user):

    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        INSERT INTO Users
            ( first_name, password, last_name, username, account_type_id, email, created_on)
        Values
            ( ?, ?, ?, ?, ?, ?, ?);
        """, (new_user['first_name'], new_user['password'], new_user['last_name'], new_user['username'],
              new_user['account_type_id'], new_user['email'], new_user['created_on'], ))

        
        
        id = db_cursor.lastrowid

        new_user['id'] = id
        new_user['valid'] = "valid"

    return json.dumps(new_user)