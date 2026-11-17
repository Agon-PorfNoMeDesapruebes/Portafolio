from abc import ABCMeta, abstractmethod

from ..extensions import db


# Metaclase combinada: une la de SQLAlchemy con la de abc.
# Sin esto, Python no deja mezclar db.Model con una clase abstracta.
class ElementoMeta(type(db.Model), ABCMeta):
    pass


# ABSTRACCIÓN: clase base abstracta. No se puede instanciar, solo sirve
# de molde: define lo que tienen en común Proyecto y Certificado.
class ElementoPortafolio(db.Model, metaclass=ElementoMeta):
    __abstract__ = True  # SQLAlchemy: no crea tabla para esta clase

    id = db.Column(db.Integer, primary_key=True)
    # ENCAPSULAMIENTO: el dato real vive en _titulo (atributo "privado" por
    # convención) y se accede solo a través de la propiedad "titulo".
    _titulo = db.Column("titulo", db.String(150), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    visible = db.Column(db.Boolean, nullable=False, default=True)

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        # ENCAPSULAMIENTO: la clase controla qué valores se aceptan.
        if not valor or not valor.strip():
            raise ValueError("El título no puede estar vacío.")
        self._titulo = valor.strip()

    # ABSTRACCIÓN: método obligatorio. Cada subclase DEBE implementarlo,
    # si no, Python no deja crear objetos de esa subclase.
    @abstractmethod
    def a_tarjeta(self):
        """Devuelve un diccionario con lo necesario para mostrar la tarjeta."""