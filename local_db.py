"""
Local database interface for server application.
:author: Denis Chernikov
"""

import postgresql

from local_config import configs

POSTGRES_PASS = configs['POSTGRES_PASS']
DB_NAME = configs['DB_NAME']
USER_NAME = configs['USER_NAME']
USER_PASS = configs['USER_PASS']

TEMP_DB = {}  # TODO remove


def configure_db():
    """
    Initialize server's PostgreSQL database from the scratch using configuration data.
    """
    with postgresql.open('pq://{}:{}@localhost:5432'.format(
            'postgres', 'postgres')) as db:
        db.execute(  # 'DROP DATABASE IF EXISTS {0};'
                   'CREATE DATABASE {0};'
                   "CREATE USER {1} WITH password '{2}';"
                   'GRANT ALL ON DATABASE {0} TO {1};'
                   .format(DB_NAME, USER_NAME, USER_PASS))

    with postgresql.open('pq://{}:{}@localhost:5432/{}'.format(
            USER_NAME, USER_PASS, DB_NAME)) as db:
        pass  # TODO schema creation


def store_user_auth(login, role_id):
    """
    Store authentication data for a new session and emmit new token for it.
    :param login: Login used for authentication
    :param role_id: `role_id` associated with given user
    :return: New token entry to be used within new session
    """
    token = f'new_access_token_for_{login}'  # TODO generate randomly
    TEMP_DB[token] = {}
    TEMP_DB[token]['login'] = login
    TEMP_DB[token]['role_id'] = role_id
    # TODO TTL
    return token


def is_valid_token(token):
    """
    Is given token - valid one?
    :param token: Token to check validity of
    :return: `true` - it is valid and up-to-date, `false` - otherwise
    """
    # TODO TTL
    return token in TEMP_DB.keys()


def get_login_by_token(token):
    """
    Get `login` associated with a given session token.
    :param token: Token to search user by
    :return: `login` associated with a given token
    """
    return TEMP_DB[token]['login']
