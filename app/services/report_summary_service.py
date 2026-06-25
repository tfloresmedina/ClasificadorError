class ReportSummaryService:


    @staticmethod
    def generar_resumen(


        estudiante,

        porcentaje,

        riesgo,

        tendencia
    ):


        resumen = (


            f'Estudiante: {estudiante}. '


            f'Rendimiento: {porcentaje}%. '


            f'Nivel de riesgo: {riesgo}. '


            f'Tendencia académica: {tendencia}.'
        )


        return resumen