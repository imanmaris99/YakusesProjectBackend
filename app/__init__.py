from flask import Flask, json, jsonify
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from app.utils.db import db, migrate

from app.models import user_model, business_category_model, business_model
from app.models import rating_model, user_need_model, article_model

from dotenv import load_dotenv

from app.controllers.user import user_route

from flask_cors import CORS
import os

# Initializing Flask application
app = Flask(__name__)
CORS(app)
load_dotenv()

# Setting database URI directly
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initializing database
db.init_app(app)
migrate.init_app(app, db)

# # Setting JWT secret key directly
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Swagger UI Configuration
SWAGGER_URL = '/docs'
API_URL = '/static/openapi.json'  # Ensure this URL is correct
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "YakusesBE-API"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Registering blueprints
app.register_blueprint(user_route.user_blueprint, url_prefix='/user')

# Defining routes here
@app.route('/')
def index():
    return jsonify({'message': 'Access to Yakuses Backend-API is available !!!'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)