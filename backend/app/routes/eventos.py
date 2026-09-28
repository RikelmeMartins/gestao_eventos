from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Evento

bp = Blueprint("eventos", __name__, url_prefix="/api/eventos")

@bp.get("/")
def listar():
    eventos = Evento.query.all()
    return jsonify([{"id": e.id, "titulo": e.titulo, "local": e.local} for e in eventos])

@bp.post("/")
def criar():
    dados = request.get_json()
    e = Evento(**dados)
    db.session.add(e)
    db.session.commit()
    return jsonify({"id": e.id}), 201