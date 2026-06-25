from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
import json
import os
from app.database.connection import db

from app.models.evaluacion import Evaluacion
from app.models.seccion import Seccion
from app.services.ocr_service import (
    OCRService
)

from app.services.math_normalizer_service import (
    MathNormalizerService
)
from app.services.exercise_detector_service import (
    ExerciseDetectorService
)

from app.services.math_procedure_parser_service import (
    MathProcedureParserService
)
evaluacion_bp = Blueprint(

    'evaluacion',

    __name__,

    url_prefix='/evaluaciones'
)


# =====================================================
# LISTAR
# =====================================================

# =====================================================
# LISTAR
# =====================================================

@evaluacion_bp.route('/')
def listar_evaluaciones():

    evaluaciones = (
        Evaluacion.query.all()
    )

    return render_template(

        'evaluaciones/listar.html',

        evaluaciones=evaluaciones
    )

@evaluacion_bp.route(
    '/crear',
    methods=['GET', 'POST']
)
def crear_evaluacion():

    secciones = (
        Seccion.query.all()
    )

    if request.method == 'POST':

        try:

            # ============================================
            # RESOLUCIÓN MODELO
            # ============================================

            respuesta_modelo = request.form.get(
                'respuesta_modelo'
            )

            imagen_modelo = request.files.get(
                'imagen_modelo'
            )

            ruta_modelo = None

            modelo_ocr = None

            modelo_normalizado = None

            procedimiento_modelo = []
            
            if imagen_modelo and imagen_modelo.filename:

                nombre_archivo = (
                    imagen_modelo.filename
                )

                extension = os.path.splitext(
                    nombre_archivo
                )[1].lower()

                if extension not in [
                    '.jpg',
                    '.jpeg',
                    '.png',
                    '.pdf'
                ]:
                    flash(
                        'Formato no permitido',
                        'danger'
                    )
                    return redirect(
                        request.url
                    )
                

                ruta_modelo = (

                    f'uploads/modelos/{nombre_archivo}'
                )

                os.makedirs(
                    'uploads/modelos',
                    exist_ok=True
                )

                imagen_modelo.save(
                    ruta_modelo
                )

                # ============================================
                # OCR EXAMEN MODELO
                # ============================================

                modelo_ocr = None

                modelo_normalizado = None

                resultado_ocr = (

                    OCRService
                    .extraer_texto(
                        ruta_modelo
                    )
                )

                if resultado_ocr.get(
                    'valido'
                ):

                    modelo_ocr = (

                        resultado_ocr[
                            'texto'
                        ]
                    )

                    lineas = modelo_ocr.splitlines()

                    lineas_normalizadas = []

                    for linea in lineas:

                        linea = linea.strip()

                        if not linea:

                            continue

                        try:

                            normalizada = (

                                MathNormalizerService
                                .normalizar_expresion(
                                    linea
                                )
                            )

                            lineas_normalizadas.append(
                                normalizada
                            )

                        except:

                            lineas_normalizadas.append(
                                linea
                            )

                    modelo_normalizado = "\n".join(
                        lineas_normalizadas
                    )

                    # ============================================
                    # PROCEDIMIENTO MODELO
                    # ============================================

                    procedimiento_modelo = []

                    ejercicios_modelo = (

                        ExerciseDetectorService
                        .detectar_ejercicios(

                            modelo_ocr
                        )
                    )

                    print(
                        "\n====================="
                    )

                    print(
                        "EJERCICIOS MODELO"
                    )

                    print(
                        "====================="
                    )

                    for i, ejercicio in enumerate(

                        ejercicios_modelo,

                        start=1
                    ):

                        print(
                            f"\nMODELO {i}"
                        )

                        print(
                            ejercicio
                        )

                        resultado_parser = (

                            MathProcedureParserService
                            .parsear_ejercicio(

                                ejercicio
                            )
                        )

                        procedimiento_modelo.append(
                            resultado_parser
                        )

                    print(
                        "\n====================="
                    )

                    print(
                        "PROCEDIMIENTO MODELO"
                    )

                    print(
                        procedimiento_modelo
                    )

                    print(
                        "\n=====================\n"
                    )

                    print(
                        "\n====================="
                    )

                    print(
                        "ANTES DE GUARDAR"
                    )

                    print(
                        procedimiento_modelo
                    )

                    print(
                        json.dumps(
                            procedimiento_modelo
                        )
                    )

                    print(
                        "=====================\n"
                    )
            # ============================================
            # CREAR EVALUACIÓN
            # ============================================

            nueva = Evaluacion(

                titulo=request.form['titulo'],

                descripcion=request.form['descripcion'],

                unidad=request.form['unidad'],

                fecha_evaluacion=request.form[
                    'fecha_evaluacion'
                ],
                procedimiento_modelo=

                    json.dumps(
                        procedimiento_modelo
                    ),

                grado_id=request.form[
                    'grado_id'
                ],

                docente_id=1,

                seccion_id=request.form[
                    'seccion_id'
                ],

                respuesta_modelo=
                    respuesta_modelo,

                ruta_modelo=
                    ruta_modelo,

                examen_modelo=
                    ruta_modelo,

                modelo_ocr=
                    modelo_ocr,

                modelo_normalizado=
                    modelo_normalizado
            )

            db.session.add(nueva)

            db.session.commit()

            flash(
                'Evaluación creada correctamente.',
                'success'
            )

            return redirect(
                url_for(
                    'evaluacion.listar_evaluaciones'
                )
            )

        except Exception as error:

            flash(str(error), 'danger')

    return render_template(

        'evaluaciones/crear.html',

        secciones=secciones
    )

# =====================================================
# DETALLE
# =====================================================

@evaluacion_bp.route('/detalle/<int:id>')
def detalle_evaluacion(id):

    evaluacion = (
        Evaluacion.query.get_or_404(id)
    )

    return render_template(

        'evaluaciones/detalle.html',

        evaluacion=evaluacion
    )