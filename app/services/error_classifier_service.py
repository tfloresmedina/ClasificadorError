class ErrorClassifierService:

    @staticmethod
    def clasificar_error_procedimiento(
        resultado_validacion
    ):

        if resultado_validacion.get(
            "valido",
            True
        ):

            return {

                "tipo_error":
                "sin_error",

                "fase_polya":
                "Verificación",

                "descripcion":
                "Procedimiento correcto.",

                "recomendacion":
                "Continuar con ejercicios de mayor complejidad.",

                "severidad":
                "bajo"
            }

        paso_actual = (

            resultado_validacion.get(
                "paso_actual",
                ""
            )
        )

        paso_siguiente = (

            resultado_validacion.get(
                "paso_siguiente",
                ""
            )
        )

        # ==================================
        # ERROR ARITMÉTICO
        # ==================================

        if (

            "=" in paso_actual

            and

            "=" in paso_siguiente
        ):

            return {

                "tipo_error":
                "operacion_incorrecta",

                "fase_polya":
                "Ejecución del plan",

                "descripcion":
                "El resultado numérico obtenido no coincide con el procedimiento esperado.",

                "recomendacion":
                "Revisar cálculos y operaciones básicas.",

                "severidad":
                "alto"
            }

        # ==================================
        # SIMPLIFICACIÓN
        # ==================================

        if (

            "*" in paso_actual

            or

            "+" in paso_actual
        ):

            return {

                "tipo_error":
                "simplificacion_incorrecta",

                "fase_polya":
                "Ejecución del plan",

                "descripcion":
                "La simplificación algebraica presenta inconsistencias.",

                "recomendacion":
                "Reforzar ejercicios de reducción de términos semejantes.",

                "severidad":
                "moderado"
            }

        # ==================================
        # DESPEJE
        # ==================================

        return {

            "tipo_error":
            "despeje_incorrecto",

            "fase_polya":
            "Ejecución del plan",

            "descripcion":
            "Se detectó una transformación algebraica incorrecta entre pasos.",

            "recomendacion":
            "Revisar el despeje de variables y la transposición de términos.",

            "severidad":
            "alto"
        }

    @staticmethod
    def clasificar_error(
        respuesta_alumno,
        respuesta_correcta
    ):


        respuesta_alumno = (
            respuesta_alumno.replace(
                ' ',
                ''
            )
        )

        respuesta_correcta = (
            respuesta_correcta.replace(
                ' ',
                ''
            )
        )


        # ERROR DE SIGNOS

        if (

            '-' in respuesta_alumno

            and

            '+' in respuesta_correcta
        ):

                       return {

                'tipo_error':
                'error_signos',


                'descripcion':

                'El estudiante presenta '
                'dificultades en el manejo '
                'de signos algebraicos.',


                'recomendacion':

                'Se recomienda reforzar '
                'operaciones con números '
                'enteros y reglas de signos '
                'mediante ejercicios guiados.',


                'competencia':

                'Resuelve problemas '
                'de cantidad.',


                'fase_polya':

                'Ejecución del plan',


                'severidad':

                'moderado'
            }


        # ERROR PARÉNTESIS

        if (

            '(' not in respuesta_alumno

            and

            '(' in respuesta_correcta
        ):

                        return {

                'tipo_error':
                'error_jerarquia',


                'descripcion':

                'El estudiante presenta '
                'dificultades en la aplicación '
                'de la jerarquía de operaciones.',


                'recomendacion':

                'Se recomienda reforzar '
                'ejercicios progresivos '
                'de operaciones combinadas '
                'y uso correcto de paréntesis.',


                'competencia':

                'Resuelve problemas '
                'de regularidad, '
                'equivalencia y cambio.',


                'fase_polya':

                'Diseñar estrategia',


                'severidad':

                'alto'
            }


        # ERROR SIMPLIFICACIÓN

        if (

            '/' in respuesta_correcta

            and

            '/' not in respuesta_alumno
        ):

            return {

                'tipo_error':
                'error_simplificacion',


                'descripcion':

                'El estudiante presenta '
                'dificultades en procesos '
                'de simplificación algebraica.',


                'recomendacion':

                'Se recomienda reforzar '
                'ejercicios progresivos '
                'de simplificación y '
                'equivalencia algebraica.',


                'competencia':

                'Resuelve problemas '
                'de regularidad, '
                'equivalencia y cambio.',


                'fase_polya':

                'Ejecución del plan',


                'severidad':

                'moderado'
            }


        # ERROR PROCEDIMIENTO

        if (

            len(respuesta_alumno)

            >

            len(respuesta_correcta) * 1.8
        ):

            return {

                'tipo_error':
                'procedimiento_inconsistente',


                'descripcion':

                'El procedimiento '
                'matemático presenta '
                'pasos inconsistentes '
                'durante el desarrollo.',


                'recomendacion':

                'Se recomienda reforzar '
                'la validación paso a paso '
                'y el control de operaciones '
                'algebraicas.',


                'competencia':

                'Resuelve problemas '
                'de cantidad.',


                'fase_polya':

                'Diseñar estrategia',


                'severidad':

                'alto'
            }


        # ERROR GENERAL

        return {

            'tipo_error':
            'respuesta_incorrecta',


            'descripcion':

            'La respuesta no coincide '
            'con la estructura algebraica '
            'esperada.',


            'recomendacion':

            'Se recomienda reforzar '
            'la resolución progresiva '
            'de ejercicios matemáticos '
            'y la verificación '
            'del procedimiento.',


            'competencia':

            'Resuelve problemas '
            'de cantidad.',


            'fase_polya':

            'Verificación de resultados',


            'severidad':

            'moderado'
        }