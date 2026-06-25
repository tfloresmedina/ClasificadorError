from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file
)
from flask import jsonify
import json
from app.services.analysis_service import (
    AnalysisService
)
from app.services.save_analysis_service import (
    SaveAnalysisService
)
from app.services.history_service import (
    HistoryService
)
from app.services.ocr_service import (
    OCRService
)
from app.services.gemini_ocr_service import (
    GeminiOCRService
)
from app.services.image_preprocessing_service import (
    ImagePreprocessingService
)
from app.services.pipeline_trace_service import (
    PipelineTraceService
)
from app.services.academic_profile_service import (
    AcademicProfileService
)
from app.services.academic_alert_service import (
    AcademicAlertService
)
from app.services.result_detail_service import (
    ResultDetailService
)
from app.services.pdf_report_service import (
    PDFReportService
)
from flask_login import (
    login_required
)
from app.services.role_required_service import (
    role_required
)
from app.services.student_result_service import (
    StudentResultService
)
from app.models.evaluacion import Evaluacion
from app.models.examen_alumno import ExamenAlumno
from app.models.respuesta_alumno import RespuestaAlumno
from app.database.connection import db
from datetime import datetime
from app.models.ejercicio import Ejercicio
from app.models.resultado_analisis import ResultadoAnalisis
from app.services.gemini_exam_service import (
    GeminiExamService
)

# =========================================================
# BLUEPRINT
# =========================================================

resultados_bp = Blueprint(
    'resultados',
    __name__,
    url_prefix='/resultados'
)


# =========================================================
# VISTA PRINCIPAL
# =========================================================

@resultados_bp.route(
    '/analizar',
    methods=['GET']
)
@role_required(
    'administrador',
    'docente'
)
def vista_analisis():

    evaluaciones = Evaluacion.query.all()

    evaluacion_id = request.args.get('evaluacion_id')

    evaluacion = None
    estudiantes = []
    analisis_por_estudiante = {}

    if evaluacion_id:

        evaluacion = Evaluacion.query.get(evaluacion_id)

        if evaluacion:
            estudiantes = evaluacion.seccion.estudiantes

    # =====================================
    # VALIDAR ANÁLISIS EXISTENTE
    # =====================================

    for estudiante in estudiantes:

        resultado = (
            ExamenAlumno.query
            .filter_by(
                evaluacion_id=evaluacion.id,
                estudiante_id=estudiante.id
            )
            .order_by(ExamenAlumno.id.desc())
            .first()
        )

        print(
            estudiante.id,
            resultado.estado if resultado else "SIN_RESULTADO"
        )

        analizado = (
            resultado is not None
            and resultado.estado == 'analizado'
        )

        resultado_bd = (
            ResultadoAnalisis.query
            .join(
                RespuestaAlumno,
                ResultadoAnalisis.respuesta_alumno_id == RespuestaAlumno.id
            )
            .join(
                ExamenAlumno,
                RespuestaAlumno.examen_alumno_id == ExamenAlumno.id
            )
            .filter(
                ExamenAlumno.estudiante_id == estudiante.id,
                ExamenAlumno.evaluacion_id == evaluacion.id
            )
            .order_by(ResultadoAnalisis.id.desc())
            .first()
        )

        respuesta = None
        resultado_final = resultado_bd

        if resultado:
            respuesta = RespuestaAlumno.query.filter_by(
                examen_alumno_id=resultado.id
            ).first()

        analisis_por_estudiante[estudiante.id] = {

            'estudiante_id': estudiante.id,

            'nombre': estudiante.nombre_completo(),

            'analizado': analizado,

            # =====================================================
            # OCR
            # =====================================================
            'texto_ocr': respuesta.texto_ocr if respuesta else '',

            # =====================================================
            # EXPRESIONES
            # =====================================================
            'expresion_original': (
                getattr(resultado_final, 'expresion_original', '')
                if resultado_final else ''
            ),

            'expresion_normalizada': (
                getattr(resultado_final, 'expresion_normalizada', '')
                if resultado_final else ''
            ),

            # =====================================================
            # PROCEDIMIENTO
            # =====================================================
            'detalle_procedimiento': (
                getattr(resultado_final, 'detalle_procedimiento', [])
                if resultado else []
            ),

            # =====================================
            # PEDAGÓGICO
            # =====================================
            'error': getattr(resultado, 'tipo_error', 'Sin error'),

            'competencia': getattr(resultado, 'competencia', 'No definida'),

            'capacidad': getattr(resultado, 'capacidad_curricular', 'No definida'),

            'desempeno': getattr(resultado, 'desempeno_curricular', 'No definido'),

            'nivel_logro': getattr(resultado, 'nivel_logro', 'No definido'),

            'perfil_matematico': getattr(resultado, 'perfil_matematico', 'No definido'),

            'riesgo': getattr(resultado, 'riesgo_academico', 'Bajo'),

            'observacion': getattr(resultado, 'observaciones', ''),

            'recomendacion': getattr(resultado, 'recomendacion', ''),

            'recomendacion_curricular': getattr(resultado, 'recomendacion_curricular', ''),

            # =====================================================
            # MODELO
            # =====================================================
            'coincidencia_modelo': (
                getattr(resultado_final, 'coincidencia_modelo', 0)
                if resultado_final else 0
            ),

            'paso_error_modelo': (
                getattr(resultado_final, 'paso_error_modelo', '')
                if resultado_final else ''
            ),

            # =====================================================
            # MÉTRICAS
            # =====================================================
            'porcentaje': (
                getattr(resultado_final, 'porcentaje_coincidencia', 0)
                if resultado_final else 0
            ),
        }

    return render_template(
        'resultados/analizar.html',
        evaluacion=evaluacion,
        evaluacion_id=evaluacion_id,
        estudiantes=estudiantes,
        evaluaciones=evaluaciones,
        analisis_por_estudiante=analisis_por_estudiante
    )


# =========================================================
# PROCESAR ANÁLISIS
# =========================================================

@resultados_bp.route(
    '/procesar',
    methods=['POST']
)
@role_required(
    'administrador',
    'docente'
)
def procesar_analisis():

    print("ENTRO A PROCESAR_ANALISIS")

    try:

        evaluacion_id = request.form.get('evaluacion_id')
        estudiante_id = request.form.get('estudiante_id')

        print("EVALUACION:", evaluacion_id)
        print("ESTUDIANTE:", estudiante_id)

        # =================================================
        # OCR DESDE IMAGEN
        # =================================================

        imagen = request.files.get('imagen_examen')
        print("ARCHIVO:", imagen)
        respuesta_ocr = ''

        if imagen and imagen.filename:

            ruta_imagen = f'uploads/{imagen.filename}'

            import os

            os.makedirs('uploads', exist_ok=True)
            os.makedirs('uploads/procesadas', exist_ok=True)
            os.makedirs('uploads/ocr', exist_ok=True)

            imagen.save(ruta_imagen)

        # =============================================
        # DETECTAR PDF O IMAGEN
        # =============================================

        import os

        extension = os.path.splitext(ruta_imagen)[1].lower()

        if extension == ".pdf":

            print("PDF DETECTADO")

            resultado_ocr = OCRService.extraer_texto(ruta_imagen)

        else:

            resultado_preprocesamiento = (
                ImagePreprocessingService.preprocessar_imagen(ruta_imagen)
            )

            print(resultado_preprocesamiento)

            if not resultado_preprocesamiento.get('valido'):

                flash('Error durante el preprocesamiento.', 'danger')

                return redirect(
                    url_for(
                        'resultados.vista_analisis',
                        evaluacion_id=evaluacion_id
                    )
                )

            ruta_procesada = resultado_preprocesamiento.get('ruta_procesada')

        print("\n=====================")
        print("USANDO GEMINI OCR")

        archivo_para_ocr = (
            ruta_procesada
            if 'ruta_procesada' in locals()
            else ruta_imagen
        )

        resultado_ocr = GeminiOCRService.extraer_texto(archivo_para_ocr)

        if not resultado_ocr.get("valido", False):

            print("\nGemini falló.")
            print("Usando EasyOCR...")

            resultado_ocr = OCRService.extraer_texto(archivo_para_ocr)

            print("\n====================")
            print("RESULTADO OCR GEMINI")
            print("====================")
            print(resultado_ocr.keys())

        # =============================================
        # OCR
        # =============================================

        print("RESULTADO OCR COMPLETO:")
        print(resultado_ocr)

        if resultado_ocr and resultado_ocr.get('valido', False):

            respuesta_ocr = resultado_ocr.get('texto', '')

            resultado_gemini = {
                "valido": False,
                "ejercicios": []
            }

            try:
                print("\n====================")
                print("ARCHIVO GEMINI")
                print("====================")
                print(archivo_para_ocr)
                print("====================")

                resultado_gemini = GeminiExamService.extraer_ejercicios(
                    archivo_para_ocr
                )

                print("\n====================")
                print("RESULTADO GEMINI")
                print("====================")
                print(resultado_gemini)
                print("====================")

            except Exception as e:
                print("ERROR GEMINI:", str(e))

            print("\n================================")
            print("OCR EXTRAIDO")
            print("================================")
            print(respuesta_ocr)
            print("================================\n")

        else:

            print("OCR INVALIDO")
            print(resultado_ocr)

            flash('Error durante el OCR.', 'danger')

            return redirect(
                url_for(
                    'resultados.vista_analisis',
                    evaluacion_id=evaluacion_id
                )
            )

        # =================================================
        # CONTEXTO ACADÉMICO
        # =================================================

        estudiante_id = request.form.get('estudiante_id')

        evaluacion = Evaluacion.query.get(evaluacion_id)

        respuesta_correcta = None

        # =================================================
        # RESOLUCIÓN MODELO
        # =================================================

        if getattr(evaluacion, 'respuesta_modelo', None):
            respuesta_correcta = evaluacion.respuesta_modelo

        if not respuesta_ocr:

            flash('No se pudo detectar contenido matemático.', 'danger')

            return redirect(
                url_for(
                    'resultados.vista_analisis',
                    evaluacion_id=evaluacion_id
                )
            )

        # =================================================
        # VALIDAR ANÁLISIS PREVIO
        # =================================================

        examen_existente = ExamenAlumno.query.filter_by(
            evaluacion_id=evaluacion_id,
            estudiante_id=estudiante_id,
            estado='analizado'
        ).first()

        if examen_existente:

            flash(
                'Este estudiante ya posee un examen analizado para esta evaluación.',
                'warning'
            )

            return redirect(
                url_for(
                    'resultados.vista_analisis',
                    evaluacion_id=evaluacion_id
                )
            )

        # =================================================
        # CREAR EXAMEN ALUMNO
        # =================================================

        nuevo_examen = ExamenAlumno(
            estudiante_id=int(estudiante_id),
            evaluacion_id=int(evaluacion_id),
            estado='procesando',
            porcentaje_analisis=0,
            ruta_imagen=ruta_imagen,
            texto_ocr=respuesta_ocr,
            precision_ocr=90,
            estado_ocr='procesado'
        )

        db.session.add(nuevo_examen)
        db.session.commit()

        print("EXAMEN CREADO:", nuevo_examen.id)
        print("\n=====================")
        print("MODELO EVALUACION")
        print("modelo_ocr:", bool(evaluacion.modelo_ocr))
        print("modelo_normalizado:", bool(evaluacion.modelo_normalizado))
        print("procedimiento_modelo:", bool(evaluacion.procedimiento_modelo))
        print(evaluacion.procedimiento_modelo)
        print("=====================\n")

        # =================================================
        # EJECUTAR ANÁLISIS
        # =================================================

        try:

            print("\n====================")
            print("EJERCICIOS GEMINI")
            print("====================")

            if resultado_gemini:

                print(
                    resultado_gemini.get(
                        "ejercicios"
                    )
                )

            print("====================")
            resultado = AnalysisService.analizar_respuesta(
                respuesta_ocr=respuesta_ocr,
                respuesta_correcta=respuesta_correcta,
                procedimiento_modelo_json=evaluacion.procedimiento_modelo,
                ejercicios_gemini=resultado_gemini.get("ejercicios")
            )

        except Exception as e:

            print("ERROR ANALYSIS SERVICE:", str(e))

            import traceback
            traceback.print_exc()

            resultado = {
                "correcto": False,
                "tipo_error": "error_analisis",
                "descripcion": str(e),
                "recomendacion": "Revisar OCR",
                "score_global": 0,
                "resultado_pedagogico": {},
                "comparacion_modelo": {},
                "validaciones_procedimiento": [],
                "resultados_por_ejercicio": []
            }

        # =============================================
        # TRACE PIPELINE
        # =============================================

        trace_pipeline = PipelineTraceService.generar_trace(
            resultado_ocr=resultado_ocr,
            resultado_final=resultado
        )

        # =============================================
        # PERFIL ACADÉMICO
        # =============================================

        perfil_academico = AcademicProfileService.generar_perfil(resultado)

        # =============================================
        # ALERTAS ACADÉMICAS
        # =============================================

        alertas_academicas = AcademicAlertService.generar_alertas(
            resultado=resultado,
            perfil_academico=perfil_academico
        )

        # =================================================
        # OBTENER EJERCICIO DE LA EVALUACIÓN
        # =================================================

        ejercicio = Ejercicio.query.filter_by(
            evaluacion_id=evaluacion_id
        ).first()

        # =================================================
        # VALIDAR MODO DE ANÁLISIS
        # =================================================

        modelo = evaluacion.procedimiento_modelo

        if modelo is None:
            tiene_modelo = False
        elif isinstance(modelo, str):
            tiene_modelo = modelo.strip() not in ["", "[]", "{}"]
        elif isinstance(modelo, (list, dict)):
            tiene_modelo = len(modelo) > 0
        else:
            tiene_modelo = bool(modelo)

        if tiene_modelo:
            print(
                "\n\n================================"
                "\nMODO COMPARACIÓN CON MODELO"
                "\nProcedimiento modelo detectado"
                "\n================================\n\n"
            )
        else:
            print(
                "\n\n================================"
                "\nMODO OCR AUTÓNOMO ACTIVADO"
                "\nNo existe procedimiento modelo"
                "\n================================\n\n"
            )

        # =================================================
        # CREAR RESPUESTA ALUMNO
        # =================================================

        nueva_respuesta = RespuestaAlumno(
            imagen_respuesta=ruta_imagen,
            texto_ocr=respuesta_ocr,
            expresion_detectada=respuesta_ocr,
            expresion_normalizada=str(
                resultado.get('expresion_normalizada', '')
            ),
            estado_ocr='procesado',
            precision_ocr=90,
            observaciones_ocr=None,
            ejercicio_id=(ejercicio.id if ejercicio else None),
            examen_alumno_id=nuevo_examen.id
        )

        db.session.add(nueva_respuesta)
        db.session.commit()

        # =================================================
        # GUARDAR RESULTADO
        # =================================================

        print("GUARDANDO RESULTADO...")
        print("\n======================")
        print("RESULTADOS POR EJERCICIO")
        print("======================")
        print(resultado.get("resultados_por_ejercicio", []))
        print("======================")

        SaveAnalysisService.guardar_resultado(
            respuesta_alumno_id=nueva_respuesta.id,
            resultado=resultado
        )

        print("RESULTADO GUARDADO")
        print("CAMBIANDO ESTADO")

        nuevo_examen.estado = 'analizado'
        db.session.commit()

        print("ESTADO ACTUAL:", nuevo_examen.estado)

        nuevo_examen.estado = 'analizado'
        nuevo_examen.porcentaje_analisis = 100
        nuevo_examen.fecha_procesamiento = datetime.utcnow()

        db.session.commit()

        # =================================================
        # MOSTRAR RESULTADO
        # =================================================

        flash('Análisis realizado correctamente.', 'success')

        return redirect(
            url_for(
                'resultados.vista_analisis',
                evaluacion_id=evaluacion_id
            )
        )

    except Exception as e:

        print("\n")
        print("================================")
        print("ERROR PROCESAR_ANALISIS")
        print(type(e))
        print(str(e))
        print("================================")
        print("\n")

        db.session.rollback()

        flash(
            "No fue posible analizar el examen. "
            "Verifique que la imagen sea legible y que la evaluación tenga ejercicios registrados.",
            "danger"
        )

    return redirect(
        url_for(
            'resultados.vista_analisis',
            evaluacion_id=evaluacion_id
        )
    )


# =========================================================
# HISTORIAL ACADÉMICO
# =========================================================

@resultados_bp.route(
    '/historial',
    methods=['GET']
)
@role_required(
    'administrador',
    'docente'
)
def historial_resultados():

    historial = HistoryService.obtener_historial()

    return render_template(
        'resultados/historial.html',
        historial=historial
    )


# =========================================================
# DETALLE RESULTADO
# =========================================================

@resultados_bp.route(
    '/detalle/<int:resultado_id>',
    methods=['GET']
)
@role_required(
    'administrador',
    'docente'
)
def detalle_resultado(resultado_id):

    resultado = ResultDetailService.obtener_resultado(resultado_id)

    if not resultado:

        flash('Resultado no encontrado.', 'danger')

        return redirect(
            url_for('resultados.historial_resultados')
        )

    import json

    # ==========================================
    # CONVERTIR JSON PROCEDIMIENTO
    # ==========================================

    if resultado.detalle_procedimiento:
        resultado.detalle_procedimiento = json.loads(
            resultado.detalle_procedimiento
        )

    # ==========================================
    # TRACE PIPELINE
    # ==========================================

    trace_pipeline = PipelineTraceService.generar_trace(
        resultado_ocr={},
        resultado_final={}
    )

    # ==========================================
    # PERFIL ACADÉMICO
    # ==========================================

    perfil_academico = AcademicProfileService.generar_perfil(
        {
            'score_global': resultado.porcentaje_coincidencia,
            'riesgo': resultado.riesgo_academico
        }
    )

    # ==========================================
    # ALERTAS ACADÉMICAS
    # ==========================================

    alertas_academicas = AcademicAlertService.generar_alertas(
        resultado={
            'riesgo': resultado.riesgo_academico,
            'score_global': resultado.porcentaje_coincidencia
        },
        perfil_academico=perfil_academico
    )

    return render_template(
        'resultados/resultado.html',
        resultado=resultado,
        trace_pipeline=trace_pipeline,
        perfil_academico=perfil_academico,
        alertas_academicas=alertas_academicas,
        texto_ocr=resultado.expresion_original
    )


# =========================================================
# GENERAR PDF
# =========================================================

@resultados_bp.route(
    '/pdf/<int:resultado_id>',
    methods=['GET']
)
@role_required(
    'administrador',
    'docente'
)
def generar_pdf(resultado_id):

    resultado = ResultDetailService.obtener_resultado(resultado_id)

    if not resultado:

        flash('Resultado no encontrado.', 'danger')

        return redirect(
            url_for('resultados.historial_resultados')
        )

    import os

    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'reportes')
    )

    os.makedirs(base_dir, exist_ok=True)

    ruta_pdf = os.path.join(base_dir, f'reporte_{resultado.id}.pdf')

    PDFReportService.generar_reporte(
        resultado=resultado,
        ruta_pdf=ruta_pdf
    )

    return send_file(
        ruta_pdf,
        as_attachment=True,
        download_name=f'reporte_alumno_{resultado.id}.pdf'
    )


# =========================================================
# MIS RESULTADOS
# =========================================================

@resultados_bp.route(
    '/mis-resultados',
    methods=['GET']
)
@login_required
@role_required(
    'administrador',
    'estudiante'
)
def mis_resultados():

    resultados = StudentResultService.obtener_resultados_estudiante()

    return render_template(
        'resultados/mis_resultados.html',
        resultados=resultados
    )


@resultados_bp.route(
    '/obtener_resultado/<int:estudiante_id>/<int:evaluacion_id>'
)
@login_required
def obtener_resultado(estudiante_id, evaluacion_id):

    examen = (
        ExamenAlumno.query
        .filter_by(
            estudiante_id=estudiante_id,
            evaluacion_id=evaluacion_id
        )
        .order_by(ExamenAlumno.id.desc())
        .first()
    )

    if not examen:
        return jsonify({'success': False, 'message': 'Sin examen'})

    respuesta = RespuestaAlumno.query.filter_by(
        examen_alumno_id=examen.id
    ).first()

    if not respuesta:
        return jsonify({'success': False, 'message': 'Sin respuesta'})

    resultado = ResultadoAnalisis.query.filter_by(
        respuesta_alumno_id=respuesta.id
    ).first()

    if not resultado:
        return jsonify({'success': False, 'message': 'Sin análisis'})

    import json

    procedimiento = []

    try:

        if resultado.detalle_procedimiento:

            print("\n======================")
            print("DETALLE PROCEDIMIENTO")
            print("======================")
            print(resultado.detalle_procedimiento)
            print("======================")

            procedimiento = json.loads(resultado.detalle_procedimiento)

            print("\n======================")
            print("PROCEDIMIENTO DECODIFICADO")
            print("======================")

            for item in procedimiento:

                print(item)

            print("======================")

    except Exception as e:

        print("ERROR JSON PROCEDIMIENTO:", e)
        procedimiento = []

    # =====================================
    # CONSERVAR ESTRUCTURA POR EJERCICIO
    # =====================================

    timeline_limpio = procedimiento
    print("\n======================")
    print("JSON FINAL")
    print("======================")

    for item in timeline_limpio:

        print(item)

    print("======================")
    return jsonify({

        'success': True,

        # =====================================
        # OCR
        # =====================================
        'ocr': respuesta.texto_ocr or '',

        # =====================================
        # EXPRESIONES
        # =====================================
        'expresion': getattr(resultado, 'expresion_original', ''),

        # IMPORTANTE:
        # TU MODELO NO TIENE expresion_normalizada
        'expresion_normalizada': getattr(respuesta, 'expresion_normalizada', ''),

        # =====================================
        # PEDAGÓGICO
        # =====================================
        'error': getattr(resultado, 'tipo_error', 'Sin error'),

        'competencia': getattr(resultado, 'competencia', 'No definida'),

        'capacidad': getattr(resultado, 'capacidad_curricular', 'No definida'),

        'desempeno': getattr(resultado, 'desempeno_curricular', 'No definido'),

        'nivel_logro': getattr(resultado, 'nivel_logro', 'No definido'),

        'observacion': getattr(resultado, 'observaciones', ''),

        'recomendacion': getattr(resultado, 'recomendacion', ''),

        'recomendacion_curricular': getattr(resultado, 'recomendacion_curricular', ''),

        'perfil': getattr(resultado, 'perfil_matematico', 'No definido'),

        'riesgo': getattr(resultado, 'riesgo_academico', 'Bajo'),

        # =====================================
        # MODELO
        # =====================================
        'coincidencia': getattr(resultado, 'coincidencia_modelo', 0),

        'ejercicios': timeline_limpio,

        'procedimiento': timeline_limpio,

        'timeline': timeline_limpio,
    })