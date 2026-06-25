import re


class MathProcedureParserService:

    @staticmethod
    def limpiar_linea(linea):

        if not linea:
            return None

        linea = linea.strip()

        if not linea:
            return None

        # quitar numeración de ejercicio
        linea = re.sub(
             r'^[a-eA-E]\)\s*',
            '',
            linea
        )

        linea = linea.strip()

        if not linea:
            return None

        return linea


    @staticmethod
    def normalizar_expresion(expresion):

        if not expresion:
            return ""
        expresion = expresion.replace("\\times", "*")
        expresion = expresion.replace("times", "*")
        expresion = expresion.replace("\\div", "/")
        expresion = expresion.replace("div", "/")
        expresion = expresion.replace(" ", "")
        # Separar ecuaciones pegadas por OCR

        print("ANTES:", expresion)

        expresion = re.sub(
            r'\\frac\{([^{}]+)\}\{([^{}]+)\}',
            r'(\1/\2)',
            expresion,
            flags=re.IGNORECASE
        )

        expresion = re.sub(
            r'cm\^?2',
            '',
            expresion,
            flags=re.IGNORECASE
        )

        print("DESPUES:", expresion)
        expresion = expresion.replace("$", "")

        expresion = re.sub(
            r'(x=\d+)(\d*x=)',
            r'\1\n\2',
            expresion
        )
        # 3x -> 3*x
        expresion = re.sub(
            r'(\d)([a-zA-Z])',
            r'\1*\2',
            expresion
        )

        return expresion

    @staticmethod
    def dividir_ecuaciones_multiples(
        paso
        ):

        if not paso:
            return []

        if paso.count("=") <= 1:

            return [paso]

        partes = paso.split("=")

        resultado = []

        for i in range(
            len(partes) - 1
        ):

            resultado.append(

                partes[i].strip()
                +
                "="
                +
                partes[i + 1].strip()
            )

        return resultado




    @classmethod
    def parsear_ejercicio(
    cls,
    lineas
):

        pasos = []

        for linea in lineas:

            limpia = cls.limpiar_linea(
                linea
            )

            if not limpia:
                continue

            if limpia.lower() in [

                "rpta",

                "rpta:",

                "respuesta",

                "respuesta:"
            ]:

                continue

            normalizada = (
                cls.normalizar_expresion(
                    limpia
                )
            )


            if "Rpta:" in normalizada:

                partes = normalizada.split("Rpta:")

                if partes[0].strip():

                    pasos.append(
                        partes[0].strip()
                    )

                pasos.append(
                    "Rpta:" + partes[1].strip()
                )

                continue

            

            print("LINEA ORIGINAL:", linea)
            print("LINEA LIMPIA:", limpia)
            print("LINEA NORMALIZADA:", normalizada)

            if re.fullmatch(
                r'\d+',
                normalizada
            ):
                continue

            if normalizada in [
                '=',
                '==',
                'x',
                '+',
                '-',
                '*',
                '/'
            ]:
                continue

            if len(
                normalizada.strip()
            ) < 2:
                continue

            if normalizada.strip().endswith("="):

                print(
                    f"PASO INCOMPLETO IGNORADO: {normalizada}"
                )

                continue



            if normalizada.startswith("="):

                    continue
            if (
                    
                cls.es_linea_matematica(
                    normalizada
                )
                and
                (
                    "=" in normalizada
                    or re.search(
                        r'\d+\s*[\+\-\*/]\s*\d+',
                        normalizada
                    )
                )
            ):

                nuevos_pasos = (
                    cls.dividir_ecuaciones_multiples(
                        normalizada
                    )
                )

                pasos.extend(
                    nuevos_pasos
            )

                print(
                    f"PASO AGREGADO: {normalizada}"
                )

            else:

                print(
                    f"LINEA IGNORADA PARSER: {normalizada}"
                )

            print("\n====================")
            print("PARSER RESULTADO")
            print("====================")
            print(pasos)
            print("====================")

        return {

            "pasos": pasos,

            "cantidad_pasos": len(
                pasos
            ),

            "es_valido": len(
                pasos
            ) > 0
        }
    

    @staticmethod
    def es_linea_matematica(texto):

        if not texto:
            return False

        patrones = [

            r'=',
            r'\d+\s*[+\-*/]\s*\d+',
            r'\d+[xyz]',
            r'[xyz]\s*=',
            r'\d+\s*/\s*\d+',
            r'P\s*=',
            r'A\s*=',
            r'\(',
            r'\)'
        ]

        for patron in patrones:

            if re.search(
                patron,
                texto,


                re.IGNORECASE
            ):
                return True

        return False

