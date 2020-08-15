from flask_restx import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    jwt_refresh_token_required,
    create_refresh_token,
    get_jwt_identity,
    get_raw_jwt,
)

from werkzeug.security import safe_str_cmp

from models.user import UserModel

from blacklist import BLACKLIST

USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted Successfully."
ERROR_INSERTING = "An error occured while inserting the user."
NAME_ALREADY_EXISTS = "A user with the name '{}' already exists."
BLANK_ERROR = "'{}' cannot be left blank!"
CREATED_SUCCESSFULLY = "User Created Successfully."
INVALID_CREDENTIALS = "Invalid Credentials"
LOG_OUT = "User <id{user_id}> successfully logged out."

class UserRegister(Resource):
    @classmethod
    def post(cls):
        """Create a new user"""
        data = User.parser.parse_args()

        if UserModel.find_by_name(data["username"]):
            return {"message": NAME_ALREADY_EXISTS.format(data["username"])}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": CREATED_SUCCESSFULLY}, 201


class UserLogin(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help=BLANK_ERROR
    )
    parser.add_argument(
        "password", type=str, required=True, help=BLANK_ERROR
    )

    @classmethod
    def post(cls):
        """Authenticate an existing user"""
        data = UserLogin.parser.parse_args()

        user = UserModel.find_by_name(data["username"])

        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"message": INVALID_CREDENTIALS}, 401


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help=BLANK_ERROR
    )
    parser.add_argument(
        "email", type=str, required=True, help=BLANK_ERROR
    )
    parser.add_argument(
        "password", type=str, required=True, help=BLANK_ERROR
    )

    @classmethod
    def get(cls, user_id: int):
        """Return a single user """
        user = UserModel.find_by_id(user_id)

        if user:
            return user.json(), 200
        return {"message": USER_NOT_FOUND}, 404

    @classmethod
    def delete(cls, user_id: int):
        """Delete an existing user"""
        user = UserModel.find_by_id(user_id)

        if user:
            user.delete_from_db()
            return {"message": USER_DELETED}
        return {"message": USER_NOT_FOUND}, 404


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": LOG_OUT.format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
