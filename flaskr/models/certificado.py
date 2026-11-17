from ..extensions import db
from .elemento_portafolio import ElementoPortafolio


# HERENCIA: también recibe id, título, fecha y visible de la clase base.
class Certificado(ElementoPortafolio):
    __tablename__ = "certificado"

    institucion = db.Column(db.String(150), nullable=False)
    archivo = db.Column(db.String(255))

    # POLIMORFISMO: mismo nombre de método, otra forma de armar la tarjeta.
    def a_tarjeta(self):
        return {
            "tipo": "certificado",
            "titulo": self.titulo,
            "subtitulo": self.institucion,
            "descripcion": f"Obtenido el {self.fecha:%d/%m/%Y}",
            "imagen": self.archivo,
        }