from flask import Blueprint, jsonify, request
from app.schemas import UsuarioSchema
from app.services import usuario_service

bp = Blueprint("usuarios", __name__, url_prefix="/api/usuarios")

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)


@bp.get("/")
def listar():
    return jsonify(usuarios_schema.dump(usuario_service.listar_usuarios()))


@bp.get("/<int:id>")
def detalhar(id):
    return jsonify(usuario_schema.dump(usuario_service.buscar_usuario(id)))


@bp.post("/")
def cadastrar():
    usuario = usuario_service.cadastrar_usuario(request.get_json())
    return jsonify(usuario_schema.dump(usuario)), 201


@bp.post("/login")
def login():
    usuario, token = usuario_service.autenticar(request.get_json())
    return jsonify({"access_token": token, "usuario": usuario_schema.dump(usuario)})
