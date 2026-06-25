class MathematicalConsistencyService:


    @staticmethod
    def validar_consistencia(
        expresion
    ):


        # NO DEBE INICIAR
        # CON OPERADOR

        operadores_inicio = [

            '+',
            '*',
            '/',
            '='
        ]


        if expresion.startswith(

            tuple(
                operadores_inicio
            )
        ):

            return {

                'consistente': False,

                'motivo':
                'inicio_invalido'
            }


        # NO DEBE TERMINAR
        # CON OPERADOR

        operadores_final = [

            '+',
            '-',
            '*',
            '/',
            '='
        ]


        if expresion.endswith(

            tuple(
                operadores_final
            )
        ):

            return {

                'consistente': False,

                'motivo':
                'final_invalido'
            }


        # PARÉNTESIS BALANCEADOS

        if (

            expresion.count('(')

            !=

            expresion.count(')')
        ):

            return {

                'consistente': False,

                'motivo':
                'parentesis_desbalanceados'
            }


        return {

            'consistente': True
        }