from flask_restx import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, get_jwt_claims, jwt_optional, fresh_jwt_required, jwt_required

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

    @jwt_optional
    def get(self):
        "Return a list of all items"
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all_items()]
        if user_id:
            return {"items" : items}, 200
        
        return(
            {
                "items":[item["name"] for item in items],
                "message": "More data available if you log in."
            }, 200
        )

    @fresh_jwt_required
    def post(self):
        """Add a new item to store"""
        data = Items.parser.parse_args()
        item = ItemModel(**data)

        if ItemModel.find_by_name(data["name"]):
            return (
                {"message" : "An Item with the name '{}' already exists.".format(data["name"])}
            )

        try:
            item.save_to_db()
        except:
            return {"message" : "An error occured while inserting the item."}, 500

        return item.json(), 201
    

class Item(Resource):
    @jwt_required
    def get(self, id):
        """Return a single item"""
        item = ItemModel.find_by_id(id)

        if item:
            return item.json(), 200
        return {"message": "Item not found "}, 404

    @jwt_required
    def delete(self, id):
        """Delete an item that matches the id"""
        item = ItemModel.find_by_id(id)

        if item:
            item.delete_from_db()
            return {"message" : "Item deleted Successfully"}, 200
        return {"message" : "Item not found"}, 404


    def put(self, id):
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