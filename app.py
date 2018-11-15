"""
Server application core, implementing request interface using Flask.
:author: Denis Chernikov
"""

from flask import Flask, jsonify, request

from local_config import configs
from local_db import configure_db
import request_processing as rp

app = Flask('mobile_server_app')


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
    return jsonify(rp.accept_order(request.headers, request.json))


@app.route('/order/pick', methods=['POST'])
def order_pick():
    return jsonify(rp.pick_order(request.headers, request.json))


@app.route('/order/validate_customer', methods=['POST'])
def order_validate_customer():
    return jsonify(rp.validate_customer(request.headers, request.json))


@app.route('/order/deliver', methods=['POST'])
def order_deliver():
    return jsonify(rp.deliver_order(request.headers, request.json))


@app.route('/order/cancel', methods=['POST'])
def order_cancel():
    return jsonify(rp.cancel_order(request.headers, request.json))


@app.route('/location/update', methods=['POST'])
def location_update():
    return jsonify(rp.update_location(request.headers, request.json))


@app.route('/support/call', methods=['POST'])
def call_support():
    return jsonify(rp.get_support_phone_number(request.headers))


@app.route('/logout', methods=['POST'])
def logout():
    return jsonify(rp.logout(request.headers))


if __name__ == '__main__':
    configure_db()
    app.run(host='0.0.0.0', port=configs['SERVER_PORT'])
