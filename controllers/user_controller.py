from flask_jwt_extended import (
    create_access_token, 
    jwt_required, 
    get_jwt_identity, 
    get_jwt
)
from blocklist import BLOCKLIST
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from passlib.hash import pbkdf2_sha256
from flask.views import MethodView
from datetime import timedelta
from bleach import clean
from database import db
import schemas
import models
import os

blp = Blueprint("users", __name__, description="Users endpoint", url_prefix="/api/user")

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(schemas.UserSchema(only=("username", "password",)))
    def post(self, data):
        """
        API Endpoint to log in an user.

        :param data: User login data.
        :return: HTTP response with the login result. If login it's correct, return an access_token.
        """

        user = models.UserModel.query.filter(models.UserModel.username == clean(data["username"])).first()

        if user and pbkdf2_sha256.verify(clean(data["password"]), user.password):
            access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=6))
            return {"access_token": access_token}, 200

        abort(401, message="Invalid credentials.")

@blp.route("/validate-token")
class UserValidateToken(MethodView):  
    @jwt_required()
    def post(self):
        """
        API Endpoint to validate a token.

        :return: HTTP response with the validation result.
        """

        return {"message": "Token is valid."}, 200

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        """
        API Endpoint to log out an user.

        :return: HTTP response with the logout result.
        """
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(schemas.UserSchema(only=("password", "username")))

    def post(self, payload):
        """
        API Endpoint to register a new user.

        :param payload: User data from the json to register.
        :return: HTTP response with the registration result.
        """
        
        if models.UserModel.query.filter(models.UserModel.email == payload["username"]).first():
            abort(409, message="User with that username already exists.")

        try:
            user = models.UserModel(
                username=clean(payload["username"]),
                password=pbkdf2_sha256.hash(clean(payload["password"]))
            )

            db.session.add(user)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            abort(400, message=f"An integrity error has ocurred.")

        return {"message": "User created successfully."}, 201

@blp.route("/profile")
class UserProfile(MethodView):
    @jwt_required()
    def get(self):
        """
        API Endpoint to get an user profile.

        :return: HTTP response with the user profile.
        """

        user_by_jwt = get_jwt_identity()

        user = db.session.get(models.UserModel, user_by_jwt)

        if user is None:
            abort(404, message="User not found")

        return {"username": user.email, "created_at": user.created_at, "updated_at": user.updated_at}, 200
    