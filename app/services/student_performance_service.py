class StudentPerformanceService:


    @staticmethod
    def resumir_desempeno(
        nombre_estudiante,
        resultados
    ):


        total = len(resultados)


        correctos = sum(

            1

            for r in resultados

            if r.get('correcto')
        )


        incorrectos = (
            total - correctos
        )


        porcentaje = 0


        if total > 0:

            porcentaje = round(

                (
                    correctos / total
                ) * 100,

                2
            )


        return {

            'estudiante':
            nombre_estudiante,

            'total_ejercicios':
            total,

            'correctos':
            correctos,

            'incorrectos':
            incorrectos,

            'porcentaje_acierto':
            porcentaje
        }