from flask import (

    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.services.analysis_service import (
    AnalysisService
)



from app.models.evaluacion import Evaluacion

from app.models.estudiante import Estudiante

from app.models.resultado_analisis import ResultadoAnalisis

analysis_bp = Blueprint(

    'analysis',

    __name__
)


# =========================================================
# FORMULARIO PRINCIPAL
# =========================================================
@analysis_bp.route(
    '/analizar',
    methods=['GET']
)
def vista_analisis():

    evaluacion_id = request.args.get(
        'evaluacion_id'
    )

    evaluacion = None
    estudiantes = []

    analisis_por_estudiante = {}


    # =========================================
    # SI EXISTE EVALUACIÓN
    # =========================================

    if evaluacion_id:

        evaluacion = Evaluacion.query.get(
            evaluacion_id
        )


        if evaluacion:

            estudiantes = Estudiante.query.filter_by(
                seccion_id=evaluacion.seccion_id
            ).all()


            # =====================================
            # VALIDAR ANÁLISIS EXISTENTE
            # =====================================

            for estudiante in estudiantes:

                resultado = ResultadoAnalisis.query.filter_by(
                    evaluacion_id=evaluacion.id,
                    estudiante_id=estudiante.id
                ).first()


                analisis_por_estudiante[
                    estudiante.id
                ] = resultado


    return render_template(

        'analysis/analizar.html',

        evaluacion=evaluacion,

        evaluacion_id=evaluacion_id,

        estudiantes=estudiantes,

        evaluaciones=Evaluacion.query.all(),

        analisis_por_estudiante=
            analisis_por_estudiante
    )


# =========================================================
# PROCESAR ANÁLISIS
# =========================================================

@analysis_bp.route(
    '/procesar-analisis',
    methods=['POST']
)

def procesar_analisis():


    try:


        respuesta_ocr = request.form.get(
            'respuesta_ocr'
        )


        respuesta_correcta = request.form.get(
            'respuesta_correcta'
        )


        # VALIDACIÓN SIMPLE

        if not respuesta_ocr:

            flash(

                'Debe ingresar una respuesta.',

                'danger'
            )

            return redirect(

                url_for(
                    'analysis.vista_analisis'
                )
            )


        if not respuesta_correcta:

            flash(

                'Debe ingresar una respuesta correcta.',

                'danger'
            )

            return redirect(

                url_for(
                    'analysis.vista_analisis'
                )
            )


        # =====================================================
        # EJECUTAR ANÁLISIS
        # =====================================================

        resultado = (

            AnalysisService
            .analizar_respuesta(

                respuesta_ocr=
                    respuesta_ocr,

                respuesta_correcta=
                    respuesta_correcta
            )
        )


        # =====================================================
        # RENDER RESULTADO
        # =====================================================

        return render_template(

            'analysis/resultado.html',

            resultado=
                resultado
        )


    except Exception as e:


        flash(

            f'Error durante el análisis: {str(e)}',

            'danger'
        )


        return redirect(

            url_for(
                'analysis.vista_analisis'
            )
        )