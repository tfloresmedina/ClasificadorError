import re


class MathContentDetectorService:

    TIPOS = [
        "ecuacion",
        "aritmetica",
        "fraccion",
        "geometria"
    ]

    @classmethod
    def detectar(cls, texto):

        if not texto:
            return []

        bloques = []

        lineas = texto.splitlines()

        for linea in lineas:

            linea = linea.strip()

            if not linea:
                continue

            tipo = cls.detectar_tipo(
                linea
            )

            if tipo:

                bloques.append({

                    "tipo": tipo,

                    "contenido": linea

                })

        return bloques

    @classmethod
    def detectar_tipo(
        cls,
        texto
    ):

        texto = texto.strip()

        # ==========================
        # FRACCIONES
        # ==========================

        if re.search(
            r'\d+\s*/\s*\d+',
            texto
        ):

            return "fraccion"

        # ==========================
        # GEOMETRIA
        # ==========================

        if (

            "perimetro" in texto.lower()

            or

            "area" in texto.lower()

            or

            re.search(
                r'^[PA]\s*=',
                texto,
                re.IGNORECASE
            )
        ):

            return "geometria"

        # ==========================
        # ECUACIONES
        # ==========================

        if (

            "=" in texto

            and

            any(
                variable in texto.lower()
                for variable in [
                    "x",
                    "y",
                    "z"
                ]
            )
        ):

            return "ecuacion"

        # ==========================
        # ARITMETICA
        # ==========================

        if re.search(
            r'\d+\s*[\+\-\*/÷×]\s*\d+',
            texto
        ):

            return "aritmetica"

        return None