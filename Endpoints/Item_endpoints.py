from bson import ObjectId
from flask import Blueprint, request, jsonify
from Utils import Mongo


def define_endpoints(configuration):
    mongo_config = configuration['mongo']
    dal = Mongo.mongo_controller(mongo_config)
    items_endpoints = Blueprint("crud_api", __name__)

    @items_endpoints.route("/get_all", methods=["GET", "POST"])
    def get_all_items():
        results = dal.get_all()
        response = jsonify({"items": results})
        return response

    @items_endpoints.route("/get", methods=["GET", "POST"])
    def get():
        item_id = 0
        if request.method == "POST":
            item_id = request.form["item_id"]
        elif request.method == "GET":
            item_id = request.args.get('page', default=0, type=int)
        response = jsonify({"items": "aquí van los items"})
        return response

    @items_endpoints.route("/add", methods=["POST"])
    def add():
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock']
        new_item = {
            'name': name,
            'price': price,
            'stock': stock
        }
        dal.insert(new_item)
        response = jsonify({"status": "OK"})
        return response

    @items_endpoints.route("/update", methods=["POST"])
    def update():
        item_id = ObjectId(request.form['_id'])
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock']
        attrs_to_update = {
            'name': name,
            'price': price,
            'stock': stock
        }
        dal.update(item_id, attrs_to_update)
        response = jsonify({"status": "OK"})
        return response

    @items_endpoints.route("/delete", methods=["GET", "POST"])
    def delete():
        item_id = 0
        if request.method == "POST":
            item_id = ObjectId(request.form['_id'])
        elif request.method == "GET":
            item_id = ObjectId(request.args.get('page', default=0, type=str))
        dal.delete(item_id)
        response = jsonify({"status": "OK"})
        return response

    return items_endpoints