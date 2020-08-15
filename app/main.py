from flask import Flask, jsonify
from flask_restx import Api
from flask_jwt_extended import JWTManager

from db.config import db
from resources.item_resource import Item, Items
from resources.store_resource import Store, Stores
from resources.user_resource import (
    User,
    UserRegister,
    UserLogin,
    UserLogout,
    TokenRefresh,
)

app = Flask(__name__)

db.init_app(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]
app.secret_key = "secret_key"

api = Api(
    app, title="Items Store API", description="A simple Item Store API", version="1.0"
)

# create tables
@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)

# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return (
        decrypted_token["jti"] in BLACKLIST
    )  # Here we blacklist particular JWTs that have been created in the past.


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(Item, "/item/<int:id>")
api.add_resource(Items, "/item")
api.add_resource(Store, "/store/<int:id>")
api.add_resource(Stores, "/store")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")


if __name__ == "__main__":
    app.run()
