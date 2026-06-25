class StepEstimationService:


    @staticmethod
    def estimar_pasos(
        expresion
    ):


        pasos = 1


        # OPERACIONES

        operadores = [

            '+',
            '-',
            '*',
            '/',
            '='
        ]


        for operador in operadores:

            pasos += (
                expresion.count(
                    operador
                )
            )


        # PARÉNTESIS

        pasos += (

            expresion.count('(')
        )


        # POTENCIAS

        pasos += (

            expresion.count('**') * 2
        )


        return pasos