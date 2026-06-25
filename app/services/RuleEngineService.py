class RuleEngineService:

    @staticmethod
    def detectar_error(

        paso_actual,

        paso_siguiente,

        resultado_transformacion
    ):

        # Error aritmético

        if not resultado_transformacion.get(
            "valido",
            True
        ):

            return "operacion_incorrecta"

        # Error de fracciones

        if (

            "/" in paso_actual

            and

            "/" in paso_siguiente

            and

            not resultado_transformacion.get(
                "valido",
                True
            )
        ):

            return "fraccion_incorrecta"

        # Error de despeje

        if (

            "x" in paso_actual

            and

            "=" in paso_actual

            and

            "x" not in paso_siguiente

        ):

            return "despeje_incorrecto"

        return "sin_error"