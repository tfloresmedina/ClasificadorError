import re


class MathStepFilter:

    @classmethod
    def es_matematico(cls, texto):

        if not texto:
            return False

        texto = str(texto).strip()

        texto_lower = texto.lower()

        # Respuestas
        if texto_lower.startswith("rpta"):
            return True

        # Debe tener igualdad o comparación
        if any(
            simbolo in texto
            for simbolo in [
                "=",
                "<",
                ">",
                "≤",
                "≥"
            ]
        ):

            numeros = re.findall(
                r'\d+',
                texto
            )

            return len(numeros) >= 1

        return False

    @classmethod
    def filtrar(cls, pasos):

        pasos_filtrados = []

        for paso in pasos:

            if cls.es_matematico(paso):

                pasos_filtrados.append(
                    paso
                )

        return pasos_filtrados