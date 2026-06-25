import os
import re
import easyocr

from pdf2image import convert_from_path



class OCRService:

    reader = easyocr.Reader(
        ['es'],
        gpu=False
    )

    @staticmethod
    def extraer_texto(ruta_imagen):

        try:
            extension = os.path.splitext(
                ruta_imagen
            )[1].lower()

            texto_final = ""

            # =====================================
            # PDF
            # =====================================
            if extension == ".pdf":

                paginas = convert_from_path(
                    ruta_imagen,
                    dpi=300,
                    poppler_path=r"C:\poppler\Library\bin"
                )

                textos = []

                for i, pagina in enumerate(paginas):

                    temp_img = f"temp_page_{i}.png"

                    pagina.save(
                        temp_img,
                        "PNG"
                    )

                    resultado = OCRService.reader.readtext(
                        temp_img,
                        detail=1,
                        paragraph=False
                    )

                    texto_pagina = "\n".join(
                        item[1]
                        for item in resultado
                    )

                    textos.append(texto_pagina)

                texto_final = "\n".join(textos)

                confianza_promedio = 100

            # =====================================
            # IMÁGENES
            # =====================================
            else:

                resultado = OCRService.reader.readtext(
                    ruta_imagen,
                    detail=1,
                    paragraph=False
                )

                lineas = []
                confianzas = []

                for item in resultado:

                    texto = item[1].strip()
                    confianza = item[2]

                    if texto:
                        lineas.append(texto)
                        confianzas.append(
                            confianza * 100
                        )

                texto_final = "\n".join(lineas)

                confianza_promedio = (
                    sum(confianzas) / len(confianzas)
                    if confianzas else 0
                )

            print("\n================================")
            print("OCR EXTRAIDO")
            print("================================")
            print(texto_final)
            print("================================")

            mejor_texto = texto_final

            # =====================================
            # LIMPIEZA
            # =====================================

            mejor_texto = re.sub(
                r'[ \t]+',
                ' ',
                mejor_texto
            )

            mejor_texto = mejor_texto.strip()

            reemplazos = {
                '×': '*',
                '÷': '/',
                '—': '-',
                '–': '-'
            }

            for origen, destino in reemplazos.items():
                mejor_texto = mejor_texto.replace(
                    origen,
                    destino
                )

            mejor_texto = re.sub(
                r'S=',
                '=',
                mejor_texto
            )

            mejor_texto = re.sub(
                r'\$=',
                '=',
                mejor_texto
            )

            mejor_texto = re.sub(
                r'(?<=x)25\b',
                '=5',
                mejor_texto
            )

            mejor_texto = re.sub(
                r'(?<=x)213\b',
                '=13',
                mejor_texto
            )

            if not mejor_texto:
                return {
                    'valido': False,
                    'error': 'OCR vacío'
                }

            # =====================================
            # LIMPIEZA AVANZADA
            # =====================================

            mejor_texto = re.sub(
                r'(\d+\))',
                r'\n\1',
                mejor_texto
            )

            mejor_texto = re.sub(
                r'\n+',
                '\n',
                mejor_texto
            )

            mejor_texto = re.sub(
                r'(x=\d+)\s+(\d*x)',
                r'\1\n\2',
                mejor_texto
            )

            lineas_limpias = []

            for linea in mejor_texto.split("\n"):

                linea = linea.strip()

                if linea.startswith(".="):
                    continue

                if linea.count("=") > 2:
                    continue

                lineas_limpias.append(linea)

            mejor_texto = "\n".join(
                lineas_limpias
            )

            mejor_texto = re.sub(
                r'(x=\d+)\s+(\d*x[\+\-])',
                r'\1\n\2',
                mejor_texto
            )

            mejor_texto = re.sub(
                r'(x=\d+)\s+(\d*x=)',
                r'\1\n\2',
                mejor_texto
            )

            print("\n================================")
            print("OCR LIMPIO")
            print("================================")
            print(mejor_texto)
            print("================================")

            # RETORNO FINAL
            return {
                'valido': True,
                'texto': mejor_texto,
                'confianza': round(
                    confianza_promedio,
                    2
                )
            }

        except Exception as e:

            print(
                "ERROR OCR:",
                str(e)
            )

            return {
                'valido': False,
                'error': str(e)
            }