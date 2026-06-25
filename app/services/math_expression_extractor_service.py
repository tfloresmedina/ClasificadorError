import re


class MathExpressionExtractorService:

    PATRONES = [

        # ecuaciones
        r'[0-9a-zA-Z\+\-\*/\(\)\s]+=[0-9a-zA-Z\+\-\*/\(\)\s]+',

        # expresiones algebraicas
        r'\d*x[\+\-\*/]\d+',
        r'\d*x[\+\-\*/]\d*x',

        # operaciones
        r'\d+\s*[\+\-\*/]\s*\d+',

        # perímetro
        r'P\s*=\s*.+',

        # área
        r'A\s*=\s*.+',

        # fracciones
        r'\d+\s*/\s*\d+'
    ]

    @classmethod
    def extraer(cls, texto):

        if not texto:
            return []

        expresiones = []

        texto = texto.replace("\n", " ")

        for patron in cls.PATRONES:

            encontrados = re.findall(
                patron,
                texto
            )

            for item in encontrados:

                item = item.strip()

                if len(item) < 3:
                    continue

                expresiones.append(item)

        # eliminar duplicados
        expresiones = list(
            dict.fromkeys(
                expresiones
            )
        )

        return expresiones