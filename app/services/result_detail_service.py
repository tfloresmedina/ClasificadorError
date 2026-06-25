from app.models.resultado_analisis import (
    ResultadoAnalisis
)


class ResultDetailService:


    @staticmethod
    def obtener_resultado(


        resultado_id
    ):


        resultado = (

            ResultadoAnalisis
            .query
            .get(
                resultado_id
            )
        )


        return resultado