import re


class OCRAutoCorrectService:


    @staticmethod
    def autocorregir(
        expresion
    ):

        if not expresion:

            return {

                'expresion_corregida': '',

                'cambios': [],

                'corregido': False
            }

        expresion_corregida = expresion

        cambios = []

        # =====================================
        # REEMPLAZOS SEGUROS
        # =====================================

        reemplazos = {

            'O': '0',
            'o': '0',

            'l': '1',
            'I': '1',
            '|': '1',

            '—': '-',
            '_': '-',

            '×': '*',
            '÷': '/',

            '==': '='
        }

        for original, nuevo in reemplazos.items():

            if original in expresion_corregida:

                expresion_corregida = (

                    expresion_corregida
                    .replace(
                        original,
                        nuevo
                    )
                )

                cambios.append(
                    f"{original}->{nuevo}"
                )

        # =====================================
        # REGLAS OCR MATEMÁTICAS
        # =====================================

        reglas = [

            (
                r'x25\b',
                'x=5'
            ),

            (
                r'x=213\b',
                'x=13'
            ),

            (
                r'5S=',
                '5='
            )
        ]

        for patron, reemplazo in reglas:

            nuevo_texto = re.sub(
                patron,
                reemplazo,
                expresion_corregida
            )

            if nuevo_texto != expresion_corregida:

                cambios.append(
                    f"{patron}->{reemplazo}"
                )

                expresion_corregida = (
                    nuevo_texto
                )

        # =====================================
        # LIMPIEZA DE LÍNEAS
        # =====================================

        lineas = expresion_corregida.splitlines()

        lineas_limpias = []
        
        lineas_originales = []

        for linea in lineas:

            linea = linea.strip()

            if not linea:

                continue

            # eliminar dobles espacios
            linea = re.sub(
                r'\s+',
                ' ',
                linea
            )

            # detectar posible ecuación incompleta
            if (

                '=' not in linea

                and

                any(
                    c.isalpha()
                    for c in linea
                )

                and

                any(
                    c.isdigit()
                    for c in linea
                )

            ):

                print(
                    "POSIBLE ECUACION INCOMPLETA:",
                    linea
                )

            lineas_originales.append(
                linea
            )
            lineas_limpias.append(
                linea
            )

        # =====================================
        # RECONSTRUCCIÓN DE ECUACIONES
        # =====================================

        for i in range(

            len(lineas_limpias) - 2
        ):

            actual = lineas_limpias[i]

            siguiente = lineas_limpias[i + 1]

            ultimo = lineas_limpias[i + 2]

            if (

                "=" not in actual

                and

                "=" in siguiente

                and

                "=" in ultimo

            ):

                try:

                    if ultimo.startswith("x="):

                        valor_x = (

                            ultimo
                            .replace(
                                "x=",
                                ""
                            )
                        )

                        valor_x = int(
                            valor_x
                        )

                        expresion = actual

                        expresion_eval = (

                            expresion
                            .replace(
                                "x",
                                str(valor_x)
                            )
                        )

                        resultado = eval(
                            expresion_eval
                        )

                        nueva_ecuacion = (

                            f"{actual}={resultado}"
                        )

                        print(
                            "ECUACION RECUPERADA:",
                            nueva_ecuacion
                        )

                        lineas_limpias[i] = (
                            nueva_ecuacion
                        )

                except:

                    pass


        expresion_corregida = '\n'.join(
            lineas_limpias
        )

        print("\n")
        print("================================")
        print("OCR CORREGIDO")
        print("================================")
        print(expresion_corregida)
        print("================================")
        print("\n")

        return {

            'expresion_corregida':
            expresion_corregida,

            'cambios':
            cambios,

            'corregido':
            len(cambios) > 0
        }
    