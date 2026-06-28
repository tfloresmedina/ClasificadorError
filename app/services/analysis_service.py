# =========================================================
# IMPORTS
# =========================================================
import json
from app.services.math_normalizer_service import (
    MathNormalizerService
)

from app.services.ast_validation_service import (
    ASTValidationService
)

from app.services.sympy_validation_service import (
    SympyValidationService
)

from app.services.error_classifier_service import (
    ErrorClassifierService
)

from app.services.variable_validation_service import (
    VariableValidationService
)

from app.services.ocr_math_extractor_service import (
    OCRMathExtractorService
)

from app.services.semantic_validation_service import (
    SemanticValidationService
)

from app.services.ocr_noise_detection_service import (
    OCRNoiseDetectionService
)

from app.services.ocr_autocorrect_service import (
    OCRAutoCorrectService
)

from app.services.confidence_score_service import (
    ConfidenceScoreService
)

from app.services.pipeline_trace_service import (
    PipelineTraceService
)

from app.services.logging_service import (
    LoggingService
)

from app.services.recommendation_engine_service import (
    RecommendationEngineService
)

from app.services.error_severity_service import (
    ErrorSeverityService
)

from app.services.topic_detection_service import (
    TopicDetectionService
)

from app.services.step_parser_service import (
    StepParserService
)

from app.services.difficulty_estimation_service import (
    DifficultyEstimationService
)

from app.services.step_estimation_service import (
    StepEstimationService
)

from app.services.mathematical_consistency_service import (
    MathematicalConsistencyService
)

from app.services.exercise_type_service import (
    ExerciseTypeService
)

from app.services.performance_metrics_service import (
    PerformanceMetricsService
)

from app.services.error_frequency_service import (
    ErrorFrequencyService
)

from app.services.student_performance_service import (
    StudentPerformanceService
)

from app.services.classroom_analytics_service import (
    ClassroomAnalyticsService
)

from app.services.risk_detection_service import (
    RiskDetectionService
)

from app.services.math_expression_extractor_service import (
    MathExpressionExtractorService
)

from app.services.math_content_detector_service import (
    MathContentDetectorService
)

from app.services.learning_trend_service import (
    LearningTrendService
)

from app.services.pedagogical_alert_service import (
    PedagogicalAlertService
)

from app.services.mathematical_profile_service import (
    MathematicalProfileService
)

from app.services.reinforcement_planning_service import (
    ReinforcementPlanningService
)

from app.services.report_summary_service import (
    ReportSummaryService
)

from app.services.result_consolidation_service import (
    ResultConsolidationService
)

from app.services.dashboard_data_service import (
    DashboardDataService
)

from app.services.competency_mapping_service import (
    CompetencyMappingService
)

from app.services.exercise_detector_service import (
    ExerciseDetectorService
)

from app.services.exercise_classifier import (
    ExerciseClassifier
)

from app.services.math_line_filter import (
    MathLineFilter
)

from app.services.math_step_filter import (
    MathStepFilter
)

from app.services.step_detector_service import (
    StepDetectorService
)

from app.services.math_metadata_service import (
    MathMetadataService
)
from app.services.math_procedure_parser_service import (
    MathProcedureParserService
)

from app.services.procedure_validation_service import (
    ProcedureValidationService
)

from app.services.model_comparison_service import (
    ModelComparisonService
)

from app.services.pedagogical_interpretation_service import (
    PedagogicalInterpretationService
)

from app.services.incomplete_equation_recovery_service import (
    IncompleteEquationRecoveryService
)
# =========================================================
# ANALYSIS SERVICE
# =========================================================

class AnalysisService:


    @staticmethod
    def analizar_respuesta(
        respuesta_ocr,
        respuesta_correcta,
        procedimiento_modelo_json=None,
        ejercicios_gemini=None
    ):


        # =====================================================
        # VALIDACIÓN OCR VACÍO
        # =====================================================

        if not respuesta_ocr:

            return {

                'valido': False,

                'correcto': False,

                'tipo_error':
                'ocr_vacio',

                'descripcion':
                'No se detectó contenido matemático.',

                'recomendacion':
                'Verificar calidad de imagen.',

                'nivel_confianza': 0,

                'etapa_error':
                'ocr'
            }


        # =====================================================
        # VALIDACIÓN TEXTO MUY CORTO
        # =====================================================

        if len(
            respuesta_ocr.strip()
        ) < 2:

            return {

                'valido': False,

                'correcto': False,

                'tipo_error':
                'ocr_insuficiente',

                'descripcion':
                'Contenido OCR insuficiente.',

                'recomendacion':
                'Subir imagen más clara.',

                'nivel_confianza': 0.2,

                'etapa_error':
                'ocr'
            }

        resultado_autocorreccion = (
            OCRAutoCorrectService.autocorregir(
                respuesta_ocr
            )
        )

        respuesta_ocr = (
            resultado_autocorreccion[
                'expresion_corregida'
            ]
        )

        # =====================================
        # FILTRO OCR
        # =====================================

        lineas_limpias = (

            MathLineFilter.filtrar(

                respuesta_ocr.splitlines()
            )
        )

        respuesta_ocr = "\n".join(
            lineas_limpias
        )


        # =====================================
        # DETECTOR DE CONTENIDO MATEMATICO
        # =====================================

        bloques_matematicos = (

            MathContentDetectorService
            .detectar(
                respuesta_ocr
            )
        )

        print(
            "\n====================="
        )

        print(
            "BLOQUES MATEMATICOS"
        )

        print(
            "====================="
        )

        for bloque in bloques_matematicos:

            print(
                bloque
            )

        texto_matematico = "\n".join(

            bloque["contenido"]

            for bloque in bloques_matematicos
        )

        print(
            "=====================\n"
        )


        print("\n=====================")
        print("OCR FILTRADO")
        
        expresiones = (

        MathExpressionExtractorService
        .extraer(
            respuesta_ocr
            )
        )

        print("\n=====================")
        print("EXPRESIONES DETECTADAS")
        print("=====================")

        for expr in expresiones:
            print(expr)

        print("=====================\n")

        print("=====================")
        print(respuesta_ocr)
        print("=====================\n")
        
        # =====================================
        # EXTRACCIÓN MATEMÁTICA
        # =====================================

       # lineas_matematicas = (

           # OCRMathExtractorService
        #    .extraer(
           #     respuesta_ocr
      #      )
       # )

       # print("\n=====================")
       # print("LINEAS MATEMATICAS")
       # print("=====================")
       # print(lineas_matematicas)
       # print("=====================\n")

       # texto_matematico = "\n".join(
       #     lineas_matematicas
       # )

        # =====================================
        # DETECCIÓN DE EJERCICIOS
        # =====================================
        print("\n=====================")
        print("TEXTO MATEMATICO FINAL")
        print("=====================")
        print(texto_matematico)
        print("=====================\n")

        if ejercicios_gemini:

            print(
                "\nUSANDO EJERCICIOS GEMINI\n"
            )

            ejercicios = ejercicios_gemini

        else:

            print(
                "\nUSANDO OCR CLÁSICO\n"
            )

            ejercicios = (

                ExerciseDetectorService
                .detectar_ejercicios(
                    respuesta_ocr
                )
            )
        
        for i, e in enumerate(
            ejercicios,
            start=1
        ):
            print(f"\nEJERCICIO {i}")
            print(e)

        print("=====================\n")

    


        # =====================================
        # NORMALIZAR MODELO JSON
        # =====================================

        if isinstance(
            procedimiento_modelo_json,
            str
        ):

            try:

                procedimiento_modelo_json = (

                    json.loads(
                        procedimiento_modelo_json
                    )
                )

            except Exception as e:

                print(
                    "ERROR JSON MODELO:",
                    e
                )

                procedimiento_modelo_json = []

        # =====================================
        # RECUPERACIÓN ECUACIONES INCOMPLETAS
        # =====================================
        print("\n====================")
        print("TIPO EJERCICIO")
        print("====================")
        print(type(ejercicios[0]))
        print("====================")
        if  not ejercicios_gemini:
                ejercicios = (

                    IncompleteEquationRecoveryService
                    .recuperar(

                        ejercicios,

                        procedimiento_modelo_json
                    )
                )
        print(
                    "\n====================="
                )

        print(
            "EJERCICIOS DETECTADOS"
        )

        print(
            "====================="
        )

        for i, ejercicio in enumerate(
            ejercicios,
            start=1
        ):

            print(
                f"\nEJERCICIO {i}"
            )

            print(
                ejercicio
            )

        print(
            "\n=====================\n"
        )


       # =====================================
# PARSER MATEMÁTICO
# =====================================
        print("\n====================")
        print("VERIFICANDO MODO IA")
        print("====================")

        es_modo_gemini = (

            ejercicios

            and isinstance(
                ejercicios[0],
                dict
            )
        )

        ejercicios_parseados = []

        if es_modo_gemini:

            print(
                "MODO GEMINI ACTIVADO"
            )

            for ejercicio in ejercicios:

                ejercicios_parseados.append({

                    "numero":
                        ejercicio.get(
                            "exercise_number"
                        ),

                    "enunciado":
                        ejercicio.get(
                            "problem_statement"
                        ),

                    "pasos":
                        ejercicio.get(
                            "solution_steps",
                            []
                        ),

                    "respuesta":
                        ejercicio.get(
                            "final_answer"
                        )
                })

        else:

            print(
                "MODO OCR CLÁSICO"
            )

            print(
                "\n====================="
            )

            print(
                "PARSER MATEMÁTICO"
            )

            print(
                "====================="
            )

            for i, ejercicio in enumerate(
                ejercicios,
                start=1
            ):

                if isinstance(
                    ejercicio,
                    list
                ):

                    ejercicio = "\n".join(
                        ejercicio
                    )

                if isinstance(
                    ejercicio,
                    str
                ):

                    ejercicio = (
                        ejercicio.splitlines()
                    )

                print("\n====================")
                print("EJERCICIO RECIBIDO")
                print("====================")
                print(ejercicio)

                resultado_parser = (

                    MathProcedureParserService
                    .parsear_ejercicio(
                        ejercicio
                    )
                )

                print("\n====================")
                print("RESULTADO PARSER")
                print("====================")
                print(resultado_parser)

                resultado_parser["pasos"] = (

                    MathStepFilter.filtrar(

                        resultado_parser.get(
                            "pasos",
                            []
                        )
                    )
                )

                ejercicios_parseados.append(
                    resultado_parser
                )

                print(
                    f"\nEJERCICIO PARSEADO {i}"
                )

                print(
                    resultado_parser
                )

                print(
                    "PASOS DETECTADOS:",
                    len(
                        resultado_parser.get(
                            "pasos",
                            []
                        )
                    )
                )

                print(
                    "\n=====================\n"
                )
        validaciones_procedimiento = []
        resultados_por_ejercicio = []
        print("\n====================")
        print("EJERCICIOS PARSEADOS FINALES")
        print("====================")

        for i, ejercicio in enumerate(
                ejercicios_parseados,
                start=1
            ):
            

            pasos = ejercicio.get(
                "pasos",
                []
            )

            print(
                ejercicio
            )

        

            print("====================\n")
            

            # =====================================
            # CLASIFICAR ANTES DE ANALIZAR
            # =====================================

            clasificacion = (

                ExerciseClassifier
                .clasificar(
                    pasos
                )
            )

            tipo_detectado = (
                clasificacion["tipo"]
            )

            analizable = (
                clasificacion["analizable"]
            )

            motivo = (
                clasificacion["motivo"]
            )

            # =====================================
            # SOLO ANALIZAR EJERCICIOS VÁLIDOS
            # =====================================

            if analizable:

                try:

                    resultado_validacion = (

                        ProcedureValidationService
                        .validar_pasos(
                            pasos
                        )
                    )

                except Exception as e:

                    print(
                        "ERROR VALIDACION PROCEDIMIENTO:",
                        str(e)
                    )

                    resultado_validacion = {

                        "valido": False,

                        "validaciones": [],

                        "motivo": str(e)
                    }

                validaciones_procedimiento.append(
                    resultado_validacion
                )

            else:

                resultado_validacion = {

                "valido": None,

                "motivo":
                    "ejercicio_un_paso",

                "descripcion":
                    "El ejercicio contiene una única operación matemática y no requiere validación de transformaciones."
            }

            
           
           

            # =====================================
            # EJERCICIOS NO ANALIZABLES
            # =====================================

            if not analizable:
                resultados_por_ejercicio.append({

                    "numero":
                        i,

                    "tipo":
                        tipo_detectado,

                    "analizable":
                        False,

                    "motivo":
                        motivo,

                    "cantidad_pasos":
                        len(pasos),

                    "valido":
                        None,

                    "validaciones":
                        [],

                    "pasos":
                        pasos,
                    "pregunta": 
                        None,
                    "respuesta": 
                    None

            })

            else:

                resultados_por_ejercicio.append({

                    "numero":
                        ejercicio.get(
                            "numero",
                            i
                        ),

                    "pregunta":
                        ejercicio.get(
                            "enunciado"
                        ),

                    "respuesta":
                        ejercicio.get(
                            "respuesta"
                        ),

                    "tipo":
                        tipo_detectado,

                    "analizable":
                        True,

                    "motivo":
                        None,

                    "cantidad_pasos":
                        len(pasos),

                    "valido":
                        resultado_validacion.get(
                            "valido",
                            False
                        ),

                    "validaciones":
                        resultado_validacion.get(
                            "validaciones",
                            []
                        ),

                    "pasos":
                        pasos

                })

            print(
                "\n====================="
            )

            print(
                f"EJERCICIO {i}"
            )

            print(
                resultados_por_ejercicio[-1]
            )

            print(
                "=====================\n"
            )
        
            print(
                "\n====================="
            )

            print(
                "RESUMEN VALIDACIONES"
            )

            print(
                "====================="
            )

            print(
                validaciones_procedimiento
            )

            print(
                "\n=====================\n"
            )

            print(
                "\n=====================\n"
            )
    

        cantidad_ejercicios = len(
            ejercicios_parseados
        )

        pasos_detectados = 0

        variables_detectadas = (

            MathMetadataService
            .obtener_variables(
                respuesta_ocr
            )
        )

        cantidad_variables = len(
            variables_detectadas
        )

        cantidad_ecuaciones = (

            MathMetadataService
            .contar_ecuaciones(
                respuesta_ocr
            )
        )

        cantidad_operaciones = (

            MathMetadataService
            .contar_operaciones(
                respuesta_ocr
            )
        )

        for ejercicio in ejercicios:

            pasos_detectados += (

                StepDetectorService
                .contar_pasos(
                    ejercicio
                )
            )

      
        # =====================================================
        # DETECCIÓN DE RUIDO OCR
        # =====================================================

        resultado_ruido = (

            OCRNoiseDetectionService
            .detectar_ruido(

                respuesta_ocr
            )
        )


        
        # =====================================================
        # NORMALIZACIÓN
        # =====================================================

        expresion_normalizada = (
         
            MathNormalizerService
            .normalizar_expresion(

                respuesta_ocr
            )
        )


        # =====================================================
        # VALIDACIÓN ESTRUCTURAL
        # =====================================================

       # estructura_valida = (

          #  ASTValidationService
         #   .expresion_valida(

           #     expresion_normalizada
          #  )
     #   )


       # if not estructura_valida:

         #   return {
#
            #    'valido': False,

              #  'tipo_error':
              #  'estructura_invalida',

              #  'descripcion':
              #  'La expresión contiene errores estructurales.',

              #  'expresion_normalizada':
            #    expresion_normalizada
                
          #  }
        estructura_valida = True
        # =====================================================
        # RESPUESTA CORRECTA
        # =====================================================

        tiene_respuesta_correcta = (

            respuesta_correcta is not None

                and

                str(
                    respuesta_correcta
                ).strip() != ''
            )

        # =====================================================
        # PROCEDIMIENTO MODELO
        # =====================================================

       # tiene_procedimiento_modelo = bool(
           # procedimiento_modelo_json
            #)
        tiene_procedimiento_modelo = False
        print(
           "\n====================="
        )

        print(
            "TIENE RESPUESTA CORRECTA:"
        )

        print(
            tiene_respuesta_correcta
        )

        print(
            "TIENE PROCEDIMIENTO MODELO:"
       )

        print(
           tiene_procedimiento_modelo
       )

        print(
            "=====================\n"
       )
        
        # =====================================================
        # VALIDACIÓN VARIABLES
        # =====================================================

        # =====================================
        # VALIDACIÓN VARIABLES
        # TEMPORALMENTE DESACTIVADA
        # =====================================

        variables_validas = True

        print(
            "\nVALIDACION VARIABLES DESACTIVADA\n"
        )


        if not variables_validas:

            return {

                'valido': False,

                'correcto': False,

                'tipo_error':
                'variables_invalidas',

                'descripcion':
                'Las variables detectadas no coinciden con el ejercicio.',

                'recomendacion':
                'Revisar variables algebraicas utilizadas.',

                'expresion_original':
                respuesta_ocr,

                'expresion_normalizada':
                expresion_normalizada,

                'nivel_confianza': 0.4,

                'etapa_error':
                'validacion_variables'
            }


        # =====================================================
        # VALIDACIÓN SEMÁNTICA
        # =====================================================

        resultado_semantico = (

            SemanticValidationService
            .validar_semantica(

                expresion_normalizada
            )
        )





        semantica_valida = True


        # =====================================================
        # CONSISTENCIA MATEMÁTICA
        # =====================================================

        consistencia = (

            MathematicalConsistencyService
            .validar_consistencia(

                expresion_normalizada
            )
        )


        


        # =====================================================
        # DETECCIÓN DE TEMA
        # =====================================================

        tema_matematico = (

            TopicDetectionService
            .detectar_tema(

                expresion_normalizada
            )
        )


        # =====================================================
        # TIPO DE EJERCICIO
        # =====================================================

        tipo_ejercicio = (

            ExerciseTypeService
            .detectar_tipo(

                expresion_normalizada
            )
        )

        # =====================================================
        # COMPETENCIA
        # =====================================================

        competencia = (

            CompetencyMappingService
            .obtener_competencia(

                tipo_ejercicio
            )
        )

        # =====================================================
        # DIFICULTAD
        # =====================================================

        dificultad = (

            DifficultyEstimationService
            .estimar_dificultad(

                expresion_normalizada
            )
        )


        # =====================================================
        # ESTIMACIÓN DE PASOS
        # =====================================================

        pasos_estimados = (

            StepEstimationService
            .estimar_pasos(

                expresion_normalizada
            )
        )


        # =====================================================
        # VALIDACIÓN ALGEBRAICA
        # =====================================================
        if tiene_respuesta_correcta:

            if tipo_ejercicio == "ecuacion":

                resultado_sympy = (

                    SympyValidationService
                    .validar_ecuaciones(

                        expresion_normalizada,

                        respuesta_correcta
                    )
                )

            elif tipo_ejercicio == "simplificacion":

                resultado_sympy = (

                    SympyValidationService
                    .validar_simplificacion(

                        expresion_normalizada,

                        respuesta_correcta
                    )
                )

            elif tipo_ejercicio == "aritmetico":

                resultado_sympy = (

                    SympyValidationService
                    .validar_operacion(

                        expresion_normalizada,

                        respuesta_correcta
                    )
                )

            else:

                resultado_sympy = (

                    SympyValidationService
                    .validar_equivalencia(

                        expresion_normalizada,

                        respuesta_correcta
                    )
                )

        else:

            resultado_sympy = {

                'valido': True,

                'equivalente': True,

                'expr1': None,

                'expr2': None
            }

            print(
                "\n====================="
            )

            print(
                "TIPO EJERCICIO"
            )

            print(
                tipo_ejercicio
            )

            print(
                resultado_sympy
            )

            print(
                "=====================\n"
            )
        # =====================================================
        # COMPARACIÓN CON MODELO
        # =====================================================

        comparacion_modelo = {

            "coincidencia": 0,

            "paso_error": None,

            "esperado": None,

            "obtenido": None,

            "tipo_error": None
        }

        if tiene_procedimiento_modelo:

            try:

                procedimiento_modelo = []

                if procedimiento_modelo_json:

                    try:

                        for ejercicio in procedimiento_modelo_json:

                            procedimiento_modelo.extend(

                                ejercicio.get(
                                    'pasos',
                                    []
                                )
                            )

                    except Exception as e:

                        print(
                            "ERROR CARGANDO MODELO:",
                            e
                        )

                elif respuesta_correcta:

                    procedimiento_modelo.append(

                        respuesta_correcta
                    )

                    procedimiento_alumno = []

                    for ejercicio in ejercicios_parseados:

                        procedimiento_alumno.extend(

                            ejercicio.get(
                                "pasos",
                                []
                            )
                        )

                        print("\n====================")
                        print("EJERCICIOS PARSEADOS")
                        print("====================")

                        print("\n====================")
                        print("EJERCICIOS RECIBIDOS IA")
                        print("====================")

                for i, ejercicio in enumerate(
                        ejercicios_parseados,
                        start=1
            ):
                    print(
                f"INDICE ACTUAL: {i}")

                    print(
                    f"TOTAL PARSEADOS: {len(ejercicios_parseados)}"
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
                    "\nPROCEDIMIENTO ALUMNO"
                )

                print(
                    procedimiento_alumno
                )

                print(
                    "=====================\n"
                )

                comparacion_modelo = (

                    ModelComparisonService
                    .comparar_procedimientos(

                        procedimiento_modelo,

                        procedimiento_alumno
                    )
                )

                print(
                    "\n====================="
                )

                print(
                    "COMPARACION MODELO"
                )
                print(
                    "PASO OK 1"
                )
                print(
                    comparacion_modelo
                )

                print(
                    "=====================\n"
                )

            except Exception as e:

                print(
                    "ERROR COMPARACION MODELO:",
                    e
                )

        # =====================================================
        # TRACE PIPELINE
        # =====================================================

        trace_pipeline = {
            "estado": "temporalmente_desactivado"
        }

        print(
            "PASO OK 2"
        )
        # =====================================================
        # SCORE GLOBAL
        # =====================================================

        score_global = (

            ConfidenceScoreService
            .calcular_score(

                confianza_ocr=90,

                ruido_detectado=

                    resultado_ruido[
                        'ruido_detectado'
                    ],

                autocorregido=

                    resultado_autocorreccion[
                        'corregido'
                    ],

                correcto=

                    resultado_sympy[
                        'equivalente'
                    ]
            )
        )

        print(
            "PASO OK 3"
        )
        # =====================================================
        # CLASIFICACIÓN ERROR
        # =====================================================

        hay_error_procedimiento = any(
            (
            not resultado.get(
                "valido",
                True
            )
        )

            and

            resultado.get(
                "motivo"
            )

            !=

            "insuficientes_pasos"

            for resultado in
            validaciones_procedimiento
        )

        if hay_error_procedimiento:

            clasificacion = (

                ErrorClassifierService
                .clasificar_error_procedimiento(

                    {
                        "valido": False
                    }
                )
            )
            print(
                "PASO OK 4"
            )
        elif tiene_procedimiento_modelo:

            clasificacion = {

                'tipo_error':

                    comparacion_modelo.get(
                        'tipo_error'
                    ),

                'descripcion':

                    'Desviación respecto al modelo.'

                    if comparacion_modelo.get(
                        'tipo_error'
                    )

                    else

                    'Sin errores detectados.',

                'fase_polya':
                    'Desarrollo'
            }

        else:

            clasificacion = {

                    'tipo_error': None,

                    'descripcion':
                        'Sin errores detectados.',

                    'fase_polya':
                        'Desarrollo'
        }
        # =====================================================
        # MÉTRICAS GENERALES
        # =====================================================

        metricas_generales = (

                PerformanceMetricsService
                .calcular_metricas(

             [
                    {
            'correcto':
            (
                resultado_sympy.get(
                    'equivalente',
                    False
                )
                and
                not hay_error_procedimiento
            ),
                    }
                ]
            )
        )


        # =====================================================
        # FRECUENCIA ERRORES
        # =====================================================

        frecuencia_errores = (

            ErrorFrequencyService
            .calcular_frecuencia(

                [
                    {
                        'tipo_error':

                            clasificacion.get(
                                'tipo_error'
                            )
                    }
                ]
            )
        )


        # =====================================================
        # RESUMEN ESTUDIANTE
        # =====================================================

        resumen_estudiante = (

            StudentPerformanceService
            .resumir_desempeno(

                nombre_estudiante=
                    'Estudiante',

                resultados=
                    [
                        {
                            'correcto':

                                resultado_sympy[
                                    'equivalente'
                                ]
                        }
                    ]
            )
        )


        # =====================================================
        # ANALÍTICA AULA
        # =====================================================

        analitica_aula = (

            ClassroomAnalyticsService
            .resumir_aula(

                [
                    resumen_estudiante
                ]
            )
        )


        # =====================================================
        # RIESGO
        # =====================================================

        coincidencia_modelo = (
            comparacion_modelo.get(
                "coincidencia",
                0
            )
        )

        if coincidencia_modelo >= 90:

            riesgo = "bajo"

        elif coincidencia_modelo >= 60:

            riesgo = "medio"

        else:

            riesgo = "alto"


        # =====================================================
        # TENDENCIA
        # =====================================================

        tendencia = (

            LearningTrendService
            .analizar_tendencia(

                [
                    50,

                    resumen_estudiante[
                        'porcentaje_acierto'
                    ]
                ]
            )
        )


        # =====================================================
        # ALERTAS
        # =====================================================

        alertas = (

            PedagogicalAlertService
            .generar_alertas(

                riesgo=
                    riesgo,

                tendencia=
                    tendencia
            )
        )


        # =====================================================
        # PERFIL MATEMÁTICO
        # =====================================================

        perfil = (

            MathematicalProfileService
            .construir_perfil(

                porcentaje_acierto=

                    resumen_estudiante[
                        'porcentaje_acierto'
                    ],

                errores_frecuentes=
                    frecuencia_errores,

                dificultad_promedio=
                    dificultad
            )
        )

        print(
            "PASO OK 5"
        )
        # =====================================================
        # PLAN REFUERZO
        # =====================================================

        plan_refuerzo = (

            ReinforcementPlanningService
            .generar_plan(

                debilidad=

                    perfil[
                        'debilidad'
                    ],

                riesgo=
                    riesgo
            )
        )


        # =====================================================
        # RESUMEN GENERAL
        # =====================================================

        resumen_general = (

            ReportSummaryService
            .generar_resumen(

                estudiante=
                    'Estudiante',

                porcentaje=

                    resumen_estudiante[
                        'porcentaje_acierto'
                    ],

                riesgo=
                    riesgo,

                tendencia=
                    tendencia
            )
        )


        # =====================================================
        # DASHBOARD
        # =====================================================

        dashboard = (

            DashboardDataService
            .preparar_dashboard(

                metricas=
                    metricas_generales,

                errores=
                    frecuencia_errores,

                perfil=
                    perfil
            )
        )


        # =====================================================
        # CONSOLIDACIÓN
        # =====================================================

        consolidado = (

            ResultConsolidationService
            .consolidar(

                analisis=
                    resumen_estudiante,

                metricas=
                    metricas_generales,

                errores=
                    frecuencia_errores,

                perfil=
                    perfil,

                alertas=
                    alertas,

                resumen=
                    resumen_general
            )
        )

        print("\n=====================")
        print("CORRECTO PARA PEDAGOGICO")
        print(resultado_sympy.get("equivalente"))
        print("=====================\n")

        # =====================================================
        # RESULTADO PEDAGÓGICO
        # =====================================================

        correcto_para_pedagogico = (
            resultado_sympy.get(
            "equivalente",
            False
            )

            and

            not hay_error_procedimiento
            )
    
        print("\n=====================")
        print("CORRECTO PARA PEDAGOGICO")
        print(correcto_para_pedagogico)
        print("=====================\n")


        resultado_pedagogico = (

            PedagogicalInterpretationService
            .interpretar(

                {

                   "correcto":
                correcto_para_pedagogico,

                    "tipo_error":

                        clasificacion.get(
                            "tipo_error"
                        ),

                    "competencia":
                        competencia,

                    "riesgo":
                        riesgo,

                    "dificultad":
                        dificultad,

                    "comparacion_modelo":
                        comparacion_modelo
                }
            )
        )
        print(
            "\n====================="
                )

        print(
            "RESULTADO PEDAGOGICO"
        )

        print(
            resultado_pedagogico
        )

        print(
            "=====================\n"
        )

        print(
            "PASO OK FINAL"
        )

        print("\n=====================")
        print("ERROR PROCEDIMIENTO")
        print("=====================")
        print(hay_error_procedimiento)
        print("=====================\n")
        # =====================================================
        # RESPUESTA FINAL
        # =====================================================

        return {
           
            'correcto':
            (
                resultado_sympy.get(
                    'equivalente',
                    False
                )
                and
                not hay_error_procedimiento
            ),

            'tipo_error':

                None

                if comparacion_modelo.get(
                    "coincidencia",
                    0
                ) >= 90

                else

                clasificacion.get(
                    'tipo_error'
                ),

                'descripcion':

                'Procedimiento matemático correcto.'

                if (
                    resultado_sympy.get(
                        'equivalente',
                        False
                    )
                    and
                    not hay_error_procedimiento
                )

                else

                'Se detectaron errores en el procedimiento.',



            'recomendacion':

                'Buen procedimiento matemático.'

                if (
                    resultado_sympy.get(
                        'equivalente',
                        False
                    )
                    and
                    not hay_error_procedimiento
                )

                else

                RecommendationEngineService
                .generar_recomendacion(

                    clasificacion.get(
                        'tipo_error'
                    )
                ),


            'tema_matematico':
            tema_matematico,

            'tipo_ejercicio':
            tipo_ejercicio,

            'variables_detectadas':
            variables_detectadas,

            'cantidad_variables':
            cantidad_variables,

            'cantidad_ecuaciones':
            cantidad_ecuaciones,

            'cantidad_operaciones':
            cantidad_operaciones,
            
            'ejercicios_detectados':
            cantidad_ejercicios,

            'resultado_pedagogico':
            resultado_pedagogico,

            'dificultad':
            dificultad,

            'pasos_estimados':

                pasos_detectados
                if pasos_detectados > 0

                else

                pasos_estimados,

            
                'severidad':

                    'baja'

                    if (
                        resultado_sympy.get(
                            'equivalente',
                            False
                        )
                        and
                        not hay_error_procedimiento
                    )

                    else

                    ErrorSeverityService
                    .obtener_severidad(

                        clasificacion.get(
                            'tipo_error'
                        )
                    ),

               'competencia':
                competencia,


            'fase_polya':

                'Verificación correcta'

                if resultado_sympy[
                    'equivalente'
                ]

                else

                clasificacion.get(
                    'fase_polya'
                ),

                
            'riesgo':
            riesgo,

            'tendencia':
            tendencia,

            'alertas':
            alertas,

            'perfil_matematico':
            perfil,

            'plan_refuerzo':
            plan_refuerzo,

            'metricas_generales':
            metricas_generales,

            'frecuencia_errores':
            frecuencia_errores,

            'resumen_estudiante':
            resumen_estudiante,

            'analitica_aula':
            analitica_aula,

            'dashboard':
            dashboard,

            'consolidado':
            consolidado,

            'trace_pipeline':
            trace_pipeline,

            'resultados_por_ejercicio':
            resultados_por_ejercicio,

            'validaciones_procedimiento':
            validaciones_procedimiento,

            'comparacion_modelo':
            comparacion_modelo,

            'resultado_pedagogico':
             resultado_pedagogico,

            'score_global':
            score_global,

            'ruido_ocr':
            resultado_ruido,

            'autocorreccion_ocr':
            resultado_autocorreccion,

            'expresion_original':
            respuesta_ocr,

            'expresion_normalizada':
            expresion_normalizada,

            'expresion_sympy': {

                'expr1':
                resultado_sympy.get(
                    'expr1'
                ),

                'expr2':
                resultado_sympy.get(
                    'expr2'
                )
            },

                'nivel_confianza':

                1.0

                if (
                    resultado_sympy.get(
                        'equivalente',
                        False
                    )
                    and
                    not hay_error_procedimiento
                )

                else

                0.50,

           

            'etapa_error':

                None

                if resultado_sympy[
                    'equivalente'
                ]

                else

                'validacion_algebraica'


      }
