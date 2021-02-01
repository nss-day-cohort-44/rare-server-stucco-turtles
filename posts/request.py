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


# 




















# As a reader, I would like to see the content of a Post so I can read it.

# Given a user is viewing a list of Posts
# When they select a post to read
# Then they should be directed to a Post Detail page that shows the Post Details.

# Post Details include:

# Title
# Header image (if exists)
# Content
# Publication date (MM/DD/YYYY)
# Author's Display Name