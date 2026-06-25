import re


class OCRMathExtractorService:

    @staticmethod
    def extraer(texto_ocr):

        if not texto_ocr:
            return []

        lineas = texto_ocr.splitlines()

        matematicas = []

        patrones = [

            r'=',
            r'\d+\s*[+\-*/]\s*\d+',
            r'[xyzXYZ]\s*=',
            r'\d+[xyzXYZ]',
            r'P\s*=',
            r'A\s*=',
            r'\(',
            r'\)',
            r'÷',
            r'×'

        ]

        for linea in lineas:

            linea = linea.strip()

            if not linea:
                continue

            es_matematica = False

            for patron in patrones:

                if re.search(
                    patron,
                    linea
                ):
                    es_matematica = True
                    break

            if es_matematica:

                matematicas.append(
                    linea
                )

        return matematicas