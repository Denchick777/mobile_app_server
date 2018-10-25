from flask import Flask, jsonify, request

import request_processing as rp

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    return jsonify(rp.try_login(request.json))


@app.route('/available_orders', methods=['POST'])
def available_orders():
    return jsonify(rp.get_available_orders(request.headers))


@app.route('/assigned_orders', methods=['POST'])
def assigned_orders():
    return jsonify(rp.get_assigned_orders(request.headers))


@app.route('/order/details', methods=['POST'])
def order_details():
    return jsonify(rp.get_order_details(request.headers, request.json))


@app.route('/order/accept', methods=['POST'])
def order_accept():
    return jsonify(rp.try_order_accept(request.headers, request.json))


@app.route('/order/pick', methods=['POST'])
def order_pick():
    return jsonify(rp.try_order_pick(request.headers, request.json))


@app.route('/order/validate_customer', methods=['POST'])
def order_validate_customer():
    return jsonify(rp.try_validate_customer(request.headers, request.json))


@app.route('/order/deliver', methods=['POST'])
def order_deliver():
    return jsonify(rp.try_order_deliver(request.headers, request.json))


@app.route('/order/cancel', methods=['POST'])
def order_cancel():
    return jsonify(rp.try_order_cancel(request.headers, request.json))


@app.route('/location/update', methods=['POST'])
def location_update():
    return jsonify(rp.try_location_update(request.headers, request.json))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5321')
