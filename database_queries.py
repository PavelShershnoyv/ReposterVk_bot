import sqlite3


def execute_sql_query(sql_query):
    con = sqlite3.connect('Reposter_Database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql_query)
    result = cur.fetchall()
    con.commit()
    con.close()

    return result


def add_new_user(id_tg):
    sql_query = f'''
    INSERT INTO Users (id_tg)
    VALUES ('{id_tg}')
    '''
    execute_sql_query(sql_query)


def connect_vk_account(id_tg, id_vk, vk_token):
    sql_query = f'''
    UPDATE Users
    SET id_vk = '{id_vk}', vk_token = '{vk_token}', group_ids = NULL, user_ids = NULL, end_time = NULL
    WHERE id_tg = '{id_tg}'
    '''
    execute_sql_query(sql_query)


def disconnect_vk_account(id_tg):
    sql_query = f'''
    UPDATE Users
    SET id_vk = NULL, vk_token = NULL, group_ids = NULL, user_ids = NULL, end_time = NULL
    WHERE id_tg = '{id_tg}'
    '''
    execute_sql_query(sql_query)


def get_user_info(id_tg):
    sql_query = f'''
    SELECT *
    FROM Users
    WHERE id_tg = '{id_tg}'
    '''
    user_info = execute_sql_query(sql_query)[0]
    return user_info


def get_all_id_tg():
    sql_query = '''
    SELECT (id_tg)
    FROM Users
    '''
    all_id_tg = [value[0] for value in execute_sql_query(sql_query)]
    return all_id_tg


def set_end_time(id_tg, value):
    sql_query = f'''
    UPDATE Users
    SET end_time = '{value}'
    WHERE id_tg = '{id_tg}'
    '''
    execute_sql_query(sql_query)


def set_group_ids(id_tg, value):
    sql_query = f'''
    UPDATE Users
    SET group_ids = '{value}'
    WHERE id_tg = '{id_tg}'
    ''' if value is not None else f'''
    UPDATE Users
    SET group_ids = NULL
    WHERE id_tg = '{id_tg}'
    '''
    execute_sql_query(sql_query)


def set_status(id_tg, value):
    sql_query = f'''
    UPDATE Users
    SET status = '{value}'
    WHERE id_tg = '{id_tg}'
    '''
    execute_sql_query(sql_query)


def set_user_ids(id_tg, value):
    sql_query = f'''
    UPDATE Users
    SET user_ids = '{value}'
    WHERE id_tg = '{id_tg}'
    ''' if value is not None else f'''
    UPDATE Users
    SET user_ids = NULL
    WHERE id_tg = '{id_tg}'
    '''
    execute_sql_query(sql_query)
