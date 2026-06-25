import re


class MathMetadataService:


    @staticmethod
    def obtener_variables(
        texto
    ):

        if not texto:

            return []

        variables = re.findall(
            r'[a-zA-Z]',
            texto
        )

        return sorted(
            list(
                set(variables)
            )
        )


    @staticmethod
    def contar_ecuaciones(
        texto
    ):

        if not texto:

            return 0

        return texto.count('=')


    @staticmethod
    def contar_operaciones(
        texto
    ):

        if not texto:

            return 0

        total = 0

        total += texto.count('+')
        total += texto.count('-')
        total += texto.count('*')
        total += texto.count('/')

        return total