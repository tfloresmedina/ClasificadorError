import re


class VariableValidationService:


    @staticmethod
    def obtener_variables(texto):

        if not texto:
            return []

        variables = re.findall(
            r'[a-zA-Z]',
            str(texto)
        )

        return list(
            set(variables)
        )


    @staticmethod
    def variables_validas(
        respuesta_alumno,
        respuesta_correcta
    ):


        variables_alumno = (

            VariableValidationService
            .obtener_variables(
                respuesta_alumno
            )
        )


        variables_correctas = (

            VariableValidationService
            .obtener_variables(
                respuesta_correcta
            )
        )


        return (

            variables_alumno
            ==
            variables_correctas
        )