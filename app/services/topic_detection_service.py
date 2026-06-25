class TopicDetectionService:


    @staticmethod
    def detectar_tema(
        expresion
    ):


        expresion = (
            expresion.lower()
        )


        # ECUACIONES

        if '=' in expresion:

            return (
                'ecuaciones'
            )


        # DISTRIBUTIVA

        if '*(' in expresion:

            return (
                'propiedad_distributiva'
            )


        # POTENCIAS

        if '**' in expresion:

            return (
                'potencias'
            )


        # FRACCIONES

        if '/' in expresion:

            return (
                'fracciones'
            )


        # ÁLGEBRA BÁSICA

        if any(

            letra in expresion

            for letra in [
                'x',
                'y',
                'z'
            ]
        ):

            return (
                'algebra_basica'
            )


        return (
            'aritmetica'
        )