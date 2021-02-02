import sqlite3
import json
from models import Comment


def create_comment(new_comment):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Comments
            ( post_id, author_id, content, subject)
        VALUES
            ( ?, ?, ?, ?);
        """, (new_comment['post_id'], 
                new_comment['author_id'],
                new_comment['content'],
                new_comment['subject'],
              ))

        id = db_cursor.lastrowid

        new_comment['id'] = id

    return json.dumps(new_comment)


def get_comments():
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
         SELECT c.id,
                c.post_id,
                c.author_id,
                c.content,
                c.subject
        FROM Comments AS c
         """)

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            comment = Comment(row['id'],row['post_id'],row['author_id'],row['content'],row['subject'])

            comments.append(comment.__dict__)
        
        return json.dumps(comments)

