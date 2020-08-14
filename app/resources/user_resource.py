from flask_restx import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, jwt_refresh_token_required, create_refresh_token, get_jwt_identity, get_raw_jwt

from werkzeug.security import safe_str_cmp

from models.user import UserModel

from blacklist import BLACKLIST



class UserRegister(Resource):
    def post(self):
        """Create a new user"""
        data = User.parser.parse_args()

        if UserModel.find_by_name(data["username"]):
            return {"message" : "A user with that username already exists."}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message" : "User Created Successfully."}, 201


class UserLogin(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
    "username", type=str, required=True, help="This field cannot be left blank!"
    )   
    parser.add_argument(
    "password", type=str, required=True, help="This field cannot be left blank!"
    )

    def post(self):
        """Authenticate an existing user"""
        data = UserLogin.parser.parse_args()

        user = UserModel.find_by_name(data["username"])

        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {"message" : "Invalid Credentials"}, 401


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "email", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be left blank!"
    )
    def get(self, user_id:int):
        """Return a single user """
        user = UserModel.find_by_id(user_id)

        if user:
            return user.json(), 200
        return{"message" : "User does not exist!"}, 404

    def delete(self, user_id:int):
        """Delete an existing user"""
        user = UserModel.find_by_id(user_id)

        if user:
            user.delete_from_db()
            return{"message" : "User deleted successfully"}
        return{"message" : "User does not exist!"}, 404


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message" : "User <id{}> successfully logged out.".format(user_id)}, 200

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token" : new_token}, 200
