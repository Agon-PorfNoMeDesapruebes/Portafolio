from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from .extensions import db
from .archivos import borrar_imagen, guardar_imagen, guardar_pdf
from .forms import CategoriaForm, TecnologiaForm, ProyectoForm, PerfilForm
from .models import Categoria, Proyecto, Tecnologia, MensajeContacto, Perfil

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.before_request
def exigir_login():
    # Se ejecuta antes de CADA ruta de este blueprint: ninguna queda sin proteger.
    if g.usuario is None:
        return redirect(url_for("auth.login"))


@bp.route("/")
def index():
    return render_template(
        "admin/index.html",
        total_categorias=Categoria.query.count(),
        total_proyectos=Proyecto.query.count(),
        sin_leer=MensajeContacto.query.filter_by(leido=False).count(),
        total_tecnologias=Tecnologia.query.count(),
    )


@bp.route("/categorias")
def categorias_lista():
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template("admin/categorias/lista.html", categorias=categorias)


@bp.route("/categorias/nueva", methods=("GET", "POST"))
def categorias_nueva():
    form = CategoriaForm()
    if form.validate_on_submit():
        db.session.add(Categoria(nombre=form.nombre.data.strip()))
        db.session.commit()
        flash("Categoría creada.")
        return redirect(url_for("admin.categorias_lista"))
    return render_template("admin/categorias/form.html", form=form, titulo="Nueva categoría")


@bp.route("/categorias/<int:id>/editar", methods=("GET", "POST"))
def categorias_editar(id):
    categoria = db.get_or_404(Categoria, id)
    form = CategoriaForm(obj=categoria, categoria_id=categoria.id)
    if form.validate_on_submit():
        categoria.nombre = form.nombre.data.strip()
        db.session.commit()
        flash("Categoría actualizada.")
        return redirect(url_for("admin.categorias_lista"))
    return render_template("admin/categorias/form.html", form=form, titulo="Editar categoría")


@bp.route("/categorias/<int:id>/borrar", methods=("POST",))
def categorias_borrar(id):
    categoria = db.get_or_404(Categoria, id)
    if categoria.proyectos:
        flash("No se puede borrar: la categoría tiene proyectos asociados.")
        return redirect(url_for("admin.categorias_lista"))
    db.session.delete(categoria)
    db.session.commit()
    flash("Categoría borrada.")
    return redirect(url_for("admin.categorias_lista"))

@bp.route("/tecnologias")
def tecnologias_lista():
    tecnologias = Tecnologia.query.order_by(Tecnologia.nombre).all()
    return render_template("admin/tecnologias/lista.html", tecnologias=tecnologias)


@bp.route("/tecnologias/nueva", methods=("GET", "POST"))
def tecnologias_nueva():
    form = TecnologiaForm()
    if form.validate_on_submit():
        db.session.add(Tecnologia(
            nombre=form.nombre.data.strip(),
            icono=form.icono.data.strip() if form.icono.data else None,
            nivel=form.nivel.data,
        ))
        db.session.commit()
        flash("Tecnología creada.")
        return redirect(url_for("admin.tecnologias_lista"))
    return render_template("admin/tecnologias/form.html", form=form, titulo="Nueva tecnología")


@bp.route("/tecnologias/<int:id>/editar", methods=("GET", "POST"))
def tecnologias_editar(id):
    tecnologia = db.get_or_404(Tecnologia, id)
    form = TecnologiaForm(obj=tecnologia, tecnologia_id=tecnologia.id)
    if form.validate_on_submit():
        tecnologia.nombre = form.nombre.data.strip()
        tecnologia.icono = form.icono.data.strip() if form.icono.data else None
        tecnologia.nivel = form.nivel.data
        db.session.commit()
        flash("Tecnología actualizada.")
        return redirect(url_for("admin.tecnologias_lista"))
    return render_template("admin/tecnologias/form.html", form=form, titulo="Editar tecnología")


@bp.route("/tecnologias/<int:id>/borrar", methods=("POST",))
def tecnologias_borrar(id):
    tecnologia = db.get_or_404(Tecnologia, id)
    db.session.delete(tecnologia)
    db.session.commit()
    flash("Tecnología borrada.")
    return redirect(url_for("admin.tecnologias_lista"))


def _cargar_opciones(form):
    """Llena los desplegables con lo que hay en la base (antes de validar)."""
    form.categoria_id.choices = [
        (c.id, c.nombre) for c in Categoria.query.order_by(Categoria.nombre)
    ]
    form.tecnologias_ids.choices = [
        (t.id, t.nombre) for t in Tecnologia.query.order_by(Tecnologia.nombre)
    ]


def _copiar_a_proyecto(proyecto, form):
    """Pasa los datos del formulario al objeto (sirve para crear y para editar)."""
    proyecto.titulo = form.titulo.data
    proyecto.descripcion_corta = form.descripcion_corta.data.strip()
    proyecto.descripcion_larga = (form.descripcion_larga.data or "").strip() or None
    proyecto.fecha = form.fecha.data
    proyecto.url_repo = (form.url_repo.data or "").strip() or None
    proyecto.url_demo = (form.url_demo.data or "").strip() or None
    proyecto.categoria_id = form.categoria_id.data
    proyecto.destacado = form.destacado.data
    proyecto.visible = form.visible.data
    proyecto.tecnologias = Tecnologia.query.filter(
        Tecnologia.id.in_(form.tecnologias_ids.data)
    ).all()


@bp.route("/proyectos")
def proyectos_lista():
    proyectos = Proyecto.query.order_by(Proyecto.fecha.desc()).all()
    return render_template("admin/proyectos/lista.html", proyectos=proyectos)


@bp.route("/proyectos/nuevo", methods=("GET", "POST"))
def proyectos_nuevo():
    if Categoria.query.first() is None:
        flash("Antes de crear un proyecto necesitás al menos una categoría.")
        return redirect(url_for("admin.categorias_nueva"))

    form = ProyectoForm()
    _cargar_opciones(form)
    if form.validate_on_submit():
        try:
            portada = (
                guardar_imagen(form.portada_archivo.data)
                if form.portada_archivo.data else None
            )
        except ValueError as error:
            form.portada_archivo.errors.append(str(error))
        else:
            proyecto = Proyecto(portada=portada)
            _copiar_a_proyecto(proyecto, form)
            db.session.add(proyecto)
            db.session.commit()
            flash("Proyecto creado.")
            return redirect(url_for("admin.proyectos_lista"))
    return render_template(
        "admin/proyectos/form.html", form=form, proyecto=None, titulo="Nuevo proyecto"
    )


@bp.route("/proyectos/<int:id>/editar", methods=("GET", "POST"))
def proyectos_editar(id):
    proyecto = db.get_or_404(Proyecto, id)
    form = ProyectoForm(obj=proyecto)
    _cargar_opciones(form)
    if request.method == "GET":
        # Las tecnologías son objetos; el formulario necesita sus ids.
        form.tecnologias_ids.data = [t.id for t in proyecto.tecnologias]

    if form.validate_on_submit():
        try:
            portada_nueva = (
                guardar_imagen(form.portada_archivo.data)
                if form.portada_archivo.data else None
            )
        except ValueError as error:
            form.portada_archivo.errors.append(str(error))
        else:
            portada_vieja = proyecto.portada
            _copiar_a_proyecto(proyecto, form)
            if portada_nueva:
                proyecto.portada = portada_nueva
            db.session.commit()
            if portada_nueva:
                borrar_imagen(portada_vieja)  # recién cuando ya se guardó todo
            flash("Proyecto actualizado.")
            return redirect(url_for("admin.proyectos_lista"))
    return render_template(
        "admin/proyectos/form.html", form=form, proyecto=proyecto, titulo="Editar proyecto"
    )


@bp.route("/proyectos/<int:id>/borrar", methods=("POST",))
def proyectos_borrar(id):
    proyecto = db.get_or_404(Proyecto, id)
    portada = proyecto.portada
    db.session.delete(proyecto)
    db.session.commit()
    borrar_imagen(portada)
    flash("Proyecto borrado.")
    return redirect(url_for("admin.proyectos_lista"))



@bp.route("/perfil", methods=("GET", "POST"))
def perfil_editar():
    perfil = Perfil.query.first()
    es_nuevo = perfil is None
    if es_nuevo:
        perfil = Perfil()
    form = PerfilForm(obj=perfil)

    if form.validate_on_submit():
        foto_nueva = cv_nuevo = None
        if form.foto_archivo.data:
            try:
                foto_nueva = guardar_imagen(form.foto_archivo.data)
            except ValueError as error:
                form.foto_archivo.errors.append(str(error))
        if form.cv_archivo.data:
            try:
                cv_nuevo = guardar_pdf(form.cv_archivo.data)
            except ValueError as error:
                form.cv_archivo.errors.append(str(error))

        if form.foto_archivo.errors or form.cv_archivo.errors:
            # Algo falló: borramos lo que sí se había alcanzado a guardar.
            borrar_imagen(foto_nueva)
            borrar_imagen(cv_nuevo)
        else:
            foto_vieja, cv_viejo = perfil.foto, perfil.ruta_cv
            perfil.nombre = form.nombre.data.strip()
            perfil.titular = (form.titular.data or "").strip() or None
            perfil.bio = (form.bio.data or "").strip() or None
            if foto_nueva:
                perfil.foto = foto_nueva
            if cv_nuevo:
                perfil.ruta_cv = cv_nuevo
            if es_nuevo:
                db.session.add(perfil)
            db.session.commit()
            if foto_nueva:
                borrar_imagen(foto_vieja)
            if cv_nuevo:
                borrar_imagen(cv_viejo)
            flash("Perfil guardado.")
            return redirect(url_for("admin.perfil_editar"))
    return render_template("admin/perfil.html", form=form, perfil=perfil)



@bp.route("/mensajes")
def mensajes_lista():
    mensajes = MensajeContacto.query.order_by(MensajeContacto.fecha.desc()).all()
    return render_template("admin/mensajes/lista.html", mensajes=mensajes)


@bp.route("/mensajes/<int:id>")
def mensajes_detalle(id):
    mensaje = db.get_or_404(MensajeContacto, id)
    if not mensaje.leido:
        mensaje.leido = True  # abrirlo lo marca como leído
        db.session.commit()
    return render_template("admin/mensajes/detalle.html", mensaje=mensaje)


@bp.route("/mensajes/<int:id>/borrar", methods=("POST",))
def mensajes_borrar(id):
    mensaje = db.get_or_404(MensajeContacto, id)
    db.session.delete(mensaje)
    db.session.commit()
    flash("Mensaje borrado.")
    return redirect(url_for("admin.mensajes_lista"))