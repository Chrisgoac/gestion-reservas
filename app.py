from flask import Flask, send_from_directory, request
from blocklist import BLOCKLIST
from flask_smorest import Api
import models
import os 
from flask_jwt_extended import JWTManager
from database import db
from flask_migrate import Migrate
from controllers.user_controller import blp as UserBlueprint
from dotenv import load_dotenv

app: Flask = Flask(__name__, static_folder="dist", static_url_path="/")

load_dotenv()

app.config["API_TITLE"] = os.getenv("API_TITLE")
app.config["API_VERSION"] = os.getenv("API_VERSION")
app.config["OPENAPI_VERSION"] = os.getenv("OPENAPI_VERSION")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)

db.init_app(app)

Migrate(app, db)

api: Api = Api(app)

api.register_blueprint(UserBlueprint)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return {"message": "The token has been revoked.", "error": "token_revoked"}, 401

@app.route("/")
def serve():
    """serves React App"""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def static_proxy(path):
    """static folder serve"""
    file_name = path.split("/")[-1]
    dir_name = os.path.join(app.static_folder, "/".join(path.split("/")[:-1]))
    return send_from_directory(dir_name, file_name)

@app.errorhandler(404)
def handle_404(e):
    if request.path.startswith("/api/"):
        # Check if there's a custom message in the response data
        message = getattr(e, "data", {}).get("message", None)
        if message:
            return {"message": message, "status": "Not found", "code": 404}, 404
        else:
            return {"message": "Resource not found"}, 404
    return send_from_directory(app.static_folder, "index.html")

@app.errorhandler(405)
def handle_405(e):
    if request.path.startswith("/api/"):
        return {"message": "Method not allowed"}, 405
    return e