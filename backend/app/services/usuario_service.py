from flask import abort
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models import Usuario
from app.schemas import UsuarioSchema, LoginSchema

usuario_schema = UsuarioSchema()
login_schema = LoginSchema()


def listar_usuarios():
    return db.session.scalars(db.select(Usuario).order_by(Usuario.nome)).all()


def buscar_usuario(id):
    return db.get_or_404(Usuario, id, description="Usuário não encontrado.")


def buscar_por_email(email):
    return db.session.scalar(db.select(Usuario).filter_by(email=email))


def cadastrar_usuario(dados):
    dados = usuario_schema.load(dados)
    email = dados["email"].strip().lower()
    if buscar_por_email(email):
        abort(409, description="E-mail já cadastrado.")

    usuario = Usuario(nome=dados["nome"], email=email)
    usuario.encripitar_senha(dados["senha"])
    db.session.add(usuario)
    db.session.commit()
    return usuario


def autenticar(dados):
    dados = login_schema.load(dados)
    usuario = buscar_por_email(dados["email"].strip().lower())
    # Mesma mensagem nos dois casos para não revelar quais e-mails existem
    if not usuario or not usuario.verificar_senha(dados["senha"]):
        abort(401, description="E-mail ou senha inválidos.")

    token = create_access_token(identity=str(usuario.id), additional_claims={"perfil": usuario.perfil})
    return usuario, token
