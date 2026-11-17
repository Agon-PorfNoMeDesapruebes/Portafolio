from ..extensions import db


class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False, unique=True)
    proyectos = db.relationship("Proyecto", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria {self.nombre}>"