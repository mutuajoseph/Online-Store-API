from db.config import db

class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    items = db.relationship("ItemModel", backref="items", lazy=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel")

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "items": [item.json() for item in self.items],
            "user_id": self.user_id
        }
    
    # save a store to db
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # find a single store
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    # find by name
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    # find all stores
    @classmethod
    def find_all_stores(cls):
        return cls.query.all()

    # delete from db
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()