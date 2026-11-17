import functools

from flask import Blueprint, flash, g, redirect, render_template, session, url_for

from .extensions import db
from .forms import LoginForm
from .models import Usuario

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def cargar_usuario_logueado():
    usuario_id = session.get("usuario_id")
    g.usuario = db.session.get(Usuario, usuario_id) if usuario_id else None


def login_required(vista):
    @functools.wraps(vista)
    def vista_envuelta(*args, **kwargs):
        if g.usuario is None:
            return redirect(url_for("auth.login"))
        return vista(*args, **kwargs)

    return vista_envuelta


@bp.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        if usuario is not None and usuario.verificar_password(form.password.data):
            session.clear()
            session["usuario_id"] = usuario.id
            return redirect(url_for("admin.index"))
        flash("Usuario o contraseña incorrectos.")
    return render_template("auth/login.html", form=form)


@bp.route("/logout", methods=("POST",))
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/panel")
@login_required
def panel():
    return render_template("auth/panel.html")