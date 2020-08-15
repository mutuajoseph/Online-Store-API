from flask_restx import Resource, reqparse

from models.store import StoreModel

STORE_NOT_FOUND = "Store not found."
STORE_DELETED = "Store deleted Successfully."
ERROR_INSERTING = "An error occured while inserting the store."
NAME_ALREADY_EXISTS = "A store with the name '{}' already exists."
BLANK_ERROR = "'{}' cannot be left blank!"
RELATION_ERROR ="Every store needs a user_id!"

class Stores(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help=BLANK_ERROR
    )
    parser.add_argument(
        "user_id", type=int, required=True, help=RELATION_ERROR
    )

    @classmethod
    def get(cls):
        """Return a list of all stores"""
        return {"stores": [x.json() for x in StoreModel.find_all_stores()]}

    @classmethod
    def post(cls):
        """Create a new store """
        data = Stores.parser.parse_args()

        if StoreModel.find_by_name(data["name"]):
            return {
                "message": NAME_ALREADY_EXISTS.format(
                    data["name"]
                )
            }

        store = StoreModel(**data)

        try:
            store.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500
        return store.json(), 201


class Store(Resource):
    @classmethod
    def get(cls, id: int):
        """Return a single store"""
        store = StoreModel.find_by_id(id)

        if store:
            return store.json(), 200
        return {"message": STORE_NOT_FOUND}, 404

    @classmethod
    def delete(cls, id: int):
        """Delete an existing store"""
        store = StoreModel.find_by_id(id)

        if store:
            store.delete_from_db()
            return {"message": STORE_DELETED}, 200
        return {"message": STORE_NOT_FOUND}, 404
