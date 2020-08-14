from db.config import db

class ItemModel(db.Model):
    __tablename__ : "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id


    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id
        }

    # save a new item to the db
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # get a single item by id
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    # get by name
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    # get all items in the db
    @classmethod
    def find_all_items(cls):
        return cls.query.all()

    # delete an item from the db
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

