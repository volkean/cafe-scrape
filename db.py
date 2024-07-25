from log import logger
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor

# Database connection parameters
db_params = {
    'user': 'user',
    'password': 'user',
    'host': 'localhost',
    'port': '5432',
    'database': 'user',
    'minconn':1,
    'maxconn':10
}

connection_pool = None


def init_connection_pool():
    global connection_pool
    connection_pool = ThreadedConnectionPool(**db_params)


def init():
    init_connection_pool()


def get_db_connection():
    global connection_pool
    conn = connection_pool.getconn()
    conn.autocommit = True
    return conn


def put_db_connection(conn):
    global connection_pool
    if conn is not None:
        connection_pool.putconn(conn)


def get_cafes():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute('SELECT id,url,name,address,phone FROM cafe ORDER BY update_time DESC')
            cafes = cursor.fetchall()
            return cafes
    except Exception as ex:
        logger.exception(ex)
        raise Exception("Database error occurred. See logs for detail.")
    finally:
        put_db_connection(conn)


def insert_cafe(domain, url, name, address, phone):
    conn = None
    try:
        conn = get_db_connection()

        insert_query = """
        INSERT INTO cafe (domain, url, name, address, phone, update_time)
        VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT(url) 
        DO UPDATE SET
        name = EXCLUDED.name,
        address = EXCLUDED.address,
        phone = EXCLUDED.phone;
        """
        
        # Data to be inserted
        data_to_insert = (domain, url, name, address, phone)
        
        # Execute the INSERT statement
        with conn.cursor() as cursor:
            cursor.execute(insert_query, data_to_insert)
    except Exception as ex:
        logger.exception(ex)
        raise Exception("Database error occurred. See logs for detail.")
    finally:
        put_db_connection(conn)

