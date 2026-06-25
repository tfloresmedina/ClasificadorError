# =========================================================
# STEP PARSER SERVICE
# I.E Elvira García Y García
# =========================================================

import re


class StepParserService:

    @staticmethod
    def parsear(texto_ocr):

        if not texto_ocr:

            return []

        texto = str(texto_ocr)

        texto = texto.replace("\r", "\n")

        lineas = texto.split("\n")

        lineas_limpias = []

        for linea in lineas:

            linea = linea.strip()

            if not linea:
                continue

            linea = re.sub(
                r"\s+",
                "",
                linea
            )

            lineas_limpias.append(linea)

        ejercicios = []

        ejercicio_actual = []

        patron_ejercicio = re.compile(
            r"^\d+[\)\.]"
        )

        for linea in lineas_limpias:

            if patron_ejercicio.match(linea):

                if ejercicio_actual:

                    ejercicios.append(
                        ejercicio_actual
                    )

                linea = re.sub(
                    r"^\d+[\)\.]",
                    "",
                    linea
                )

                ejercicio_actual = []

                if linea:

                    ejercicio_actual.append(
                        linea
                    )

            else:

                ejercicio_actual.append(
                    linea
                )

        if ejercicio_actual:

            ejercicios.append(
                ejercicio_actual
            )

        resultado = []

        for indice, ejercicio in enumerate(
            ejercicios,
            start=1
        ):

            pasos = []

            for paso in ejercicio:

                # Caso:
                # 1/2+1/3=3/6+2/6=5/6

                if paso.count("=") > 1:

                    partes = paso.split("=")

                    for i in range(
                        len(partes) - 1
                    ):

                        nuevo_paso = (

                            partes[i].strip()
                            +
                            "="
                            +
                            partes[i + 1].strip()
                        )

                        nuevo_paso = (
                            StepParserService.normalizar(
                                nuevo_paso
                            )
                        )

                        if (
                            StepParserService
                            .es_paso_matematico(
                                nuevo_paso

                                
                            )
                            
                        ):
                            print(
                                    "PASO ACEPTADO:",
                                    paso
                                )
                            pasos.append(
                                nuevo_paso
                            )

                        else:

                                    print(
                                        "PASO DESCARTADO:",
                                        paso
                                    )

                    continue

                paso = (
                    StepParserService
                    .normalizar(
                        paso
                    )
                )

                if (
                    paso
                    and
                    StepParserService
                    .es_paso_matematico(
                        paso
                    )
                ):

                    pasos.append(
                        paso
                    )

            resultado.append({

                "ejercicio":
                    indice,

                "pasos":
                    pasos,

                "cantidad_pasos":
                    len(pasos)
            })

        return resultado

    # =====================================================
    # NORMALIZADOR
    # =====================================================

    @staticmethod
    def normalizar(expresion):

        if not expresion:

            return ""

        expr = str(expresion)

        expr = expr.replace("X", "x")

        expr = expr.replace("×", "*")

        expr = expr.replace("÷", "/")

        expr = expr.replace("^", "**")

        expr = expr.replace(" ", "")

        expr = re.sub(
            r"(\d)(x)",
            r"\1*\2",
            expr
        )

        expr = re.sub(
            r"(\d)(\()",
            r"\1*\2",
            expr
        )

        expr = re.sub(
            r"(\))(\d)",
            r"\1*\2",
            expr
        )

        expr = re.sub(
            r"(\))([a-z])",
            r"\1*\2",
            expr
        )

        expr = re.sub(
            r"([a-z])(\()",
            r"\1*\2",
            expr
        )

        return expr

    # =====================================================
    # DETECTAR TIPO
    # =====================================================
    @staticmethod
    def es_paso_matematico(texto):

        texto = str(texto)

        # Muy largo = probablemente enunciado
        if len(texto) > 30:
            return False

        # Debe contener igualdad o comparación
        if not any(
            simbolo in texto
            for simbolo in [
                "=",
                "<",
                ">",
                "≤",
                "≥"
            ]
        ):
            return False

        numeros = re.findall(
            r'\d+',
            texto
        )

        return len(numeros) >= 2
    @staticmethod
    def detectar_tipo(pasos):

        texto = " ".join(pasos)

        if "=" in texto:

            return "ecuacion"

        if "/" in texto:

            return "fraccion"

        if "(" in texto:

            return "distributiva"

        if "**" in texto:

            return "potencia"

        return "operacion"

    # =====================================================
    # TIMELINE BASE
    # =====================================================

    @staticmethod
    def construir_timeline(pasos):

        timeline = []

        for indice, paso in enumerate(
            pasos,
            start=1
        ):

            timeline.append({

                "paso":
                    indice,

                "expresion":
                    paso,

                "descripcion":
                    f"Paso {indice}"
            })

        return timeline
