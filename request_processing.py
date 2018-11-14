"""
Request bodies for server application.
:author: Denis Chernikov
"""

import data_cluster_queries as dc
from data_cluster_queries import DataClusterQueryFailure
import local_db as ldb

# IDs of roles in data cluster
# 7 - truckDriver
# 8 - deliveryOperator
ALLOWED_ROLES = [7, 8]


def _err_dict(label):
    """
    Construct a dictionary with an error message.
    :param label: Label to assign as error message
    :return: Dictionary with single field called `error`
    """
    return {'error': label}


def try_login(data):
    """
    Try to login with given credentials or give an error response.
    :param data: Dictionary with `login` and `password_hash` fields
    :return: Dictionary with `token` of authenticated user or `error`
    """
    try:
        login = data['login']
        password_hash = data['password_hash']
    except KeyError:
        return _err_dict('Required field(s) missed')
    try:
        role_id = dc.try_authorize(login, password_hash)
    except DataClusterQueryFailure as e:
        return _err_dict(str(e))
    if role_id and role_id in ALLOWED_ROLES:
        token = ldb.store_user_auth(login, role_id)
    else:
        return _err_dict('Invalid authentication data')
    return {'token': token}


def get_available_orders(header):
    """
    Get a list of all unassigned orders.
    :param header: Dictionary with `token` field
    :return: List of dictionaries of all unassigned orders (reduced order info) or `error`
    """
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not ldb.is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        orders = dc.get_available_orders()
    except DataClusterQueryFailure as e:
        return _err_dict(str(e))
    return orders


def get_assigned_orders(header):
    """
    Get a list of all orders assigned to the specified user.
    :param header: Dictionary with `token` field
    :return: List of dictionaries of all orders of a given user (reduced order info) or `error`
    """
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not ldb.is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        login = ldb.get_login_by_token(token)
    except ldb.LocalDBQueryFailure as e:
        return _err_dict(str(e))
    try:
        orders = dc.get_assigned_orders(login)
    except DataClusterQueryFailure as e:
        return _err_dict(str(e))
    return orders


def get_order_details(header, data):
    """
    Get all the details about the specified order.
    :param header: Dictionary with `token` field
    :param data: Dictionary with `order_id` field
    :return: Dictionary with full info about the given order or `error`
    """
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not ldb.is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        order_id = data['order_id']
    except KeyError:
        return _err_dict('Required field missed')
    try:
        order = dc.get_order_details(order_id)
    except DataClusterQueryFailure as e:
        return _err_dict(str(e))
    return order


def accept_order(header, data):
    """
    Set the state of a given order as accepted to the given user.
    :param header: Dictionary with `token` field
    :param data: Dictionary with `order_id` field
    :return: Empty dictionary in case of success or dictionary with `error` field otherwise
    """
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not ldb.is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        order_id = data['order_id']
    except KeyError:
        return _err_dict('Required field missed')
    login = ldb.get_login_by_token(token)
    try:
        dc.try_order_accept(login, order_id)
    except DataClusterQueryFailure as e:
        return _err_dict(str(e))
    return {}


def pick_order(header, data):
    """
    Set the state of a given order as picked using given validation key.
    :param header: Dictionary with `token` field
    :param data: Dictionary with `order_id` and `key` fields
    :return: Empty dictionary in case of success or dictionary with `error` field otherwise
    """
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not ldb.is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        order_id = data['order_id']
        key = data['key']
    except KeyError:
        return _err_dict('Required field(s) missed')
    try:
        dc.try_pick_order(order_id, key)
    except DataClusterQueryFailure as e:
        return _err_dict(str(e))
    return {}


def validate_customer(header, data):
    """
    Make request for customer validation key creation while trying to end delivery.
    :param header: Dictionary with `token` field
    :param data: Dictionary with `order_id` field
    :return: Empty dictionary in case of success or dictionary with `error` field otherwise
    """
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not ldb.is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        order_id = data['order_id']
    except KeyError:
        return _err_dict('Required field missed')
    try:
        dc.try_validate_customer(order_id)
    except DataClusterQueryFailure as e:
        return _err_dict(str(e))
    return {}


def deliver_order(header, data):
    """
    Set the state of a given order as delivered using given validation key.
    :param header: Dictionary with `token` field
    :param data: Dictionary with `order_id` and `key` fields
    :return: Empty dictionary in case of success or dictionary with `error` field otherwise
    """
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not ldb.is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        order_id = data['order_id']
        key = data['key']
    except KeyError:
        return _err_dict('Required field(s) missed')
    try:
        dc.try_deliver_order(order_id, key)
    except DataClusterQueryFailure as e:
        return _err_dict(str(e))
    return {}


def cancel_order(header, data):
    """
    Set the state of a given order as cancelled.
    :param header: Dictionary with `token` field
    :param data: Dictionary with `order_id` field
    :return: Empty dictionary in case of success or dictionary with `error` field otherwise
    """
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not ldb.is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        order_id = data['order_id']
    except KeyError:
        return _err_dict('Required field missed')
    try:
        dc.try_cancel_order(order_id)
    except DataClusterQueryFailure as e:
        return _err_dict(str(e))
    return {}


def update_location(header, data):
    """
    Update geographical coordinates of a given user for the whole system.
    :param header: Dictionary with `token` field
    :param data: Dictionary with `location` field
    :return: Empty dictionary in case of success or dictionary with `error` field otherwise
    """
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not ldb.is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        location = data['location']
    except KeyError:
        return _err_dict('Required field missed')
    login = ldb.get_login_by_token(token)
    try:
        dc.try_update_location(login, location)
    except DataClusterQueryFailure as e:
        return _err_dict(str(e))
    return {}


def get_support_phone_number(header):
    """
    Get support service's phone number.
    :param header: Dictionary with `token` field
    :return: Dictionary with `number` field containing support service's phone number or `error`
    """
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not ldb.is_valid_token(token):
        return _err_dict('Invalid token')
    return {'number': '+7 (800) 555-35-35'}  # TODO actual data


def logout(header):
    """
    Close the session associated with a given token.
    :param header: Dictionary with `token` field
    :return: Empty dictionary in case of success or dictionary with `error` field otherwise
    """
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not ldb.is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        ldb.remove_token(token)
    except ldb.LocalDBQueryFailure as e:
        return _err_dict(e)
    return {}


def plug_reset():  # TODO remove
    """
    DEBUG FEATURE.
    Reset some fields for testing purposes.
    :return: Empty dictionary in case of success or dictionary with `error` field otherwise
    """
    try:
        return dc.plug_reset()
    except DataClusterQueryFailure as e:
        return _err_dict(str(e))
