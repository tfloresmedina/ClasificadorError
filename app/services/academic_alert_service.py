class AcademicAlertService:


    @staticmethod
    def generar_alertas(


        resultado,

        perfil_academico
    ):


        alertas = []


        # =============================================
        # RIESGO
        # =============================================

        if resultado.get(
            'riesgo'
        ) == 'alto':


            alertas.append({

                'tipo':
                    'danger',

                'titulo':
                    'Riesgo Académico Alto',

                'descripcion':

                    'El estudiante presenta '
                    'dificultades matemáticas '
                    'considerables.'
            })


        # =============================================
        # DIFICULTAD
        # =============================================

        if resultado.get(
            'dificultad'
        ) == 'alta':


            alertas.append({

                'tipo':
                    'warning',

                'titulo':
                    'Ejercicio Complejo',

                'descripcion':

                    'El procedimiento matemático '
                    'requiere múltiples pasos '
                    'de resolución.'
            })


        # =============================================
        # PERFIL
        # =============================================

        if perfil_academico.get(
            'nivel'
        ) == 'Bajo':


            alertas.append({

                'tipo':
                    'danger',

                'titulo':
                    'Refuerzo Recomendado',

                'descripcion':

                    'Se recomienda reforzamiento '
                    'académico personalizado.'
            })


        # =============================================
        # ALERTA POSITIVA
        # =============================================

        if not alertas:


            alertas.append({

                'tipo':
                    'success',

                'titulo':
                    'Desempeño Estable',

                'descripcion':

                    'No se detectaron alertas '
                    'académicas significativas.'
            })


        return alertas