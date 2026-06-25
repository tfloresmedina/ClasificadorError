from app.services.math_normalizer_service import (
    MathNormalizerService
)


class ModelComparisonService:


    @staticmethod
    def comparar_procedimientos(

        procedimiento_modelo,

        procedimiento_alumno
    ):

        if not procedimiento_modelo:

            return {

                "coincidencia": 0,

                "paso_error": None,

                "esperado": None,

                "obtenido": None,

                "tipo_error":
                "sin_modelo"
            }

        pasos_modelo = list(
            procedimiento_modelo
        )

        pasos_alumno = list(
            procedimiento_alumno
        )

        total = max(
            len(pasos_modelo),
            1
        )

        correctos = 0

        for i in range(

            min(

                len(pasos_modelo),

                len(pasos_alumno)
            )
        ):

            paso_modelo = (

                MathNormalizerService
                .normalizar_expresion(

                    str(
                        pasos_modelo[i]
                    )
                )
            )

            paso_alumno = (

                MathNormalizerService
                .normalizar_expresion(

                    str(
                        pasos_alumno[i]
                    )
                )
            )

            if paso_modelo == paso_alumno:

                correctos += 1

            else:

                return {

                    "coincidencia":

                    round(

                        (
                            correctos
                            /
                            total
                        )
                        * 100,

                        2
                    ),

                    "paso_error":
                    i + 1,

                    "esperado":
                    pasos_modelo[i],

                    "obtenido":
                    pasos_alumno[i],

                    "tipo_error":
                    "desviacion_modelo"
                }

        # =====================================
        # PASOS OMITIDOS
        # =====================================

        if len(
            pasos_alumno
        ) < len(
            pasos_modelo
        ):

            return {

                "coincidencia":

                round(

                    (
                        len(
                            pasos_alumno
                        )
                        /
                        total
                    )
                    * 100,

                    2
                ),

                "paso_error":
                len(
                    pasos_alumno
                ) + 1,

                "esperado":

                    pasos_modelo[
                        len(
                            pasos_alumno
                        )
                    ],

                "obtenido":
                "paso_omitido",

                "tipo_error":
                "omision_paso"
            }

        # =====================================
        # PASOS ADICIONALES
        # =====================================

        if len(
            pasos_alumno
        ) > len(
            pasos_modelo
        ):

            return {

                "coincidencia": 100,

                "paso_error":
                len(
                    pasos_modelo
                ) + 1,

                "esperado":
                "fin_modelo",

                "obtenido":

                    pasos_alumno[
                        len(
                            pasos_modelo
                        )
                    ],

                "tipo_error":
                "paso_extra"
            }

        return {

            "coincidencia": 100,

            "paso_error":
            None,

            "esperado":
            None,

            "obtenido":
            None,

            "tipo_error":
            None
        }