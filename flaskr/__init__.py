from flask import Flask

from .config import Config
from .extensions import db, csrf


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config is not None:
        # Configuración de prueba: pisa los valores por defecto.
        app.config.from_mapping(test_config)

    csrf.init_app(app)
    db.init_app(app)

    from . import models  # noqa: F401  (registra los modelos)
    
    from . import auth
    app.register_blueprint(auth.bp)

    from . import public
    app.register_blueprint(public.bp)

    from .comandos import crear_admin
    app.cli.add_command(crear_admin)

    from . import admin
    app.register_blueprint(admin.bp)

    return app