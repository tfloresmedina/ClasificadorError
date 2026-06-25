from app.models.resultado_analisis import (
    ResultadoAnalisis
)


class StudentDashboardService:


    @staticmethod
    def obtener_metricas_estudiante():


        total = (

            ResultadoAnalisis
            .query
            .count()
        )


        correctos = (

            ResultadoAnalisis
            .query
            .filter_by(
                es_correcto=True
            )
            .count()
        )


        incorrectos = (

            ResultadoAnalisis
            .query
            .filter_by(
                es_correcto=False
            )
            .count()
        )


        porcentaje = 0


        if total > 0:


            porcentaje = (

                correctos
                / total
            ) * 100


        return {

            'total':
                total,

            'correctos':
                correctos,

            'incorrectos':
                incorrectos,

            'porcentaje':

                round(
                    porcentaje,
                    2
                )
        }