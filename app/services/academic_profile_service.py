class AcademicProfileService:


    @staticmethod
    def generar_perfil(


        resultado
    ):


        score = resultado.get(
            'score_global',
            0
        )


        if score >= 85:


            return {

                'nivel':
                    'Alto',

                'descripcion':

                    'El estudiante demuestra '
                    'buen dominio algebraico '
                    'y adecuada resolución '
                    'matemática.',

                'color':
                    'success'
            }


        elif score >= 60:


            return {

                'nivel':
                    'Medio',

                'descripcion':

                    'El estudiante presenta '
                    'algunas dificultades '
                    'matemáticas moderadas.',

                'color':
                    'warning'
            }


        else:


            return {

                'nivel':
                    'Bajo',

                'descripcion':

                    'El estudiante requiere '
                    'reforzamiento académico '
                    'y seguimiento pedagógico.',

                'color':
                    'danger'
            }