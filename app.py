from flask import Flask, jsonify, request

app = Flask(__name__)


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
        return jsonify(
            {
                'order_id': '1',
                'title': 'Letter',
                'address': 'street 1',
                'weight': '1kg',
                'dimensions': '10x10x10cm',
                'distance_from_warehouse': '10km',
                'order_type': '1'
            },
            {
                'order_id': '2',
                'title': 'Letter',
                'address': 'street 2',
                'weight': '1kg',
                'dimensions': '11x11x11cm',
                'distance_from_warehouse': '15km',
                'order_type': '2'
            }
        )
    else:
        return jsonify({'error': 'Invalid token'})


@app.route('/order/order_details', methods=['POST'])
def order_details():
    if request.headers['token'] == 'test_token_successful':
        if request.json['order_id'] == '1':
            return jsonify({
                'order_id': '0',
                'order_type': '1',
                'destination': '127.0,127.0,127.0',
                'address': 'Universitetskaya 1, k.1, kv.111',
                'description': 'Leightweight letter',
                'dimensions': '10x15cm',
                'weight': '15kg',
                'delivery_state': 'Waiting Delivery',
                'customer_name': 'Ivan Ivanov',
                'customer_phone': '+7(999)0001122',
            })
        else:
            return jsonify({'error': 'Order does not exist'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
