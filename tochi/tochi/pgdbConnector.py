import psycopg2
from psycopg2 import pool

db_pool = None


def inititalize_connection_pool(dbsettings, minconn=1, maxconn=5):
    global db_pool
    if db_pool is None:
        try:
            db_pool = psycopg2.pool.SimpleConnectionPool(
                minconn,
                maxconn,
                dbname=dbsettings["DB_NAME"],
                user=dbsettings["AD_USERNAME"],
                password=dbsettings["DB_PASSWORD"],
                host=dbsettings["DB_HOST"],
                port=dbsettings["DB_PORT"]
            )
            print("Database pool created!!")
        except psycopg2.Error as e:
            print(f'Error creating database pool: {e}') 

def shutdown_connection_pool():
    global db_pool
    if db_pool:
        db_pool.closeall()
        print("Database connection closed...")


def execute_sql_query(query, values):
    try:
        conn = db_pool.getconn()
        cursor = conn.cursor()
        cursor.execute(query, values)

        if query.strip().lower().startswith("select"):
            result = cursor.fetchall()
        else:
            conn.commit()
            result = {"message": "Query executed successfully."}

        cursor.close()
        return result

    except psycopg2.Error as e:
        return {"error": str(e)}

    finally:
        if conn:
            db_pool.putconn(conn)


def execute_sql_query2(query):
    conn = None
    
    try:
        conn = db_pool.getconn()

        cursor = conn.cursor()
        
        cursor.execute(query)

        if query.strip().lower().startswith("select"):
            result = cursor.fetchall()
        else:
            conn.commit()
            result = {"message": "Query executed successfully."}
        
        cursor.close() 
        return result
    
    except psycopg2.Error as e:
        return {"error": str(e)}
    
    finally:
        if conn:
            db_pool.putconn(conn)

