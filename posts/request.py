import sqlite3
import json
from models import Post

def get_all_posts():
    #open a connection to the database
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        #sql query for the post
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM posts p
        """)

        # Initialize an empty list to hold the all post representations
        posts = []
        # Convert rows of data into a python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            # Create an post instance from the current row
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'], row['image_url'], row['content'], row['approved'])
            # convert the post into the dictonery and append into the posts(all post)
            posts.append(post.__dict__)
    # Use `json` package to properly serialize list as JSON
    return json.dumps(posts)

def get_single_post(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM posts p
        WHERE p.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'], data['title'],
                    data['publication_date'], data['image_url'], data['content'], data['approved'])

    return json.dumps(post.__dict__)


def delete_post(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM posts
        WHERE id = ?
        """, (id, ))


def get_users_post(user_id):

    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
        p.id,
        p.user_id,
        p.category_id,
        p.title,
        p.publication_date,
        p.image_url,
        p.content,
        p.approved
        FROM posts p
        WHERE p.user_id = ?
        """, (user_id, ))

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                        row['publication_date'], row['image_url'], row['content'], row['approved'])

            posts.append(post.__dict__)
    return json.dumps(posts)


def delete_post(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM posts
        WHERE id = ?
        """, (id, ))


def create_post(new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, category_id, title, publication_date, image_url, content, approved )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?);
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'],
              new_post['image_url'], new_post['content'],
              new_post['approved'], ))

        id = db_cursor.lastrowid

        new_post['id'] = id

    return json.dumps(new_post)


def update_post(id, new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE posts 
            SET
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?
        WHERE id = ?
        """, (new_post['category_id'], new_post['title'], new_post['publication_date'],
              new_post['image_url'], new_post['content'], id))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

