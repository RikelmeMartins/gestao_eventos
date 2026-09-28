import os
from dotenv import load_dotenv
from flask import Flask
from .extensions import db, migrate, jwt, cors

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    from . import models  # garante que as tabelas sejam registradas
    from .routes.eventos import bp as eventos_bp
    app.register_blueprint(eventos_bp)
    return app