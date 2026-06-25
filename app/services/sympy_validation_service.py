from sympy import (
    sympify,
    simplify,
    symbols,
    Eq,
    solve
)

from sympy.core.sympify import (
    SympifyError
)


class SympyValidationService:


    @staticmethod
    def validar_equivalencia(
        expresion_1,
        expresion_2
    ):

        try:

            expr1 = sympify(
                expresion_1
            )

            expr2 = sympify(
                expresion_2
            )

            resultado = simplify(
                expr1 - expr2
            ) == 0

            return {

                'valido': True,

                'equivalente': resultado,

                'expr1': str(expr1),

                'expr2': str(expr2)
            }

        except SympifyError:

            return {

                'valido': False,

                'equivalente': False,

                'error':
                'Error de interpretación algebraica'
            }

        except Exception as e:

            return {

                'valido': False,

                'equivalente': False,

                'error': str(e)
            }


    @staticmethod
    def validar_simplificacion(
        expresion_1,
        expresion_2
    ):

        try:

            expr1 = simplify(
                sympify(
                    expresion_1
                )
            )

            expr2 = simplify(
                sympify(
                    expresion_2
                )
            )

            return {

                "valido": True,

                "equivalente":
                expr1 == expr2,

                "resultado_1":
                str(expr1),

                "resultado_2":
                str(expr2)
            }

        except Exception as e:

            return {

                "valido": False,

                "equivalente": False,

                "error": str(e)
            }


    @staticmethod
    def validar_operacion(
        expresion_1,
        expresion_2
    ):

        try:

            resultado_1 = (

                sympify(
                    expresion_1
                )
                .evalf()
            )

            resultado_2 = (

                sympify(
                    expresion_2
                )
                .evalf()
            )

            return {

                "valido": True,

                "equivalente":

                    resultado_1 ==
                    resultado_2,

                "resultado_1":
                str(resultado_1),

                "resultado_2":
                str(resultado_2)
            }

        except Exception as e:

            return {

                "valido": False,

                "equivalente": False,

                "error": str(e)
            }
    
    @staticmethod
    def validar_ecuaciones(
        ecuacion_1,
        ecuacion_2
    ):

        try:

            if "=" not in ecuacion_1:

                return {

                    "valido": False,

                    "error":
                    "ecuacion_1 invalida"
                }

            if "=" not in ecuacion_2:

                return {

                    "valido": False,

                    "error":
                    "ecuacion_2 invalida"
                }

            x = symbols('x')

            izq1, der1 = (

                ecuacion_1.split("=")
            )

            izq2, der2 = (

                ecuacion_2.split("=")
            )

            solucion_1 = solve(

                Eq(

                    sympify(izq1),

                    sympify(der1)

                ),

                x
            )

            solucion_2 = solve(

                Eq(

                    sympify(izq2),

                    sympify(der2)

                ),

                x
            )

            return {

                "valido": True,

                "equivalente":

                    solucion_1 ==
                    solucion_2,

                "solucion_1":
                str(solucion_1),

                "solucion_2":
                str(solucion_2)
            }

        except Exception as e:

            return {

                "valido": False,

                "equivalente": False,

                "error": str(e)
            }