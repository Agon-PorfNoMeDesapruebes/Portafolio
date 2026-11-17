from ..extensions import db
from .elemento_portafolio import ElementoPortafolio


# Tabla intermedia: NO es una clase, solo dos claves foráneas
# que juntas forman la clave primaria (igual que en tu script SQL).
proyecto_tecnologia = db.Table(
    "proyecto_tecnologia",
    db.Column("proyecto_id", db.Integer, db.ForeignKey("proyecto.id"), primary_key=True),
    db.Column("tecnologia_id", db.Integer, db.ForeignKey("tecnologia.id"), primary_key=True),
)


class Proyecto(ElementoPortafolio):
    __tablename__ = "proyecto"

    descripcion_corta = db.Column(db.String(255), nullable=False)
    descripcion_larga = db.Column(db.Text)
    url_repo = db.Column(db.String(255))
    url_demo = db.Column(db.String(255))
    portada = db.Column(db.String(255))
    destacado = db.Column(db.Boolean, nullable=False, default=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)

    # Relación 1:N (muchos proyectos, una categoría)
    categoria = db.relationship("Categoria", back_populates="proyectos")

    # Relación N:N (a través de la tabla intermedia)
    tecnologias = db.relationship(
        "Tecnologia",
        secondary=proyecto_tecnologia,
        back_populates="proyectos",
    )

    imagenes = db.relationship(
        "Imagen",
        back_populates="proyecto",
        cascade="all, delete-orphan",
        order_by="Imagen.orden",
    )

    def __repr__(self):
        return f"<Proyecto {self.titulo}>"
    
    def a_tarjeta(self):
        return {
            "tipo": "proyecto",
            "titulo": self.titulo,
            "subtitulo": self.categoria.nombre,
            "descripcion": self.descripcion_corta,
            "imagen": self.portada,
            "tecnologias": [t.nombre for t in self.tecnologias],
            "url_repo": self.url_repo,
            "url_demo": self.url_demo,
        }