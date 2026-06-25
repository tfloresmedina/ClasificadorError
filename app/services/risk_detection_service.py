class RiskDetectionService:


    @staticmethod
    def detectar_riesgo(
        porcentaje_acierto
    ):


        if porcentaje_acierto >= 70:

            return (
                'bajo'
            )


        if porcentaje_acierto >= 40:

            return (
                'medio'
            )


        return (
            'alto'
        )