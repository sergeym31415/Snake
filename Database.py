import sqlite3


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query, name, result):
    cursor = connection.cursor()
    try:
        cursor.execute(query, (name, result))
        connection.commit()
        print("Query executed successfully")
    except sqlite3.Error as e:
        print(f"The error in execute_query '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print('execute_read_query success')
        return result
    except sqlite3.Error as e:
        print(f"The error in execute_read_query '{e}' occurred")

def read_user_stat(conn, name):
    query = f"""
    SELECT
     besttime
    FROM Records
    WHERE 
        name LIKE "{name}"
    """
    user_stats = execute_read_query(conn, query)
    if len(user_stats) > 0:
        return user_stats[0]
    else:
        return None


def write_game_stat(connection, username, result):
    readed_info = read_user_stat(connection, username)[0]
    if readed_info == None:
        query = f"""
                        INSERT INTO
                            Records
                        (name,besttime)
                        VALUES(?,?);
                        """
        execute_query(connection, query, username, result)
    else:
        if result < readed_info or readed_info == 0:
            query = f"""
                UPDATE
                    Records
                SET besttime=?
                WHERE name=?;
                """
            execute_query(connection, query, username, result)
