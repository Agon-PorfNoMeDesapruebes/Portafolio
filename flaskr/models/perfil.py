from ..extensions import db


class Perfil(db.Model):
    __tablename__ = "perfil"

    # id fijo en 1: la base lo exige con el CHECK, y no es autoincremental
    id = db.Column(db.SmallInteger, primary_key=True, autoincrement=False, default=1)
    nombre = db.Column(db.String(100), nullable=False)
    titular = db.Column(db.String(150))
    bio = db.Column(db.Text)
    foto = db.Column(db.String(255))
    ruta_cv = db.Column(db.String(255))