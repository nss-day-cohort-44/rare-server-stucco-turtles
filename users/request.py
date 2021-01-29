import sqlite3
import json
from models import User



def get_all_users():

    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(""" 
        SELECT
            u.id,
            u.first_name,
            u.password,
            u.last_name,
            u.username,
            u.email,
            u.created_on,
            u.active,
            u.account_type_id
        FROM Users u
        """)

        users = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            user = User(row['id'],row['first_name'], row['password'], row['last_name'], row['username'], row['account_type_id'], row['email'], row['created_on'], row['active'])

            users.append(user.__dict__)

    return json.dumps(users)

def get_single_user(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory=sqlite3.Row
        db_cursor=conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.password,
            u.last_name,
            u.username,
            u.email,
            u.created_on,
            u.active,
            u.account_type_id
        FROM Users u
        WHERE u.id=?
        """, (id,))

        
        data=db_cursor.fetchone()

        
        user = User(data['id'], data['first_name'], data['password'], data['last_name'], data['username'], data['account_type_id'], data['email'], data['created_on'], data['active'])

    return json.dumps(user.__dict__)




def logged_user(log_user):
    get_users = json.loads(get_all_users())
    
    
    user_found = {}

    for user in get_users:
        if log_user['username'] == user['email'] and log_user['password'] == user['password']:
            user_found = (user)
            user_found['valid'] = True
            return json.dumps(user_found)

    user_found['valid'] = False
    return(json.dumps(user_found))






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


