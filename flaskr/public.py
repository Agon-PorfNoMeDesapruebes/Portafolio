from flask import Blueprint, flash, redirect, render_template, url_for

from .extensions import db
from .forms import ContactoForm
from .models import Perfil, Proyecto, Tecnologia, Certificado, MensajeContacto

bp = Blueprint("public", __name__)


@bp.route("/", methods=("GET", "POST"))
def index():
    form = ContactoForm()

    if form.validate_on_submit():
        mensaje = MensajeContacto(
            nombre=form.nombre.data,
            email=form.email.data,
            texto=form.texto.data,
        )
        db.session.add(mensaje)
        db.session.commit()
        flash("¡Gracias! Tu mensaje fue enviado.")
        return redirect(url_for("public.index", _anchor="contacto"))

    perfil = Perfil.query.first()
    proyectos = (
        Proyecto.query.filter_by(visible=True).order_by(Proyecto.fecha.desc()).all()
    )
    tecnologias = Tecnologia.query.order_by(Tecnologia.nivel.desc()).all()
    certificados = (
        Certificado.query.filter_by(visible=True).order_by(Certificado.fecha.desc()).all()
    )

    return render_template(
        "index.html",
        form=form,
        perfil=perfil,
        proyectos=[p.a_tarjeta() for p in proyectos],
        tecnologias=tecnologias,
        certificados=[c.a_tarjeta() for c in certificados],
    )