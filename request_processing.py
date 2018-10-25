ORDERS = [
    {
        'order_id': '1',
        'title': 'string',
        'weight': 'string',
        'dimensions': 'string',
        'state_code': '1',
        'state': 'awaiting delivery',
        'order_type': 'tbd',
        'warehouse_address': 'string',
        'recipient_address': 'string',
        'warehouse_id': 'string',
        'warehouse_location': '55.753320;48.741012',
        'recipient_location': '55.817458;49.130425',
        'delivery_time_from': 'string in some datetime format',
        'delivery_time_to': 'string in some datetime format',
        'recipient_phone': 'string in some phone format',
        'recipient_name': 'string',
        'assigned_to': None,
    },
    {
        'order_id': '2',
        'title': 'string',
        'weight': 'string',
        'dimensions': 'string',
        'state_code': '1',
        'state': 'awaiting delivery',
        'order_type': 'tbd',
        'warehouse_address': 'string',
        'recipient_address': 'string',
        'warehouse_id': 'string',
        'warehouse_location': '55.753320;48.741012',
        'recipient_location': '55.817458;49.130425',
        'delivery_time_from': 'string in some datetime format',
        'delivery_time_to': 'string in some datetime format',
        'recipient_phone': 'string in some phone format',
        'recipient_name': 'string',
        'assigned_to': None,
    },
    {
        'order_id': '3',
        'title': 'string',
        'weight': 'string',
        'dimensions': 'string',
        'state_code': '1',
        'state': 'awaiting delivery',
        'order_type': 'tbd',
        'warehouse_address': 'string',
        'recipient_address': 'string',
        'warehouse_id': 'string',
        'warehouse_location': '55.753320;48.741012',
        'recipient_location': '55.817458;49.130425',
        'delivery_time_from': 'string in some datetime format',
        'delivery_time_to': 'string in some datetime format',
        'recipient_phone': 'string in some phone format',
        'recipient_name': 'string',
        'assigned_to': 'abc',
    },
    {
        'order_id': '4',
        'title': 'string',
        'weight': 'string',
        'dimensions': 'string',
        'state_code': '1',
        'state': 'awaiting delivery',
        'order_type': 'tbd',
        'warehouse_address': 'string',
        'recipient_address': 'string',
        'warehouse_id': 'string',
        'warehouse_location': '55.753320;48.741012',
        'recipient_location': '55.817458;49.130425',
        'delivery_time_from': 'string in some datetime format',
        'delivery_time_to': 'string in some datetime format',
        'recipient_phone': 'string in some phone format',
        'recipient_name': 'string',
        'assigned_to': 'abc',
    },
]


def _err_dict(label):
    return {'error': label}


def _are_valid_credentials(login, password_hash):
    """
    Ask data cluster if given authentication pair is correct
    and belongs to the correct user.
    :param login: Login of user that tries to log in
    :param password_hash: User password's hash
    :return: `True' - there is a user with given credentials
    """
    return login == 'abc' and password_hash == '123'  # TODO actual request


def _generate_token(login):
    return 'new_access_token'  # TODO


def _is_valid_token(token):
    return token == 'new_access_token'  # TODO


def _get_login_by_token(token):
    return 'abc'  # TODO


def try_login(data):
    """
    Try to login with given credentials or give an error response.
    :param data: Dictionary with `login` and `password_hash`
    :return: Dictionary with `token` of authenticated user or `error`
    """
    try:
        login = data['login']
        password_hash = data['password_hash']
    except KeyError:
        return _err_dict('Required field(s) missed')
    if _are_valid_credentials(login, password_hash):
        return {'token': _generate_token(login)}
    else:
        return _err_dict('Invalid authentication data')


def get_available_orders(header):
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not _is_valid_token(token):
        return _err_dict('Invalid token')
    return [el for el in ORDERS if not el['assigned_to']]  # TODO


def get_assigned_orders(header):
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not _is_valid_token(token):
        return _err_dict('Invalid token')
    login = _get_login_by_token(token)
    return [el for el in ORDERS if el['assigned_to'] == login]  # TODO


def get_order_details(header, data):
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not _is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        order_id = data['order_id']
    except KeyError:
        return _err_dict('Required field missed')
    try:  # TODO
        return next(
            el for el in ORDERS
            if el['order_id'] == order_id
        )
    except StopIteration:
        return _err_dict('Order with given ID does not exist')


def try_order_accept(header, data):
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not _is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        order_id = data['order_id']
    except KeyError:
        return _err_dict('Required field missed')
    i = 0  # TODO
    while i < len(ORDERS):
        if ORDERS[i]['order_id'] == order_id:
            ORDERS[i]['assigned_to'] = _get_login_by_token(token)
            break
    if i == len(ORDERS):
        return _err_dict('Order with given ID does not exist')
    return {}  # TODO


def try_order_pick(header, data):
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not _is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        order_id = data['order_id']
        key = data['key']
    except KeyError:
        return _err_dict('Required field(s) missed')
    if False:  # TODO
        return _err_dict('Order picking failed')
    return {}  # TODO


def try_validate_customer(header, data):
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not _is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        order_id = data['order_id']
    except KeyError:
        return _err_dict('Required field missed')
    if False:  # TODO
        return _err_dict('Customer validation failed')
    return {}  # TODO


def try_order_deliver(header, data):
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not _is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        order_id = data['order_id']
        key = data['key']
    except KeyError:
        return _err_dict('Required field(s) missed')
    if False:  # TODO
        return _err_dict('Order deliver try failed')
    return {}  # TODO


def try_order_cancel(header, data):
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not _is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        order_id = data['order_id']
    except KeyError:
        return _err_dict('Required field missed')
    if False:  # TODO
        return _err_dict('Order cancellation failed')
    return {}  # TODO


def try_location_update(header, data):
    try:
        token = header['token']
    except KeyError:
        return _err_dict('Token is missing')
    if not _is_valid_token(token):
        return _err_dict('Invalid token')
    try:
        location = data['location']
    except KeyError:
        return _err_dict('Required field missed')
    if False:  # TODO
        return _err_dict('Location update failed')
    return {}  # TODO
