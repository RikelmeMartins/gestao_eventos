import click
from .extensions import db
from .models.usuario import Usuario


def registrar_comandos(app):
    @app.cli.command("criar-admin")
    @click.argument("email")
    def criar_admin(email):
        """Promove um usuário existente a administrador."""
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario is None:
            raise click.ClickException(f"Nenhum usuário com o email {email}")

        if usuario.perfil == "administrador":
            click.echo(f"{email} já é administrador.")
            return

        usuario.perfil = "administrador"
        db.session.commit()
        click.echo(f"{email} agora é administrador. Faça login de novo para gerar um token novo.")
