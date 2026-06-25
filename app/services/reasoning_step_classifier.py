import re


class ReasoningStepClassifier:


    @staticmethod
    def clasificar(paso):

        if not paso:
            return "desconocido"

        paso = paso.strip().lower()

        # ==================================
        # CONCLUSIONES
        # ==================================

        palabras_conclusion = [

            "respuesta",
            "rpta",
            "correcta",
            "incorrecta",
            "si",
            "sí",
            "no",
            "conclusion",
            "conclusión"
        ]

        for palabra in palabras_conclusion:

            if palabra in paso:

                return "conclusion"

        # ==================================
        # COMPARACIONES
        # ==================================

        if (
            "<" in paso
            or ">" in paso
            or "<=" in paso
            or ">=" in paso
        ):

            return "comparacion"

        # ==================================
        # ECUACIONES
        # ==================================

        if len(paso) > 30 and "=" not in paso:
            return "texto"
        if "=" in paso:

            return "ecuacion"

        # ==================================
        # OPERACIONES NUMÉRICAS
        # ==================================

        if re.search(

            r'[\+\-\*/÷×]',

            paso
        ):

            return "calculo"

        # ==================================
        # TEXTO EXPLICATIVO
        # ==================================

        if len(paso.split()) > 3:

            return "explicacion"

        return "otro"