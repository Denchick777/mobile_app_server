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
    try:
        postgresql.open(
            'pq://{}:{}@localhost:5432/{}'.format(USER_NAME, USER_PASS, DB_NAME)
        )
    except postgresql.exceptions.ClientCannotConnectError:
        print('Database is unreachable! Trying to initialize it from scratch...')
        try:
            with postgresql.open(
                    'pq://{}:{}@localhost:5432'.format('postgres', POSTGRES_PASS)
            ) as db:
                db.execute(
                    'DROP USER IF EXISTS {0};'
                    "CREATE USER {0} WITH password '{1}';"
                    .format(USER_NAME, USER_PASS)
                )
                db.execute(
                    'DROP DATABASE IF EXISTS {0}'
                    .format(DB_NAME)
                )
                db.execute(
                    'CREATE DATABASE {0} WITH OWNER = {1};'
                    .format(DB_NAME, USER_NAME)
                )
        except postgresql.exceptions.ClientCannotConnectError:
            print(
                'Unable to create database!\n'
                'Check if PostgreSQL is running and configurations are correct\n'
                'Terminating application...'
            )
            exit(1)

    with postgresql.open(
            'pq://{}:{}@localhost:5432/{}'.format(USER_NAME, USER_PASS, DB_NAME)
    ) as db:
        db.execute(
            ''  # TODO schema
        )


def _generate_token(user_name):
    """
    For local use.
    Generate almost unique session token associated with given user name.
    NOTE: collision is very improbable, but still may occur.
    :param user_name: User name to be used for creation
    :return: String with almost unique token value
    """
    return f'new_access_token_for_{user_name}'  # TODO generate randomly


def store_user_auth(login, role_id):
    """
    Store authentication data for a new session and emmit new token for it.
    :param login: Login used for authentication
    :param role_id: `role_id` associated with given user
    :return: New token entry to be used within new session
    """
    token = _generate_token(login)
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


if __name__ == '__main__':
    configure_db()
