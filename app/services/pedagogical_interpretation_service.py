from app.services.rules.curricular_rules import (
    CURRICULAR_RULES
)


class PedagogicalInterpretationService:

    @staticmethod
    def interpretar(resultado):

        tipo_error = resultado.get(
            "tipo_error"
        )

        riesgo = resultado.get(
            "riesgo"
        )

        dificultad = resultado.get(
            "dificultad"
        )

        comparacion_modelo = resultado.get(
            "comparacion_modelo",
            {}
        )

        # ==========================================
        # EJERCICIO CORRECTO
        # ==========================================

        if resultado.get("correcto"):

            coincidencia = 0

            if comparacion_modelo:

                coincidencia = (
                    comparacion_modelo.get(
                        "coincidencia",
                        0
                    )
                )

            interpretacion = (
                CURRICULAR_RULES[
                    "sin_error"
                ]
            ).copy()

            # --------------------------------------
            # MISMO MÉTODO DEL DOCENTE
            # --------------------------------------

            if coincidencia >= 80:

                interpretacion[
                    "nivel_logro"
                ] = "Logrado"

                interpretacion[
                    "observacion"
                ] = (
                    "El estudiante resolvió correctamente el ejercicio siguiendo una estrategia equivalente a la resolución modelo."
                )

                interpretacion[
                    "perfil_matematico"
                ] = (
                    "Demuestra dominio adecuado de los procedimientos matemáticos."
                )

                interpretacion[
                    "fortalezas"
                ] = [
                    "Mantiene equivalencia matemática.",
                    "Aplica correctamente procedimientos algebraicos.",
                    "Resuelve siguiendo una secuencia coherente."
                ]

            # --------------------------------------
            # MÉTODO DIFERENTE PERO CORRECTO
            # --------------------------------------

            else:

                interpretacion[
                    "nivel_logro"
                ] = "Logrado"

                interpretacion[
                    "observacion"
                ] = (
                    "El estudiante resolvió correctamente el ejercicio utilizando una estrategia alternativa a la resolución modelo."
                )

                interpretacion[
                    "perfil_matematico"
                ] = (
                    "Demuestra autonomía para resolver problemas mediante procedimientos propios matemáticamente válidos."
                )

                interpretacion[
                    "fortalezas"
                ] = [
                    "Propone estrategias propias.",
                    "Mantiene validez matemática.",
                    "Obtiene resultados correctos."
                ]

        else:

            interpretacion = (

                CURRICULAR_RULES.get(

                    tipo_error,

                    CURRICULAR_RULES.get(
                        "tipo_desconocido"
                    )

                )

            ).copy()
        # ==========================================
        # ALERTA DOCENTE
        # ==========================================

        if riesgo == "alto":

            interpretacion[
                "alerta_docente"
            ] = (

                "Se recomienda seguimiento personalizado debido al riesgo académico identificado."
            )

        elif riesgo == "medio":

            interpretacion[
                "alerta_docente"
            ] = (

                "Se recomienda monitoreo periódico del desempeño matemático."
            )

        # ==========================================
        # COMPLEJIDAD DEL EJERCICIO
        # ==========================================

        if dificultad == "alta":

            interpretacion[
                "complejidad"
            ] = (

                "El ejercicio presenta una alta demanda cognitiva para el estudiante."
            )

        elif dificultad == "media":

            interpretacion[
                "complejidad"
            ] = (

                "El ejercicio presenta una dificultad moderada."
            )

        else:

            interpretacion[
                "complejidad"
            ] = (

                "El ejercicio presenta una dificultad básica."
            )

        # ==========================================
        # COMPARACIÓN CON MODELO DOCENTE
        # ==========================================

        if comparacion_modelo:

            coincidencia = (

                comparacion_modelo.get(
                    "coincidencia",
                    0
                )
            )

            interpretacion[
                "porcentaje_coincidencia"
            ] = coincidencia

            interpretacion[
                "paso_error"
            ] = (

                comparacion_modelo.get(
                    "paso_error"
                )
            )

            interpretacion[
                "esperado"
            ] = (

                comparacion_modelo.get(
                    "esperado"
                )
            )

            interpretacion[
                "obtenido"
            ] = (

                comparacion_modelo.get(
                    "obtenido"
                )
            )

            if coincidencia >= 80:

                interpretacion[
                    "estado_modelo"
                ] = (

                    "Coincidencia alta con la resolución modelo."
                )

            elif coincidencia >= 50:

                interpretacion[
                    "estado_modelo"
                ] = (

                    "Coincidencia parcial con la resolución modelo."
                )

            else:

                interpretacion[
                    "estado_modelo"
                ] = (

                    "Coincidencia baja con la resolución modelo."
                )

        # ==========================================
        # PERFIL MATEMÁTICO BÁSICO
        # ==========================================

        nivel_logro = interpretacion.get(
            "nivel_logro",
            "En proceso"
        )

        if (
                nivel_logro == "Logrado"
                and
                "perfil_matematico"
                not in interpretacion
            ):

            interpretacion[
                "perfil_matematico"
            ] = (

                "Demuestra dominio adecuado de los procedimientos matemáticos analizados."
            )

        elif nivel_logro == "En proceso":

            interpretacion[
                "perfil_matematico"
            ] = (

                "Presenta avances parciales y requiere reforzamiento en algunos procedimientos matemáticos."
            )

        elif nivel_logro == "Inicio":

            interpretacion[
                "perfil_matematico"
            ] = (

                "Presenta dificultades significativas en la comprensión y aplicación de procedimientos matemáticos."
            )

        else:

            interpretacion[
                "perfil_matematico"
            ] = (

                "Perfil matemático en evaluación."
            )

        # ==========================================
        # OBSERVACIÓN GENERAL
        # ==========================================

        if resultado.get(
            "correcto"
        ):

            interpretacion[
                "observacion"
            ] = (

                "El estudiante resolvió correctamente el procedimiento manteniendo equivalencia matemática durante el desarrollo."
            )

        else:

            interpretacion[
                "observacion"
            ] = (

                interpretacion.get(
                    "descripcion_pedagogica",
                    "Se identificaron oportunidades de mejora en el procedimiento matemático."
                )
            )

        return interpretacion