from ..extensions import db


class MensajeContacto(db.Model):
    __tablename__ = "mensaje_contacto"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    leido = db.Column(db.Boolean, nullable=False, default=False)