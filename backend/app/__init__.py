from dotenv import load_dotenv
from flask import Flask, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException
from .extensions import db, migrate, jwt, cors

def create_app(config_class=None):
    load_dotenv()
    if config_class is None:
        from .config import Config as config_class  # lê o .env já carregado

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    from . import models  # garante que as tabelas sejam registradas
    from .routes.eventos import bp as eventos_bp
    app.register_blueprint(eventos_bp)

    registrar_erros(app)
    return app


def registrar_erros(app):
    # A API sempre responde em JSON, inclusive nos erros
    @app.errorhandler(ValidationError)
    def erro_validacao(e):
        return jsonify({"erro": "Dados inválidos", "detalhes": e.messages}), 400

    @app.errorhandler(HTTPException)
    def erro_http(e):
        return jsonify({"erro": e.description}), e.code
