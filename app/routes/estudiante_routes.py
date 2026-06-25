from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.models.grado import Grado
from app.models.seccion import Seccion

from app.services.estudiante_service import (
    EstudianteService
)


estudiante_bp = Blueprint(
    'estudiantes',
    __name__,
    url_prefix='/estudiantes'
)


@estudiante_bp.route('/')
def listar():

    estudiantes = (
        EstudianteService.listar_estudiantes()
    )

    return render_template(
        'estudiantes/listar.html',
        estudiantes=estudiantes
    )


@estudiante_bp.route('/crear', methods=['GET', 'POST'])
def crear():

    grados = Grado.query.all()

    secciones = Seccion.query.all()

    if request.method == 'POST':

        try:

            data = {

                'codigo': request.form['codigo'],

                'nombres': request.form['nombres'],

                'apellidos': request.form['apellidos'],

                'fecha_nacimiento': request.form.get(
                    'fecha_nacimiento'
                ),

                'grado_id': request.form['grado_id'],

                'seccion_id': request.form['seccion_id']
            }

            EstudianteService.crear_estudiante(
                data
            )

            flash(
                'Estudiante registrado correctamente.',
                'success'
            )

            return redirect(
                url_for('estudiantes.listar')
            )

        except Exception as error:

            flash(str(error), 'danger')

    return render_template(
        'estudiantes/crear.html',
        grados=grados,
        secciones=secciones
    )


@estudiante_bp.route('/detalle/<int:id>')
def detalle(id):

    estudiante = (
        EstudianteService.obtener_estudiante(id)
    )

    return render_template(
        'estudiantes/detalle.html',
        estudiante=estudiante
    )


@estudiante_bp.route(
    '/editar/<int:id>',
    methods=['GET', 'POST']
)
def editar(id):

    estudiante = (
        EstudianteService.obtener_estudiante(id)
    )

    grados = Grado.query.all()

    secciones = Seccion.query.all()

    if request.method == 'POST':

        data = {

            'codigo': request.form['codigo'],

            'nombres': request.form['nombres'],

            'apellidos': request.form['apellidos'],

            'fecha_nacimiento': request.form.get(
                'fecha_nacimiento'
            ),

            'grado_id': request.form['grado_id'],

            'seccion_id': request.form['seccion_id']
        }

        EstudianteService.actualizar_estudiante(
            estudiante,
            data
        )

        flash(
            'Estudiante actualizado correctamente.',
            'success'
        )

        return redirect(
            url_for('estudiantes.listar')
        )

    return render_template(
        'estudiantes/editar.html',
        estudiante=estudiante,
        grados=grados,
        secciones=secciones
    )


@estudiante_bp.route(
    '/eliminar/<int:id>',
    methods=['POST']
)
def eliminar(id):

    estudiante = (
        EstudianteService.obtener_estudiante(id)
    )

    EstudianteService.eliminar_estudiante(
        estudiante
    )

    flash(
        'Estudiante eliminado correctamente.',
        'success'
    )

    return redirect(
        url_for('estudiantes.listar')
    )