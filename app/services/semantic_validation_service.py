class SemanticValidationService:


    @staticmethod
    def validar_semantica(
        expresion
    ):


        # DIVISIÓN ENTRE CERO

        if '/0' in expresion:

            return {

                'valido': False,

                'tipo_error':
                'division_cero',

                'descripcion':
                'La expresión contiene división entre cero.'
            }


        # PARÉNTESIS VACÍOS

        if '()' in expresion:

            return {

                'valido': False,

                'tipo_error':
                'parentesis_vacios',

                'descripcion':
                'La expresión contiene paréntesis vacíos.'
            }


        # OPERADORES REPETIDOS

        operadores_invalidos = [

            '++',
            '--',
            '**',
            '//'
        ]


        for op in operadores_invalidos:

            if op in expresion:

                return {

                    'valido': False,

                    'tipo_error':
                    'operador_invalido',

                    'descripcion':
                    'La expresión contiene operadores inválidos.'
                }


        return {

            'valido': True
        }