"""
Data cluster queries interface for server application.
:author: Denis Chernikov
"""

import json
import requests

from local_config import configs

CLUSTER_ADDRESS = configs['CLUSTER_ADDRESS']

ORDERS = [  # TODO remove (created for setting up purposes)
    {
        'order_id': '1',
        'title': 'Big parcel #581',
        'weight': '1.977 kg',
        'dimensions': '0.25×0.40×0.1',
        'state_code': '0',
        'state': 'awaiting delivery',
        'order_type': '2',
        'warehouse_address': 'Kazan, Tatarstan str., 137, room 115',
        'warehouse_id': '0',
        'recipient_address': 'Innopolis, Universitetskaya str., 1k2, ap. 213',
        'warehouse_location': '55.753320;48.741012',
        'recipient_location': '55.817458;49.130425',
        'delivery_time_from': '29/11/2018 14:00:00',
        'delivery_time_to': '29/11/2018 16:00:00',
        'recipient_phone': '+7 (917) 923-43-84',
        'recipient_name': 'Denis Chernikov',
        'assigned_to': None,
        'pick_key': '31337',
        'validate_key': None,
    },
    {
        'order_id': '2',
        'title': 'Letter #17',
        'weight': '0.456 kg',
        'dimensions': '0.32×0.23×0.03',
        'state_code': '0',
        'state': 'awaiting delivery',
        'order_type': '0',
        'warehouse_address': 'Kazan, Tatarstan str., 137, room 115',
        'warehouse_id': '0',
        'recipient_address': 'Innopolis, Universitetskaya str., 1, room 424',
        'warehouse_location': '55.753320;48.741012',
        'recipient_location': '55.817458;49.130425',
        'delivery_time_from': '30/11/2018 10:00:00',
        'delivery_time_to': '30/11/2018 17:00:00',
        'recipient_phone': '+7 (843) 203-92-53',
        'recipient_name': 'Sergey Masyagin',
        'assigned_to': None,
        'pick_key': '31337',
        'validate_key': None,
    },
    {
        'order_id': '3',
        'title': 'Small parcel #318',
        'weight': '1.381 kg',
        'dimensions': '0.6×0.5×0.3',
        'state_code': '1',
        'state': 'assigned to delivery operator',
        'order_type': '1',
        'warehouse_address': 'Kazan, Tatarstan str., 137, room 115',
        'warehouse_id': '0',
        'recipient_address': 'Innopolis, Universitetskaya str., 1k4, ap. 404',
        'warehouse_location': '55.753320;48.741012',
        'recipient_location': '55.817458;49.130425',
        'delivery_time_from': '29/10/2018 18:00:00',
        'delivery_time_to': '29/10/2018 20:30:00',
        'recipient_phone': '+7 (999) 437-18-11',
        'recipient_name': 'Ivan Petrov',
        'assigned_to': 'abc',
        'pick_key': '31337',
        'validate_key': None,
    },
    {
        'order_id': '4',
        'title': 'Pallet #114',
        'weight': '0.418 kg',
        'dimensions': '2×1.65×2.1',
        'state_code': '0',
        'state': 'picked by delivery operator',
        'order_type': '3',
        'warehouse_address': 'Kazan, Tatarstan str., 137, room 115',
        'warehouse_id': '0',
        'recipient_address': 'Innopolis, Universitetskaya str., 1',
        'warehouse_location': '55.753320;48.741012',
        'recipient_location': '55.817458;49.130425',
        'delivery_time_from': '08/11/2018 10:30:00',
        'delivery_time_to': '08/11/2018 15:45:00',
        'recipient_phone': '+7 (961) 044-86-18',
        'recipient_name': 'Boris Vasilenko',
        'assigned_to': None,
        'pick_key': '31337',
        'validate_key': None,
    },
]


class DataClusterQueryFailure(Exception):
    """
    Exception for cases of failed data cluster query try.
    """
    def __init__(self, message):
        """
        Initialize data cluster query failure exception with given content.
        :param message: Message to store in this exception
        """
        super(DataClusterQueryFailure, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


def _ask_data_cluster(query_name, data):
    """
    For local use.
    Execute query to the data cluster using given query type and data.
    :param query_name: Query to be used for request to the data cluster (like `login` etc.)
    :param data: Dictionary with data to be sent as JSON inside this query
    :return: Response of the server
    :raises DataClusterQueryFailure: Data cluster responded with an error code
    :raises DataClusterQueryFailure: Data cluster returned non-JSON response
    """
    data_json = json.dumps(data)
    headers = {'content-type': 'application/json'}
    res = requests.post(f'{CLUSTER_ADDRESS}/{query_name}', data=data_json, headers=headers)
    if not res.ok:
        raise DataClusterQueryFailure('Data cluster responded with an error code')
    try:
        return res.json()
    except json.decoder.JSONDecodeError:
        raise DataClusterQueryFailure('Data cluster returned non-JSON response')


def try_authorize(login, password_hash):
    """
    Ask data cluster if given authentication pair is correct and belongs to the correct user.
    :param login: Login of user that tries to log in
    :param password_hash: User password's hash
    :return: `true` - given credentials are correct, `false` - otherwise
    :raises DataClusterQueryFailure: User authorization failed
    :raises DataClusterQueryFailure: Data cluster responded with an error code
    :raises DataClusterQueryFailure: Data cluster returned non-JSON response
    """
    res = _ask_data_cluster('login', {
        'login': login,
        'password_hash': password_hash,
    })
    if res['error'] != 'none':
        raise DataClusterQueryFailure('User authorization failed')
    return res['access_right_id']


def get_available_orders(role_id):
    """
    Ask data cluster for not yet assigned orders according to the role of the user.
    :param role_id: User role's identifier
    :return: List of dictionaries of all unassigned orders (reduced order info)
    :raises DataClusterQueryFailure: Data cluster responded with an error code
    :raises DataClusterQueryFailure: Data cluster returned non-JSON response
    """
    return [el for el in ORDERS if not el['assigned_to'] and ((el['order_type'] == '3') ^ (role_id == 8))]  # TODO DC


def get_assigned_orders(login):
    """
    Ask data cluster for orders assigned to the given user.
    :param login: Login of user that asks for the info
    :return: List of dictionaries of all orders of a given user (reduced order info)
    :raises DataClusterQueryFailure: Data cluster responded with an error code
    :raises DataClusterQueryFailure: Data cluster returned non-JSON response
    """
    return [el for el in ORDERS if el['assigned_to'] == login]  # TODO DC


def get_order_details(order_id):
    """
    Ask data cluster for given orders' details.
    :param order_id: Order number to search detailed info about
    :return: Dictionary with full info about the given order
    :raises DataClusterQueryFailure: Data cluster responded with an error code
    :raises DataClusterQueryFailure: Data cluster returned non-JSON response
    :raises DataClusterQueryFailure: Order with given ID does not exist
    """
    try:  # TODO DC
        return next(
            el for el in ORDERS
            if el['order_id'] == order_id
        )
    except StopIteration:
        raise DataClusterQueryFailure('Order with given ID does not exist')


def try_order_accept(login, order_id):
    """
    Say to data cluster that specified order is accepted by the given user.
    :param login: Login of user that tries to accept an order
    :param order_id: Order number to try to accept
    :raises DataClusterQueryFailure: Data cluster responded with an error code
    :raises DataClusterQueryFailure: Data cluster returned non-JSON response
    :raises DataClusterQueryFailure: Given order is already accepted
    :raises DataClusterQueryFailure: Order with given ID does not exist
    """
    i = 0  # TODO DC
    while i < len(ORDERS):
        if ORDERS[i]['order_id'] == order_id:
            if ORDERS[i]['state_code'] != '0':
                raise DataClusterQueryFailure('Given order is already accepted')
            ORDERS[i]['assigned_to'] = login
            ORDERS[i]['state_code'] = '1'
            return
        i += 1
    raise DataClusterQueryFailure('Order with given ID does not exist')


def try_pick_order(order_id, key):
    """
    Ask data cluster if given order may be picked using given key.
    :param order_id: Order number to try to pick
    :param key: Approvement key for order pick
    :raises DataClusterQueryFailure: Data cluster responded with an error code
    :raises DataClusterQueryFailure: Data cluster returned non-JSON response
    :raises DataClusterQueryFailure: Order picking failed
    :raises DataClusterQueryFailure: Order with given ID does not exist
    """
    i = 0  # TODO DC
    while i < len(ORDERS):
        if ORDERS[i]['order_id'] == order_id:
            if ORDERS[i]['pick_key'] == key:
                ORDERS[i]['state_code'] = '2'
                return
            raise DataClusterQueryFailure('Order picking failed')
        i += 1
    raise DataClusterQueryFailure('Order with given ID does not exist')


def try_validate_customer(order_id):
    """
    Say to data cluster new validation code for order delivery.
    :param order_id: Order number to assign validation code to
    :raises DataClusterQueryFailure: Data cluster responded with an error code
    :raises DataClusterQueryFailure: Data cluster returned non-JSON response
    :raises DataClusterQueryFailure: Order with given ID does not exist
    """
    i = 0  # TODO DC
    while i < len(ORDERS):
        if ORDERS[i]['order_id'] == order_id:
            ORDERS[i]['validate_key'] = '31337'  # TODO random
            return
        i += 1
    raise DataClusterQueryFailure('Order with given ID does not exist')


def try_deliver_order(order_id, key):
    """
    Ask data cluster if given order may be delivered using given key.
    :param order_id: Order number to try to deliver
    :param key: Approvement key for order delivery
    :raises DataClusterQueryFailure: Data cluster responded with an error code
    :raises DataClusterQueryFailure: Data cluster returned non-JSON response
    :raises DataClusterQueryFailure: Order delivery failed
    :raises DataClusterQueryFailure: Order with given ID does not exist
    """
    i = 0  # TODO DC
    while i < len(ORDERS):
        if ORDERS[i]['order_id'] == order_id:
            if ORDERS[i]['validate_key'] == key:
                ORDERS[i]['state_code'] = '3'
                return
            raise DataClusterQueryFailure('Order delivery failed')
        i += 1
    raise DataClusterQueryFailure('Order with given ID does not exist')


def try_cancel_order(order_id):
    """
    Say to data cluster that the specified order needs to be declined from the assigned employee.
    :param order_id: Order number to decline
    :raises DataClusterQueryFailure: Data cluster responded with an error code
    :raises DataClusterQueryFailure: Data cluster returned non-JSON response
    :raises DataClusterQueryFailure: Order cancellation failed
    :raises DataClusterQueryFailure: Order with given ID does not exist
    """
    i = 0  # TODO DC
    while i < len(ORDERS):
        if ORDERS[i]['order_id'] == order_id:
            if ORDERS[i]['state_code'] == '1':
                ORDERS[i]['state_code'] = '0'
                ORDERS[i]['assigned_to'] = None
                return
            raise DataClusterQueryFailure('Order cancellation failed')
        i += 1
    raise DataClusterQueryFailure('Order with given ID does not exist')


def try_update_location(login, location):
    """
    Say to data cluster new geographical position of a given user.
    :param login: Login of user to update position of
    :param location: New geographical location of the given user
    :raises DataClusterQueryFailure: Data cluster responded with an error code
    :raises DataClusterQueryFailure: Data cluster returned non-JSON response
    :raises DataClusterQueryFailure: Location update failed
    """
    if False:  # TODO DC
        raise DataClusterQueryFailure('Location update failed')
