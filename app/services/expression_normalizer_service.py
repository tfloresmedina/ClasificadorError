import re


class ExpressionNormalizerService:


    @staticmethod
    def normalizar(
        expresion
    ):


        expresion = (
            expresion.lower()
        )


        expresion = (
            expresion.replace(
                ' ',
                ''
            )
        )


        # MULTIPLICACIÓN ENTRE NÚMERO Y VARIABLE

        expresion = re.sub(

            r'(\d)([a-z])',

            r'\1*\2',

            expresion
        )


        # MULTIPLICACIÓN ENTRE VARIABLE Y VARIABLE

        expresion = re.sub(

            r'([a-z])([a-z])',

            r'\1*\2',

            expresion
        )


        # MULTIPLICACIÓN ENTRE NÚMERO Y PARÉNTESIS

        expresion = re.sub(

            r'(\d)\(',

            r'\1*(',

            expresion
        )


        # MULTIPLICACIÓN ENTRE VARIABLE Y PARÉNTESIS

        expresion = re.sub(

            r'([a-z])\(',

            r'\1*(',

            expresion
        )


        # MULTIPLICACIÓN ENTRE PARÉNTESIS

        expresion = re.sub(

            r'\)\(',

            r')*(',

            expresion
        )


        return expresion