import re


class ASTValidationService:


    @staticmethod
    def expresion_valida(expresion):

        if not expresion:

            return False


        # caracteres permitidos

        patron = r'^[0-9a-zA-Z+\-*/().= ]+$'


        if not re.match(
            patron,
            expresion
        ):

            return False


        # operadores repetidos inválidos

        operadores_invalidos = [

            '+++',
            '++',
            '--',
            '//',
            '///',
            '**+',
            '==',
            '..',
            '/*',
            '*/',
            '+*',
            '*+',
            '/+',
            '+/',
            '=+',
            '=*'
        ]


        for op in operadores_invalidos:

            if op in expresion:

                return False

         # validar inicio inválido

        caracteres_invalidos_inicio = [

            '*',
            '/',
            '=',
            ')'
        ]


        if expresion[0] in (
            caracteres_invalidos_inicio
        ):

            return False
        
         # validar final inválido

        caracteres_invalidos_final = [

            '+',
            '-',
            '*',
            '/',
            '=',
            '('
        ]


        if expresion[-1] in (
            caracteres_invalidos_final
        ):

            return False
        
        # paréntesis balanceados

        abiertos = expresion.count('(')

        cerrados = expresion.count(')')


        if abiertos != cerrados:

            return False


        return True