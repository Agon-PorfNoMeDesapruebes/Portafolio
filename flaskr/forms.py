from datetime import date
from urllib.parse import urlparse

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, SubmitField, TextAreaField, SelectField, SelectMultipleField, DateField, BooleanField)
from wtforms.validators import DataRequired, Length, Email, Optional, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput

from .models import Categoria, Tecnologia

from .models import Categoria, Tecnologia

class CategoriaForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=60)])
    submit = SubmitField("Guardar")

    def __init__(self, *args, categoria_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.categoria_id = categoria_id  # None si se está creando una nueva

    def validate_nombre(self, campo):
        existente = Categoria.query.filter_by(nombre=campo.data.strip()).first()
        if existente is not None and existente.id != self.categoria_id:
            raise ValidationError("Ya existe una categoría con ese nombre.")

class ContactoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=150)])
    texto = TextAreaField("Mensaje", validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField("Enviar")

class LoginForm(FlaskForm):
    username = StringField(
        'Nombre de usuario',
        validators=[DataRequired(message='El nombre de usuario es obligatorio.')],
    )
    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(message='La contraseña es obligatoria.')],
    )
    submit = SubmitField('Iniciar sesión')

class PostForm(FlaskForm):
    title = StringField(
        'Título',
        validators=[DataRequired(message='El título es obligatorio.')],
    )
    body = TextAreaField('Contenido')
    submit = SubmitField('Guardar')

class TecnologiaForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=60)])
    icono = StringField("Ícono (clase CSS)", validators=[Optional(), Length(max=100)])
    nivel = SelectField(
        "Nivel",
        choices=[(1, "1 - Básico"), (2, "2 - Intermedio bajo"), (3, "3 - Intermedio"),
                 (4, "4 - Avanzado"), (5, "5 - Experto")],
        coerce=int,
    )
    submit = SubmitField("Guardar")

    def __init__(self, *args, tecnologia_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tecnologia_id = tecnologia_id

    def validate_nombre(self, campo):
        existente = Tecnologia.query.filter_by(nombre=campo.data.strip()).first()
        if existente is not None and existente.id != self.tecnologia_id:
            raise ValidationError("Ya existe una tecnología con ese nombre.")

def url_http(form, campo):
    """Acepta solo enlaces http/https (rechaza, por ejemplo, javascript:...)."""
    if campo.data and urlparse(campo.data.strip()).scheme not in ("http", "https"):
        raise ValidationError("La dirección debe empezar con http:// o https://")


class ProyectoForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(max=150)])
    descripcion_corta = StringField("Descripción corta", validators=[DataRequired(), Length(max=255)])
    descripcion_larga = TextAreaField("Descripción larga", validators=[Optional(), Length(max=5000)])
    fecha = DateField("Fecha", validators=[DataRequired()], default=date.today)
    url_repo = StringField("Repositorio (URL)", validators=[Optional(), Length(max=255), url_http])
    url_demo = StringField("Demo (URL)", validators=[Optional(), Length(max=255), url_http])
    categoria_id = SelectField("Categoría", coerce=int, validators=[DataRequired()])
    tecnologias_ids = SelectMultipleField(
        "Tecnologías", coerce=int,
        widget=ListWidget(prefix_label=False), option_widget=CheckboxInput(),
    )
    portada_archivo = FileField(
        "Portada",
        validators=[FileAllowed(["jpg", "jpeg", "png", "webp"], "Solo imágenes JPG, PNG o WebP.")],
    )
    destacado = BooleanField("Destacado")
    visible = BooleanField("Visible", default=True)
    submit = SubmitField("Guardar")


class PerfilForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    titular = StringField("Frase o título", validators=[Optional(), Length(max=150)])
    bio = TextAreaField("Sobre mí", validators=[Optional(), Length(max=3000)])
    foto_archivo = FileField(
        "Foto",
        validators=[FileAllowed(["jpg", "jpeg", "png", "webp"], "Solo imágenes JPG, PNG o WebP.")],
    )
    cv_archivo = FileField("CV (PDF)", validators=[FileAllowed(["pdf"], "Solo archivos PDF.")])
    submit = SubmitField("Guardar")