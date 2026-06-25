class LearningTrendService:


    @staticmethod
    def analizar_tendencia(
        historico
    ):


        if len(historico) < 2:

            return (
                'sin_datos'
            )


        inicial = historico[0]

        final = historico[-1]


        if final > inicial:

            return (
                'mejora'
            )


        if final < inicial:

            return (
                'descenso'
            )


        return (
            'estable'
        )