import psycopg2
import os


def get_connection():

    conn = psycopg2.connect(
        host=os.getenv("MNT_DATABASE_HOST"),
        port=os.getenv("MNT_DATABASE_PORT"),
        database=os.getenv("MNT_DATABASE_NAME"),
        user=os.getenv("MNT_DATABASE_USER"),
        password=os.getenv("MNT_DATABASE_PASSWORD")
    )

    return conn
