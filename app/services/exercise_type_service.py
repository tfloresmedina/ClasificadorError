class ExerciseTypeService:


    @staticmethod
    def detectar_tipo(
        expresion
    ):

        expresion = (
            expresion.lower()
        )

        # =====================================
        # ECUACIÓN
        # =====================================

        if '=' in expresion:

            return 'ecuacion'

        # =====================================
        # FRACCIÓN
        # =====================================

        if '/' in expresion:

            return 'fraccion'

        # =====================================
        # POTENCIA
        # =====================================

        if '**' in expresion:

            return 'potencia'

        # =====================================
        # DISTRIBUTIVA
        # =====================================

        if '*(' in expresion:

            return 'distributiva'

        # =====================================
        # SIMPLIFICACIÓN ALGEBRAICA
        # =====================================

        if (

            any(
                variable in expresion

                for variable in [
                    'x',
                    'y',
                    'z'
                ]
            )

            and

            '+' in expresion

        ):

            return 'simplificacion'

        # =====================================
        # OPERACIÓN ALGEBRAICA
        # =====================================

        if any(

            variable in expresion

            for variable in [
                'x',
                'y',
                'z'
            ]
        ):

            return 'algebraico'

        # =====================================
        # ARITMÉTICO
        # =====================================

        return 'aritmetico'