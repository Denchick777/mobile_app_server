"""
Server application core, implementing request interface using Flask.
:author: Denis Chernikov
"""

from flask import Flask, jsonify, request

from local_config import configs
import local_db
import request_processing as rp

app = Flask(__name__)  # Initialize Flask application


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


@app.route('/plug_reset', methods=['POST'])
def plug_reset():  # TODO remove
    return jsonify(rp.plug_reset())


if __name__ == '__main__':
    # local_db.configure_db()
    app.run(host='0.0.0.0', port=configs['SERVER_PORT'])
