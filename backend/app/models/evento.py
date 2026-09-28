from app.extensions import db

class Evento(db.Model):
    __tablename__ = "eventos"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    local = db.Column(db.String(200))
    vagas = db.Column(db.Integer, default=0)