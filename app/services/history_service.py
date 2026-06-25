from app.models.resultado_analisis import (
    ResultadoAnalisis
)


class HistoryService:


    @staticmethod
    def obtener_historial(


        limite=50
    ):


        historial = (

            ResultadoAnalisis
            .query

            .order_by(
                ResultadoAnalisis.fecha_registro.desc()
            )

            .limit(
                limite
            )

            .all()
        )


        return historial