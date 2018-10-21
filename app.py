from flask import Flask, jsonify, request

app = Flask(__name__)

ORDERS = [
    {
        'order_id': '1',
        'order_type': '1',
        'title': 'Parcel 1',
        'destination': '127.0,127.0,127.0',
        'address': 'Universitetskaya 777, d.5, kv.42',
        'description': 'Regular Letter',
        'weight': '0.1kg',
        'dimensions': '9x12x0.1cm',
        'distance_from_warehouse': '10km',
        'status': '0',
        'delivery_state': 'Waiting for Delivery',
        'customer_name': 'Ivan Ivanov',
        'customer_phone': '+7(999)0001122',
        'assigned_to': '-',
        'delivery_time_from': '12/10/18 14:00',
        'delivery_time_to': '12/10/18 17:00',
    },
    {
        'order_id': '2',
        'order_type': '2',
        'title': 'Parcel 2',
        'destination': '127.0,127.0,127.0',
        'address': 'Universitetskaya 676, d.7, kv.42',
        'description': 'Document Letter',
        'weight': '2.4kg',
        'dimensions': '15x20x0.1cm',
        'distance_from_warehouse': '15km',
        'status': '0',
        'delivery_state': 'Waiting for Delivery',
        'customer_name': 'Ivan Ivanov',
        'customer_phone': '+7(999)0001122',
        'assigned_to': '-',
        'delivery_time_from': '12/10/18 14:00',
        'delivery_time_to': '12/10/18 17:00',
    },
    {
        'order_id': '3',
        'order_type': '3',
        'title': 'Parcel 3',
        'destination': '127.0,127.0,127.0',
        'address': 'Kvantovy Bulvar 333, d.99, kv.42',
        'description': 'Small Parcel',
        'weight': '2.4kg',
        'dimensions': '15x20x0.1cm',
        'distance_from_warehouse': '15km',
        'status': '0',
        'delivery_state': 'Waiting for Delivery',
        'customer_name': 'Ivan Ivanov',
        'customer_phone': '+7(999)0001122',
        'assigned_to': 'abc',
        'delivery_time_from': '12/10/18 14:00',
        'delivery_time_to': '12/10/18 17:00',
    },
    {
        'order_id': '4',
        'order_type': '4',
        'title': 'Parcel 4',
        'destination': '127.0,127.0,127.0',
        'address': 'Universitetskaya 676, d.7, kv.42',
        'description': 'Document Letter',
        'weight': '2.4kg',
        'dimensions': '15x20x0.1cm',
        'distance_from_warehouse': '15km',
        'status': '0',
        'delivery_state': 'Waiting for Delivery',
        'customer_name': 'Ivan Ivanov',
        'customer_phone': '+7(999)0001122',
        'assigned_to': 'abc',
        'delivery_time_from': '12/10/18 14:00',
        'delivery_time_to': '12/10/18 17:00',
    },
]

ASSIGNED_ORDERS = {
    'abc': ['1', '2'],
}


def are_valid_credentials(login, password):
    return login == 'abc' and password == '123'


@app.route('/login', methods=['POST'])
def login():
    if are_valid_credentials(request.json['login'], request.json['password']):
        return jsonify({'token': 'test_token_successful'})
    else:
        return jsonify({'error': 'Invalid auth data'})


@app.route('/available_orders', methods=['POST'])
def available_orders():
    if request.headers['token'] == 'test_token_successful':
        return jsonify([el for el in ORDERS if el['assigned_to'] == '-'])
    else:
        return jsonify({'error': 'Invalid token'})


@app.route('/assigned_orders', methods=['POST'])
def assigned_orders():
    if request.headers['token'] == 'test_token_successful':
        try:
            return jsonify([
                el for el in ORDERS
                if el['order_id'] in ASSIGNED_ORDERS[request.json['login']]
            ])
        except KeyError:
            return jsonify([])
    else:
        return jsonify({'error': 'Invalid token'})


@app.route('/order/order_details', methods=['POST'])
def order_details():
    if request.headers['token'] == 'test_token_successful':
        try:
            return jsonify(next(
                el for el in ORDERS
                if el['order_id'] == request.json['order_id'])
            )
        except StopIteration:
            return jsonify({'error': 'Order does not exist'})
    else:
        return jsonify({'error': 'Invalid token'})


@app.route('/order/accept_order', methods=['POST'])
def accept_order():
    return jsonify({'error': 'Not implemented yet'})  # TODO


@app.route('/order/dismiss_order', methods=['POST'])
def dismiss_order():
    return jsonify({'error': 'Not implemented yet'})  # TODO


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5321')
