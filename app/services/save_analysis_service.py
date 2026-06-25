import json

from app.database.connection import db

from app.models.resultado_analisis import (
    ResultadoAnalisis
)
import json

class SaveAnalysisService:


    @staticmethod
    def guardar_resultado(


        respuesta_alumno_id,

        resultado
    ):


        nuevo_resultado = (

            ResultadoAnalisis(

                expresion_original=

                    resultado.get(
                        'expresion_original'
                    ),

                expresion_procesada=

                    resultado.get(
                        'expresion_normalizada'
                    ),

                expresion_sympy=

                    str(
                        resultado.get(
                            'expresion_sympy'
                        )
                    ),

                es_correcto=

                    resultado.get(
                        'correcto'
                    ),

                porcentaje_coincidencia=

                    resultado.get(
                        'score_global',
                        0
                    ),

                tipo_error=

                    resultado.get(
                        'tipo_error'
                    ),

                severidad_error=

                    resultado.get(
                        'severidad'
                    ),

                descripcion_error=

                    resultado.get(
                        'descripcion'
                    ),

                recomendacion=

                    resultado.get(
                        'recomendacion'
                    ),

                nivel_confianza=

                    resultado.get(
                        'nivel_confianza',
                        0
                    ),

                estado_analisis='procesado',

                tema_matematico=

                    resultado.get(
                        'tema_matematico'
                    ),

                tipo_ejercicio=

                    resultado.get(
                        'tipo_ejercicio'
                    ),

                dificultad=

                    resultado.get(
                        'dificultad'
                    ),

                pasos_estimados=

                    resultado.get(
                        'pasos_estimados',
                        0
                    ),

                riesgo_academico=

                    resultado.get(
                        'riesgo'
                    ),

                tendencia_aprendizaje=

                    resultado.get(
                        'tendencia'
                    ),

                perfil_matematico=

                    str(
                        resultado.get(
                            'perfil_matematico'
                        )
                    ),

                # =====================================================
                # INTERPRETACIÓN CURRICULAR
                # =====================================================

                competencia=

                    resultado.get(
                        'resultado_pedagogico',
                        {}
                    ).get(
                        'competencia'
                    ),
                capacidad_curricular=

                    resultado.get(
                        'resultado_pedagogico',
                        {}
                    ).get(
                        'capacidad'
                    ),

                desempeno_curricular=

                    resultado.get(
                        'resultado_pedagogico',
                        {}
                    ).get(
                        'desempeno'
                    ),

                nivel_logro=

                    resultado.get(
                        'resultado_pedagogico',
                        {}
                    ).get(
                        'nivel_logro'
                    ),

                recomendacion_curricular=

                    resultado.get(
                        'resultado_pedagogico',
                        {}
                    ).get(
                        'recomendacion'
                    ),



                ruido_ocr=

                    resultado.get(
                        'ruido_ocr',
                        {}
                    ).get(
                        'ruido_detectado',
                        False
                    ),

                autocorreccion_aplicada=

                    resultado.get(
                        'autocorreccion_ocr',
                        {}
                    ).get(
                        'corregido',
                        False
                    ),
                detalle_procedimiento=
                json.dumps(
                    resultado.get(
                        'resultados_por_ejercicio',
                        []
                    )
                ),

                # =====================================================
                # COMPARACIÓN MODELO
                # =====================================================

                coincidencia_modelo=

                    resultado.get(
                        'comparacion_modelo',
                        {}
                    ).get(
                        'coincidencia',
                        0
                    ),

                paso_error_modelo=

                    resultado.get(
                        'comparacion_modelo',
                        {}
                    ).get(
                        'paso_error'
                    ),


                # =====================================================
                # PROCEDIMIENTO DETECTADO
                # =====================================================

                procedimiento_detectado=

                    json.dumps(

                        resultado.get(
                            'validaciones_procedimiento',
                            []
                        )
                    ),


                respuesta_alumno_id=
                    respuesta_alumno_id
            )
        )


        db.session.add(

            nuevo_resultado
        )


        db.session.commit()


        return nuevo_resultado
    
    