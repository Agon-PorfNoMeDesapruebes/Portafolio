from ..extensions import db


class Imagen(db.Model):
    __tablename__ = "imagen"

    id = db.Column(db.Integer, primary_key=True)
    archivo = db.Column(db.String(255), nullable=False)
    orden = db.Column(db.Integer, nullable=False, default=0)
    proyecto_id = db.Column(db.Integer, db.ForeignKey("proyecto.id"), nullable=False)

    proyecto = db.relationship("Proyecto", back_populates="imagenes")