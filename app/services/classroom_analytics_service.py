class ClassroomAnalyticsService:


    @staticmethod
    def resumir_aula(
        estudiantes
    ):


        total_estudiantes = (
            len(estudiantes)
        )


        if total_estudiantes == 0:

            return {

                'total_estudiantes': 0,

                'promedio_general': 0
            }


        suma_porcentajes = sum(

            estudiante.get(
                'porcentaje_acierto',
                0
            )

            for estudiante in estudiantes
        )


        promedio_general = round(

            suma_porcentajes
            /
            total_estudiantes,

            2
        )


        return {

            'total_estudiantes':
            total_estudiantes,

            'promedio_general':
            promedio_general
        }