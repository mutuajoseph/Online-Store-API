from flask_restx import Resource, reqparse
from flask_jwt_extended import fresh_jwt_required, jwt_required

from models.item import ItemModel

ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted Successfully."
ERROR_INSERTING = "An error occured while inserting the item."
NAME_ALREADY_EXISTS = "An Item with the name '{}' already exists."
BLANK_ERROR = "'{}' cannot be left blank!"
RELATION_ERROR ="Every Item needs a store_id!"

class Items(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help=BLANK_ERROR.format("name")
    )
    parser.add_argument(
        "price", type=float, required=True, help=BLANK_ERROR.format("price")
    )
    parser.add_argument(
        "store_id", type=int, required=True, help=RELATION_ERROR
    )

    @classmethod
    def get(cls):
        "Return a list of all items"
        return {"items": [item.json() for item in ItemModel.find_all_items()]}

    @classmethod
    @fresh_jwt_required
    def post(cls):
        """Add a new item to store"""
        data = Items.parser.parse_args()
        item = ItemModel(**data)

        if ItemModel.find_by_name(data["name"]):
            return {
                "message": NAME_ALREADY_EXISTS.format(
                    data["name"]
                )
            }

        try:
            item.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return item.json(), 201


class Item(Resource):
    @classmethod
    @jwt_required
    def get(cls, id: int):
        """Return a single item"""
        item = ItemModel.find_by_id(id)

        if item:
            return item.json(), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    @jwt_required
    def delete(cls, id: int):
        """Delete an item that matches the id"""
        item = ItemModel.find_by_id(id)

        if item:
            item.delete_from_db()
            return {"message": ITEM_DELETED}, 200
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    def put(cls, id: int):
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
