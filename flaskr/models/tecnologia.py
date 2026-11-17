from ..extensions import db


class Tecnologia(db.Model):
    __tablename__ = "tecnologia"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False, unique=True)
    icono = db.Column(db.String(100))
    nivel = db.Column(db.SmallInteger, nullable=False, default=3)

    # Lado "muchos a muchos": las tecnologías conocen sus proyectos
    proyectos = db.relationship(
        "Proyecto",
        secondary="proyecto_tecnologia",
        back_populates="tecnologias",
    )

    def __repr__(self):
        return f"<Tecnologia {self.nombre}>"