import logging
import sys
import psycopg2
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
logger = logging.getLogger(__name__)

def init_logging():
    """
    Initializes logging with handlers.
    """
    formatter = logging.Formatter("%(asctime)s %(levelname)8s --- [%(threadName)-8s] [%(filename)s:%(lineno)d] %(funcName)s: %(message)s")

    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setFormatter(formatter)
    # make it log less serious messages to stdout
    info_handler.addFilter(lambda record: record.levelno < logging.WARNING)

    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.WARNING)

    logger.handlers = [info_handler, error_handler]
    logger.setLevel(logging.DEBUG)

def init_connection_pool():
    global connection_pool
    connection_pool = ThreadedConnectionPool(**db_params)

def init():
    init_logging()
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

