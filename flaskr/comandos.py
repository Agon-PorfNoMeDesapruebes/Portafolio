import click
from flask.cli import with_appcontext

from .extensions import db
from .models import Usuario


@click.command("crear-admin")
@click.option("--username", prompt="Usuario")
@click.password_option()
@with_appcontext
def crear_admin(username, password):
    """Crea la cuenta de administrador (solo se permite una)."""
    if Usuario.query.first() is not None:
        click.echo("Ya existe un administrador. No se crea otro.")
        return

    admin = Usuario(username=username)
    admin.establecer_password(password)
    db.session.add(admin)
    db.session.commit()
    click.echo(f"Administrador '{username}' creado.")