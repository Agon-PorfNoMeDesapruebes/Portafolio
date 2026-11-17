from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def establecer_password(self, password):
        # Nunca se guarda la contraseña: solo su hash
        self.password_hash = generate_password_hash(password)

    def verificar_password(self, password):
        return check_password_hash(self.password_hash, password)