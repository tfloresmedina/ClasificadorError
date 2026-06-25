from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.database.connection import db

from app.models.seccion import Seccion


seccion_bp = Blueprint(

    'seccion',

    __name__,

    url_prefix='/secciones'
)


# =====================================================
# LISTAR
# =====================================================

@seccion_bp.route('/')
def listar_secciones():

    secciones = (
        Seccion.query.all()
    )

    return render_template(

        'secciones/listar.html',

        secciones=secciones
    )


# =====================================================
# CREAR
# =====================================================

@seccion_bp.route(
    '/crear',
    methods=['GET', 'POST']
)
def crear_seccion():

    if request.method == 'POST':

        try:

            nueva = Seccion(

                nombre=request.form['nombre']
            )

            db.session.add(nueva)

            db.session.commit()

            flash(
                'Sección creada correctamente.',
                'success'
            )

            return redirect(
                url_for(
                    'seccion.listar_secciones'
                )
            )

        except Exception as error:

            flash(str(error), 'danger')

    return render_template(
        'secciones/crear.html'
    )


# =====================================================
# DETALLE
# =====================================================

@seccion_bp.route('/detalle/<int:id>')
def detalle_seccion(id):

    seccion = (
        Seccion.query.get_or_404(id)
    )

    return render_template(

        'secciones/detalle.html',

        seccion=seccion
    )