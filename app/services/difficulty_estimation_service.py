class DifficultyEstimationService:


    @staticmethod
    def estimar_dificultad(
        expresion
    ):


        score = 0


        # VARIABLES

        if any(

            letra in expresion

            for letra in [
                'x',
                'y',
                'z'
            ]
        ):

            score += 2


        # PARÉNTESIS

        if '(' in expresion:

            score += 2


        # DIVISIONES

        if '/' in expresion:

            score += 2


        # POTENCIAS

        if '**' in expresion:

            score += 3


        # ECUACIONES

        if '=' in expresion:

            score += 2


        # LONGITUD

        if len(expresion) > 10:

            score += 1


        # CLASIFICACIÓN

        if score <= 2:

            return 'baja'


        if score <= 5:

            return 'media'


        return 'alta'