from flask_restx import Resource, reqparse

from models.store import StoreModel

class Stores(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "user_id", type=int, required=True, help="Every Store needs a user_id!"
    )

    def get(self):
        """Return a list of all stores"""
        return {"stores": [x.json() for x in StoreModel.find_all_stores()]}

    def post(self):
        """Create a new store """
        data = Stores.parser.parse_args()

        if StoreModel.find_by_name(data["name"]):
            return (
                {"message" : "A store with the name '{}' already exists.".format(data["name"])}
            )

        store = StoreModel(**data)

        try:
            store.save_to_db()
        except:
            return {"message" : "An error occurred while creating the store."}, 500
        return store.json(), 201

   

class Store(Resource):
    def get(self, id):
        """Return a single store"""
        store = StoreModel.find_by_id(id)

        if store:
            return store.json(), 200
        return {"message" : "Store does not exist."}, 404

    def delete(self, id):
        """Delete an existing store"""
        store = StoreModel.find_by_id(id)

        if store:
            store.delete_from_db()
            return {"message" : "Store deleted successfully."}, 200
        return {"message" : "Store does not exist."}, 404
