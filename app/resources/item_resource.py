from flask_restx import Resource, reqparse
from flask_jwt_extended import fresh_jwt_required, jwt_required

from models.item import ItemModel

class Items(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "store_id", type=int, required=True, help="Eery Item needs a store_id!"
    )

    def get(self):
        "Return a list of all items"
        return {"items" : items = [item.json() for item in ItemModel.find_all_items()]}
        

    @fresh_jwt_required
    def post(self):
        """Add a new item to store"""
        data = Items.parser.parse_args()
        item = ItemModel(**data)

        if ItemModel.find_by_name(data["name"]):
            return ({"message" : "An Item with the name '{}' already exists.".format(data["name"])})

        try:
            item.save_to_db()
        except:
            return {"message" : "An error occured while inserting the item."}, 500

        return item.json(), 201
    

class Item(Resource):
    @jwt_required
    def get(self, id:int):
        """Return a single item"""
        item = ItemModel.find_by_id(id)

        if item:
            return item.json(), 200
        return {"message": "Item not found "}, 404

    @jwt_required
    def delete(self, id:int):
        """Delete an item that matches the id"""
        item = ItemModel.find_by_id(id)

        if item:
            item.delete_from_db()
            return {"message" : "Item deleted Successfully"}, 200
        return {"message" : "Item not found"}, 404


    def put(self, id:int):
        """Update an existing item or creates a new item"""
        data = Items.parser.parse_args()

        item = ItemModel.find_by_id(id)


        if item:
            item.name = data["name"]
            item.price = data["price"]
        else:
            item = ItemModel(**data)

        item.save_to_db()

        return item.json(), 200