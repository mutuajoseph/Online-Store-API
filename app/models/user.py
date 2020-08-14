from db.config import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    stores = db.relationship("StoreModel", backref="stores", lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email= email
        self.password = password
    
    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "stores": [store.json() for store in self.stores]
        }

    # save to the db
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # find by name
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    # find by name
    @classmethod
    def find_by_name(cls, username):
        return cls.query.filter_by(username=username).first()

    # get all user
    @classmethod
    def find_all_users(cls):
        return cls.query.all()

    # delete from db
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
