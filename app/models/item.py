from typing import Dict, List, Union

from db.config import db

ItemJSON = Dict[str, Union[int, str, float]]


class ItemModel(db.Model):
    __tablename__: "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float(precision=2), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, name: str, price: float, store_id: int):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self) -> ItemJSON:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id,
        }

    # save a new item to the db
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    # get a single item by id
    @classmethod
    def find_by_id(cls, id: int) -> "ItemModel":
        return cls.query.filter_by(id=id).first()

    # get by name
    @classmethod
    def find_by_name(cls, name: str) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    # get all items in the db
    @classmethod
    def find_all_items(cls) -> List:
        return cls.query.all()

    # delete an item from the db
    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
