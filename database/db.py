import psycopg2
from psycopg2 import DatabaseError
from decouple import config


def get_connection():
    try:
        return psycopg2.connect(
            host=config('PGSQL_HOST'),
            database=config('PGSQL_DATABASE'),
            user=config('PGSQL_USERNAME'),
            password=config('PGSQL_PASSWORD')
        )
    except DatabaseError as ex:
        raise ex
    