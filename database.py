import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="MEDITECH_PLANIFAM",
        user="postgres",
        password="isaac",
        cursor_factory=RealDictCursor
    )