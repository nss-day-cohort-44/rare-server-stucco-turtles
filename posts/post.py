import sqlite3
import json
from models import Post


def create_post(new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Post
            ( title, publication_date, image_url, content, approved, user_id, category_id )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?);
        """, (new_post['title'], new_post['publication_date'],
              new_post['image_url'], new_post['content'],
              new_post['approved'], new_post['user_id'], new_post['category_id'], ))

        id = db_cursor.lastrowid

        new_post['id'] = id

    return json.dumps(new_post)
