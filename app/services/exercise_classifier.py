import re


class ExerciseClassifier:

    @staticmethod
    def clasificar(pasos):

        texto = " ".join(
            pasos
        ).lower()

        texto_limpio = texto.strip()

        # =====================================
        # TEXTO VACÍO
        # =====================================

        if not texto_limpio:

            return {
                "tipo": "vacio",
                "analizable": False,
                "motivo": "Sin contenido matemático"
            }

        # =====================================
        # SELECCIÓN MÚLTIPLE
        # =====================================

        patrones_multiple = [

            r'a\)',
            r'b\)',
            r'c\)',
            r'd\)',
            r'e\)'
        ]

        coincidencias = sum(

            1

            for patron in patrones_multiple

            if re.search(
                patron,
                texto_limpio
            )
        )

        if coincidencias >= 3:

            return {
                "tipo": "seleccion_multiple",
                "analizable": False,
                "motivo": "Ejercicio de alternativa múltiple"
            }

        # =====================================
        # GEOMETRÍA
        # =====================================

        palabras_geometria = [

            "angulo",
            "triangulo",
            "perimetro",
            "area",
            "rectangulo",
            "cuadrado",
            "circunferencia",
            "radio",
            "diametro",
            "figura"
        ]

        if any(
            palabra in texto_limpio
            for palabra in palabras_geometria
        ):

            return {
                "tipo": "geometria",
                "analizable": False,
                "motivo": "Análisis geométrico no implementado"
            }

        # =====================================
        # FRACCIONES
        # =====================================

        if re.search(
            r'\d+\s*/\s*\d+',
            texto_limpio
        ):

            return {
                "tipo": "fraccion",
                "analizable": True,
                "motivo": None
            }

        # =====================================
        # ECUACIONES
        # =====================================

        if (

            "=" in texto_limpio

            and

            any(
                variable in texto_limpio
                for variable in [
                    "x",
                    "y",
                    "z"
                ]
            )
        ):

            return {
                "tipo": "ecuacion",
                "analizable": True,
                "motivo": None
            }

        # =====================================
        # ÁLGEBRA
        # =====================================

        if any(
            variable in texto_limpio
            for variable in [
                "x",
                "y",
                "z"
            ]
        ):

            return {
                "tipo": "algebra",
                "analizable": True,
                "motivo": None
            }

        # =====================================
        # ARITMÉTICA
        # =====================================

        operadores = [

            "+",
            "-",
            "*",
            "/",
            "÷",
            "×"
        ]

        if any(
            op in texto_limpio
            for op in operadores
        ):

            return {
                "tipo": "aritmetica",
                "analizable": True,
                "motivo": None
            }

        # =====================================
        # PROBLEMAS SIN PROCEDIMIENTO
        # =====================================

        if len(texto_limpio.split()) > 6:

            return {
                "tipo": "problema_sin_procedimiento",
                "analizable": False,
                "motivo": "No se detectó desarrollo matemático"
            }

        # =====================================
        # DESCONOCIDO
        # =====================================

        return {
            "tipo": "desconocido",
            "analizable": False,
            "motivo": "Tipo de ejercicio no reconocido"
        }