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


resultados_bp = Blueprint(

    'reportes',

    __name__,

    url_prefix='/reportes'
)


# =========================================================
# VISTA PRINCIPAL
# =========================================================

@resultados_bp.route(
    '/analizar',
    methods=['GET']
)

def vista_analisis():

    return render_template(

        'resultados/analizar.html'
    )


# =========================================================
# PROCESAMIENTO
# =========================================================

@resultados_bp.route(
    '/procesar',
    methods=['POST']
)

def procesar_analisis():


    try:


        # =================================================
        # DATOS FORMULARIO
        # =================================================

        respuesta_ocr = request.form.get(
            'respuesta_ocr'
        )


        respuesta_correcta = request.form.get(
            'respuesta_correcta'
        )


        # =================================================
        # VALIDACIONES
        # =================================================

        if not respuesta_ocr:

            flash(

                'Debe ingresar una respuesta OCR.',

                'danger'
            )

            return redirect(

                url_for(
                    'reportes.vista_analisis'
                )
            )


        if not respuesta_correcta:

            flash(

                'Debe ingresar la respuesta correcta.',

                'danger'
            )

            return redirect(

                url_for(
                    'reportes.vista_analisis'
                )
            )


        # =================================================
        # ANÁLISIS INTELIGENTE
        # =================================================

        resultado = (

            AnalysisService
            .analizar_respuesta(

                respuesta_ocr=
                    respuesta_ocr,

                respuesta_correcta=
                    respuesta_correcta
            )
        )


        # =================================================
        # RENDER RESULTADOS
        # =================================================

        return render_template(

            'resultados/resultado.html',

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
                'reportes.vista_analisis'
            )
        )