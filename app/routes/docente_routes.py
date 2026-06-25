from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

import os
from app.models.evaluacion import (
    Evaluacion
)

from app.models.examen_alumno import (
    ExamenAlumno
)

from app.models.respuesta_alumno import (
    RespuestaAlumno
)

from app.services.analysis_service import (
    AnalysisService
)

from app.services.save_analysis_service import (
    SaveAnalysisService
)

from app.models.bimestre import (
    Bimestre
)

from app.models.evaluacion import (
    Evaluacion
)

from werkzeug.utils import (
    secure_filename
)

from app.models.estudiante import (
    Estudiante
)

from app.models.seccion import (
    Seccion
)

from app.models.bimestre import (
    Bimestre
)

from app.services.docente_service import (
    DocenteService
)

from flask_login import (
    login_required
)

from app.services.role_required_service import (
    role_required
)

from app.services.docente_section_service import (
    DocenteSectionService
)

from app.models.evaluacion import (
    Evaluacion
)

from app.services.ocr_service import (
    OCRService
)

from app.services.math_normalizer_service import (
    MathNormalizerService
)

from app.models.resultado_analisis import (
    ResultadoAnalisis
)

from app.database.connection import db

docente_bp = Blueprint(
    'docentes',
    __name__,
    url_prefix='/docentes'
)


@docente_bp.route('/')
def listar():

    docentes = (
        DocenteService.listar_docentes()
    )

    return render_template(
        'docentes/listar.html',
        docentes=docentes
    )


@docente_bp.route(
    '/crear',
    methods=['GET', 'POST']
)
def crear():

    if request.method == 'POST':

        data = {

            'codigo': request.form['codigo'],

            'nombres': request.form['nombres'],

            'apellidos': request.form['apellidos'],

            'especialidad': request.form[
                'especialidad'
            ]
        }

        DocenteService.crear_docente(data)

        flash(
            'Docente registrado correctamente.',
            'success'
        )

        return redirect(
            url_for('docentes.listar')
        )

    return render_template(
        'docentes/crear.html'
    )


@docente_bp.route('/detalle/<int:id>')
def detalle(id):

    docente = (
        DocenteService.obtener_docente(id)
    )

    return render_template(
        'docentes/detalles.html',
        docente=docente
    )


@docente_bp.route(
    '/editar/<int:id>',
    methods=['GET', 'POST']
)
def editar(id):

    docente = (
        DocenteService.obtener_docente(id)
    )

    if request.method == 'POST':

        data = {

            'codigo': request.form['codigo'],

            'nombres': request.form['nombres'],

            'apellidos': request.form['apellidos'],

            'especialidad': request.form[
                'especialidad'
            ]
        }

        DocenteService.actualizar_docente(
            docente,
            data
        )

        flash(
            'Docente actualizado correctamente.',
            'success'
        )

        return redirect(
            url_for('docentes.listar')
        )

    return render_template(
        'docentes/editar.html',
        docente=docente
    )


@docente_bp.route(
    '/eliminar/<int:id>',
    methods=['POST']
)
def eliminar(id):

    docente = (
        DocenteService.obtener_docente(id)
    )

    DocenteService.eliminar_docente(
        docente
    )

    flash(
        'Docente eliminado correctamente.',
        'success'
    )

    return redirect(
        url_for('docentes.listar')
    )

# =========================================================
# MIS SECCIONES
# =========================================================

@docente_bp.route(
    '/mis-secciones',
    methods=['GET']
)

@login_required

@role_required(
    'administrador',
    'docente'
)
def mis_secciones():


    secciones = (

        DocenteSectionService
        .obtener_secciones_docente()
    )


    return render_template(

        'docentes/mis_secciones.html',

        secciones=
            secciones
    )



# =========================================================
# DETALLE SECCIÓN
# =========================================================

@docente_bp.route(
    '/seccion/<int:seccion_id>',
    methods=['GET']
)

@login_required

@role_required(
    'administrador',
    'docente'
)
def detalle_seccion(


    seccion_id
):


    seccion = (

        Seccion
        .query
        .get_or_404(
            seccion_id
        )
    )


    estudiantes = (
        seccion.estudiantes
    )


    bimestres = (

        Bimestre
        .query
        .all()
    )


    return render_template(

        'docentes/detalle_seccion.html',

        seccion=
            seccion,

        estudiantes=
            estudiantes,

        bimestres=
            bimestres
    )


# =========================================================
# DETALLE BIMESTRE
# =========================================================

@docente_bp.route(
    '/seccion/<int:seccion_id>/bimestre/<int:bimestre_id>',
    methods=['GET']
)

@login_required

@role_required(
    'administrador',
    'docente'
)
def detalle_bimestre(


    seccion_id,

    bimestre_id
):


    seccion = (

        Seccion
        .query
        .get_or_404(
            seccion_id
        )
    )


    bimestre = (

        Bimestre
        .query
        .get_or_404(
            bimestre_id
        )
    )


    evaluaciones = (

        Evaluacion
        .query
        .filter_by(

            seccion_id=
                seccion.id,

            bimestre_id=
                bimestre.id
        )
        .all()
    )


    return render_template(

        'docentes/detalle_bimestre.html',

        seccion=
            seccion,

        bimestre=
            bimestre,

        evaluaciones=
            evaluaciones
    )

# =========================================================
# DETALLE EVALUACIÓN
# =========================================================

@docente_bp.route(
    '/evaluacion/<int:evaluacion_id>',
    methods=['GET']
)

@login_required

@role_required(
    'administrador',
    'docente'
)
def detalle_evaluacion(


    evaluacion_id
):


    evaluacion = (

        Evaluacion
        .query
        .get_or_404(
            evaluacion_id
        )
    )


    estudiantes = (

        evaluacion
        .seccion
        .estudiantes
    )

    examenes = (

        ExamenAlumno
        .query
        .filter_by(

            evaluacion_id=
                evaluacion.id
        )
        .all()
    )

    examenes_map = {

        examen.estudiante_id:
            examen

        for examen in examenes
    }

    return render_template(

    'docentes/detalle_evaluacion.html',

    evaluacion=
        evaluacion,

    estudiantes=
        estudiantes,

    examenes_map=
        examenes_map
    )

# =========================================================
# SUBIR EXAMEN MODELO
# =========================================================

@docente_bp.route(
    '/evaluacion/<int:evaluacion_id>/modelo',
    methods=['POST']
)

@login_required

@role_required(
    'administrador',
    'docente'
)
def subir_modelo(


    evaluacion_id
):


    evaluacion = (

        Evaluacion
        .query
        .get_or_404(
            evaluacion_id
        )
    )


    archivo = request.files.get(
        'modelo'
    )


    if not archivo:


        flash(

            'Debe seleccionar '
            'una imagen.',

            'danger'
        )


        return redirect(
            request.referrer
        )


    # =============================================
    # NOMBRE
    # =============================================

    nombre_archivo = secure_filename(

        archivo.filename
    )


    carpeta = (

        'app/static/modelos'
    )


    os.makedirs(

        carpeta,

        exist_ok=True
    )


    ruta = os.path.join(

        carpeta,

        nombre_archivo
    )


    archivo.save(
        ruta
    )

        
    # =============================================
    # OCR
    # =============================================

    resultado_ocr = (

        OCRService
        .extraer_texto(
            ruta
        )
    )


    texto_ocr = (

        resultado_ocr.get(
            'texto',
            ''
        )
    )


    # =============================================
    # NORMALIZACIÓN
    # =============================================

    expresion_normalizada = (

        MathNormalizerService
        .normalizar_expresion(

            texto_ocr
        )
    )


    # =============================================
    # GUARDAR
    # =============================================

    evaluacion.examen_modelo = (
        ruta
    )


    evaluacion.modelo_ocr = (
        texto_ocr
    )


    evaluacion.modelo_normalizado = (
        expresion_normalizada
    )


    db.session.commit()


    flash(

        'Examen modelo '
        'procesado correctamente.',

        'success'
    )


    return redirect(

        url_for(

            'docentes.detalle_evaluacion',

            evaluacion_id=
                evaluacion.id
        )
    )
# =========================================================
# RESULTADO ALUMNO
# =========================================================

@docente_bp.route(
    '/resultado/<int:estudiante_id>',
    methods=['GET']
)

@login_required

@role_required(
    'administrador',
    'docente'
)
def resultado_alumno(


    estudiante_id
):


    estudiante = (

        Estudiante
        .query
        .get_or_404(
            estudiante_id
        )
    )


    resultado = (

        ResultadoAnalisis
        .query
        .filter_by(

            estudiante_id=
                estudiante.id
        )
        .order_by(

            ResultadoAnalisis.id.desc()
        )
        .first()
    )


    return render_template(

        'docentes/resultado_alumno.html',

        estudiante=
            estudiante,

        resultado=
            resultado
    )

# =========================================================
# SUBIR EXAMEN
# =========================================================

@docente_bp.route(
    '/evaluacion/<int:evaluacion_id>/subir/<int:estudiante_id>',
    methods=['GET', 'POST']
)

@login_required

@role_required(
    'administrador',
    'docente'
)

def subir_examen(

    evaluacion_id,

    estudiante_id
):


    estudiante = (

        Estudiante
        .query
        .get_or_404(
            estudiante_id
        )
    )

    evaluacion = (

            Evaluacion
            .query
            .get_or_404(
                evaluacion_id
            )
        )

    # =============================================
    # POST
    # =============================================

    if request.method == 'POST':


        archivo = request.files.get(
            'imagen'
        )


        if not archivo:


            flash(

                'Debe seleccionar '
                'una imagen.',

                'danger'
            )


            return redirect(
                request.url
            )


        # =============================================
        # NOMBRE
        # =============================================

        nombre_archivo = secure_filename(

            archivo.filename
        )


        carpeta = (

            'app/static/uploads'
        )


        os.makedirs(

            carpeta,

            exist_ok=True
        )


        ruta = os.path.join(

            carpeta,

            nombre_archivo
        )


        archivo.save(
            ruta
        )

        # =============================================
        # EXAMEN ALUMNO
        # =============================================

        examen = ExamenAlumno(

            estudiante_id=
                estudiante.id,

            evaluacion_id=
                evaluacion.id
        )


        db.session.add(
            examen
        )


        db.session.commit()

                # =============================================
        # OCR
        # =============================================

        resultado_ocr = (

            OCRService
            .extraer_texto(
                ruta
            )
        )


        texto_ocr = (

            resultado_ocr.get(
                'texto',
                ''
            )
        )
        
        # =============================================
        # NORMALIZACIÓN
        # =============================================

        expresion_normalizada = (

            MathNormalizerService
            .normalizar_expresion(

                texto_ocr
            )
        )

        # =============================================
        # ANALYSIS SERVICE
        # =============================================

        resultado_analisis = (

            AnalysisService
            .analizar_respuesta(


                respuesta_estudiante=
                    expresion_normalizada,


                respuesta_correcta=

                    evaluacion
                    .modelo_normalizado
            )
        )

        # =============================================
        # SAVE ANALYSIS
        # =============================================

        SaveAnalysisService.salvar_resultado(


            estudiante=
                estudiante,


            resultado=
                resultado_analisis,


            respuesta_original=
                texto_ocr,


            respuesta_normalizada=
                expresion_normalizada
        )

        flash(

            'Examen analizado '
            'correctamente.',

            'success'
        )


        return redirect(

            url_for(

                'dashboard.dashboard_principal'
            )
        )


    return render_template(

        'docentes/subir_examen.html',

        estudiante=
            estudiante
    )