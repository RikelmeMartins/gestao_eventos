from app.extensions import db
from app.models import Evento
from app.schemas import EventoSchema

evento_schema = EventoSchema()


def listar_eventos():
    return db.session.scalars(db.select(Evento).order_by(Evento.data_inicio)).all()


def buscar_evento(id):
    return db.get_or_404(Evento, id, description="Evento não encontrado.")


def criar_evento(dados):
    evento = Evento(**evento_schema.load(dados))
    db.session.add(evento)
    db.session.commit()
    return evento


def atualizar_evento(id, dados, parcial=False):
    evento = buscar_evento(id)
    if parcial and isinstance(dados, dict):
        # Mescla com os dados atuais para validar o evento completo (ex.: data_fim >= data_inicio)
        atuais = evento_schema.dump(evento)
        atuais.pop("id")
        dados = {**atuais, **dados}
    for campo, valor in evento_schema.load(dados).items():
        setattr(evento, campo, valor)
    db.session.commit()
    return evento


def excluir_evento(id):
    evento = buscar_evento(id)
    db.session.delete(evento)
    db.session.commit()
