from typing import Dict, List, Union
from db.config import db
from models.store import StoreJSON

UserJSON = Dict[str, Union[int, str, List[StoreJSON]]]


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    stores = db.relationship("StoreModel", backref="stores", lazy=True)

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

    def json(self) -> Dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "stores": [store.json() for store in self.stores],
        }

    # save to the db
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    # find by name
    @classmethod
    def find_by_id(cls, _id) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    # find by name
    @classmethod
    def find_by_name(cls, username) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    # get all user
    @classmethod
    def find_all_users(cls) -> List:
        return cls.query.all()

    # delete from db
    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
