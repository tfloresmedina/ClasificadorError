class PerformanceMetricsService:


    @staticmethod
    def calcular_metricas(
        resultados
    ):


        total = len(resultados)


        if total == 0:

            return {

                'total': 0,

                'correctos': 0,

                'incorrectos': 0,

                'porcentaje_correctos': 0
            }


        correctos = sum(

            1

            for r in resultados

            if r.get('correcto')
        )


        incorrectos = (
            total - correctos
        )


        porcentaje_correctos = round(

            (
                correctos / total
            ) * 100,

            2
        )


        return {

            'total':
            total,

            'correctos':
            correctos,

            'incorrectos':
            incorrectos,

            'porcentaje_correctos':
            porcentaje_correctos
        }