import re


class IncompleteEquationRecoveryService:


    @staticmethod
    def recuperar(

        ejercicios,
        procedimiento_modelo=None
    ):

        ejercicios_recuperados = []

        for indice, ejercicio in enumerate(
            ejercicios
        ):

            ejercicio_corregido = []

            pasos_modelo = []

            if (
                procedimiento_modelo
                and
                indice < len(
                    procedimiento_modelo
                )
            ):

                pasos_modelo = (

                    procedimiento_modelo[
                        indice
                    ].get(
                        "pasos",
                        []
                    )
                )

            for i, linea in enumerate(
                ejercicio
            ):

                linea = linea.strip()

                # =========================================
                # SI YA ES ECUACIÓN VÁLIDA
                # =========================================

                if "=" in linea:

                    ejercicio_corregido.append(
                        linea
                    )

                    continue

                # =========================================
                # ECUACIÓN INCOMPLETA
                # =========================================

                recuperada = linea

                if i < len(
                    pasos_modelo
                ):

                    modelo = pasos_modelo[i]

                    izquierda_modelo = (
                        modelo.split("=")[0]
                    )

                    izquierda_linea = (
                        re.sub(
                            r"\s+",
                            "",
                            linea
                        )
                    )

                    izquierda_modelo = (
                        re.sub(
                            r"\s+",
                            "",
                            izquierda_modelo
                        )
                    )

                    # =====================================
                    # MISMO PATRÓN
                    # =====================================

                    if (
                        izquierda_linea
                        ==
                        izquierda_modelo
                    ):

                        recuperada = modelo

                        print(
                            "\n================================"
                        )

                        print(
                            "ECUACION RECUPERADA"
                        )

                        print(
                            f"ORIGINAL: {linea}"
                        )

                        print(
                            f"RECUPERADA: {recuperada}"
                        )

                        print(
                            "================================\n"
                        )

                ejercicio_corregido.append(
                    recuperada
                )

            ejercicios_recuperados.append(
                ejercicio_corregido
            )

        return ejercicios_recuperados