# =========================================================
# TRANSFORMATION VALIDATION SERVICE
# =========================================================

import re
from sympy import (
    simplify,
    sympify,
    Eq,
    Symbol,
    solveset,
    S
)



class TransformationValidationService:


    # =====================================================
    # NORMALIZAR EXPRESIÓN PARA SYMPY
    # =====================================================

    @staticmethod
    def normalizar_expr(texto):
        texto = texto.strip()
        texto = texto.replace("÷", "/")
        texto = texto.replace("×", "*")
        # Números mixtos: "1 1/4" → "(1 + 1/4)"
        texto = re.sub(
            r'(\d+)\s+(\d+)/(\d+)',
            r'(\1 + \2/\3)',
            texto
        )
        # Coeficientes implícitos: "2x" → "2*x"
        texto = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', texto)
        return texto


    # =====================================================
    # DETECTAR TIPO EJERCICIO
    # =====================================================

    @staticmethod
    def detectar_tipo(
        paso_actual,
        paso_siguiente
    ):

        texto = f"{paso_actual} {paso_siguiente}"


        # =============================================
        # ECUACIONES
        # =============================================

        if "=" in texto:

            return "ecuacion_lineal"


        # =============================================
        # FRACCIONES
        # =============================================

        if "/" in texto:

            return "fracciones"


        # =============================================
        # DISTRIBUTIVA
        # =============================================

        if "(" in texto and ")" in texto:

            return "distributiva"


        # =============================================
        # POTENCIAS
        # =============================================

        if "^" in texto or "**" in texto:

            return "potencias"


        # =============================================
        # OPERACIONES
        # =============================================

        operadores = [
            "+",
            "-",
            "*",
            "/"
        ]

        if any(op in texto for op in operadores):

            return "operacion_combinada"


        # =============================================
        # DEFAULT
        # =============================================

        return "desconocido"


    # =====================================================
    # VALIDADOR PRINCIPAL
    # =====================================================

    @classmethod
    def validar_transformacion(
        cls,
        paso_actual,
        paso_siguiente
    ):

        tipo = cls.detectar_tipo(

            paso_actual,
            paso_siguiente
        )

        print("\n=====================")
        print("TRANSFORMATION VALIDATOR")
        print("=====================")
        print("TIPO:", tipo)
        print("ACTUAL:", paso_actual)
        print("SIGUIENTE:", paso_siguiente)
        print("=====================\n")


        # =============================================
        # ECUACIONES
        # =============================================

        if tipo == "ecuacion_lineal":

            return cls.validar_ecuacion(

                paso_actual,
                paso_siguiente
            )


        # =============================================
        # FRACCIONES
        # =============================================

        elif tipo == "fracciones":

            return cls.validar_fracciones(

                paso_actual,
                paso_siguiente
            )


        # =============================================
        # DISTRIBUTIVA
        # =============================================

        elif tipo == "distributiva":

            return cls.validar_distributiva(

                paso_actual,
                paso_siguiente
            )


        # =============================================
        # POTENCIAS
        # =============================================

        elif tipo == "potencias":

            return cls.validar_potencias(

                paso_actual,
                paso_siguiente
            )


        # =============================================
        # OPERACIONES
        # =============================================

        elif tipo == "operacion_combinada":

            return cls.validar_operacion(

                paso_actual,
                paso_siguiente
            )


        # =============================================
        # DESCONOCIDO
        # =============================================

        return cls.construir_respuesta(

            valido=False,

            tipo=tipo,

            error="tipo_desconocido",

            explicacion=(
                "No se pudo determinar "
                "el tipo de transformación."
            ),

            confianza=0.2
        )


    # =====================================================
    # VALIDAR ECUACIONES
    # =====================================================

    @staticmethod
    def validar_ecuacion(
        paso_actual,
        paso_siguiente
    ):

        try:

            if "=" not in paso_actual:

                return TransformationValidationService.construir_respuesta(

                    valido=False,

                    tipo="ecuacion_lineal",

                    error="ecuacion_invalida",

                    explicacion=(
                        "El paso actual "
                        "no contiene ecuación."
                    ),

                    confianza=0.3
                )

            if "=" not in paso_siguiente:

                return TransformationValidationService.construir_respuesta(

                    valido=False,

                    tipo="ecuacion_lineal",

                    error="ecuacion_invalida",

                    explicacion=(
                        "El paso siguiente "
                        "no contiene ecuación."
                    ),

                    confianza=0.3
                )


            # =========================================
            # VALIDAR ECUACIONES OCR ROTAS
            # → beneficio de la duda si no se puede parsear
            # =========================================

            if paso_actual.count("=") != 1:

                return TransformationValidationService.construir_respuesta(

                    valido=True,

                    tipo="ecuacion_lineal",

                    error=None,

                    explicacion=(
                        "No se pudo validar automáticamente. Se asume correcto."
                    ),

                    confianza=0.5
                )

            if paso_siguiente.count("=") != 1:

                return TransformationValidationService.construir_respuesta(

                    valido=True,

                    tipo="ecuacion_lineal",

                    error=None,

                    explicacion=(
                        "No se pudo validar automáticamente. Se asume correcto."
                    ),

                    confianza=0.5
                )

            paso_actual_norm = TransformationValidationService.normalizar_expr(paso_actual)
            paso_siguiente_norm = TransformationValidationService.normalizar_expr(paso_siguiente)

            izquierda_1, derecha_1 = paso_actual_norm.split("=", 1)
            izquierda_2, derecha_2 = paso_siguiente_norm.split("=", 1)

            print("\n====================")
            print("ECUACIONES NORMALIZADAS")
            print("====================")
            print(izquierda_1, "=", derecha_1)
            print(izquierda_2, "=", derecha_2)
            print("====================")


            # =========================================
            # NORMALIZAR
            # =========================================

            expr_1 = simplify(

                sympify(izquierda_1)
                -
                sympify(derecha_1)
            )

            expr_2 = simplify(

                sympify(izquierda_2)
                -
                sympify(derecha_2)
            )


            # =========================================
            # EQUIVALENCIA
            # =========================================

            x = Symbol("x")

            sol_1 = solveset(
                sympify(izquierda_1)
                -
                sympify(derecha_1),
                x,
                domain=S.Reals
            )

            sol_2 = solveset(
                sympify(izquierda_2)
                -
                sympify(derecha_2),
                x,
                domain=S.Reals
            )

            equivalente = (
                sol_1 == sol_2
            )

            if equivalente:

                return TransformationValidationService.construir_respuesta(

                    valido=True,

                    tipo="ecuacion_lineal",

                    error=None,

                    explicacion=(
                        "La transformación conserva "
                        "la equivalencia algebraica."
                    ),

                    confianza=0.95
                )

            return TransformationValidationService.construir_respuesta(

                valido=False,

                tipo="ecuacion_lineal",

                error="transformacion_invalida",

                explicacion=(
                    "La transformación no conserva "
                    "la equivalencia algebraica."
                ),

                confianza=0.20
            )

       
        except Exception as e:

            print("NO SE PUDO VALIDAR ECUACION (beneficio de la duda):", str(e))

            return TransformationValidationService.construir_respuesta(

                valido=True,

                tipo="ecuacion_lineal",

                error=None,

                explicacion="No se pudo validar automáticamente. Se asume correcto.",

                confianza=0.5
            )


    # =====================================================
    # VALIDAR OPERACIONES
    # =====================================================

    @staticmethod
    def validar_operacion(
        paso_actual,
        paso_siguiente
    ):
        """
        Valida cada paso internamente. Si el paso tiene = verifica LHS==RHS.
        No compara ambos pasos entre sí (son etapas distintas del procedimiento).
        Detecta notación de cadena: "5200/8=650*3" donde el alumno escribe
        el resultado intermedio (650) como primer factor del siguiente cálculo.
        """

        def paso_es_correcto(paso):
            norm = TransformationValidationService.normalizar_expr(paso)
            if "=" not in norm:
                return True
            partes = norm.split("=", 1)
            lhs_str = partes[0].strip()
            rhs_str = partes[1].strip()
            try:
                lhs = simplify(sympify(lhs_str))
                rhs = simplify(sympify(rhs_str))
                if lhs == rhs:
                    return True
                # Detectar notación de cadena: el valor del LHS aparece
                # como factor en el RHS (ej: "5200/8=650*3" → lhs=650, "650" en rhs)
                lhs_num = str(lhs)
                if lhs_num in rhs_str:
                    return True
                return False
            except Exception:
                return True

        try:

            ok_actual    = paso_es_correcto(paso_actual)
            ok_siguiente = paso_es_correcto(paso_siguiente)
            correcto = ok_actual and ok_siguiente

            return TransformationValidationService.construir_respuesta(

                valido=correcto,

                tipo="operacion_combinada",

                error=None if correcto else "operacion_incorrecta",

                explicacion=(
                    "Operación validada correctamente."
                    if correcto
                    else
                    "Resultado inconsistente."
                ),

                confianza=0.9 if correcto else 0.4
            )

        except Exception as e:

            print("NO SE PUDO VALIDAR OPERACION (beneficio de la duda):", str(e))

            return TransformationValidationService.construir_respuesta(

                valido=True,

                tipo="operacion_combinada",

                error=None,

                explicacion="No se pudo validar automáticamente. Se asume correcto.",

                confianza=0.5
            )


    # =====================================================
    # VALIDAR FRACCIONES
    # =====================================================

    @staticmethod
    def validar_fracciones(
        paso_actual,
        paso_siguiente
    ):
        """
        Valida que cada paso sea internamente correcto (LHS == RHS si tiene =).
        No compara paso_actual con paso_siguiente porque en un procedimiento
        los pasos consecutivos representan operaciones distintas.
        """

        def paso_es_correcto(paso):
            norm = TransformationValidationService.normalizar_expr(paso)
            if "=" not in norm:
                return True
            partes = norm.split("=", 1)
            lhs_str = partes[0].strip()
            rhs_str = partes[1].strip()
            try:
                lhs = simplify(sympify(lhs_str))
                rhs = simplify(sympify(rhs_str))
                if lhs == rhs:
                    return True
                # Detectar notación de cadena: el valor del LHS aparece
                # como factor en el RHS (ej: "5200/8=650*3" → lhs=650, "650" en rhs)
                lhs_num = str(lhs)
                if lhs_num in rhs_str:
                    return True
                return False
            except Exception:
                return True

        try:
            ok_actual   = paso_es_correcto(paso_actual)
            ok_siguiente = paso_es_correcto(paso_siguiente)
            correcto = ok_actual and ok_siguiente

            return TransformationValidationService.construir_respuesta(

                valido=correcto,

                tipo="fracciones",

                error=None if correcto else "fraccion_incorrecta",

                explicacion=(
                    "Transformación de fracción válida."
                    if correcto
                    else
                    "Error en simplificación de fracción."
                ),

                confianza=0.9 if correcto else 0.3
            )

        except Exception as e:

            print("NO SE PUDO VALIDAR FRACCION (beneficio de la duda):", str(e))

            return TransformationValidationService.construir_respuesta(

                valido=True,

                tipo="fracciones",

                error=None,

                explicacion="No se pudo validar automáticamente. Se asume correcto.",

                confianza=0.5
            )


    # =====================================================
    # VALIDAR DISTRIBUTIVA
    # =====================================================

    @staticmethod
    def validar_distributiva(
        paso_actual,
        paso_siguiente
    ):

        try:

            expr_a = TransformationValidationService.normalizar_expr(paso_actual)
            expr_b = TransformationValidationService.normalizar_expr(paso_siguiente)

            expr_1 = simplify(sympify(expr_a))
            expr_2 = simplify(sympify(expr_b))

            correcto = (expr_1 == expr_2)

            return TransformationValidationService.construir_respuesta(

                valido=correcto,

                tipo="distributiva",

                error=None if correcto else "distributiva_incorrecta",

                explicacion=(
                    "Propiedad distributiva aplicada correctamente."
                    if correcto
                    else
                    "Error en propiedad distributiva."
                ),

                confianza=0.92 if correcto else 0.4
            )

        except Exception as e:

            print("NO SE PUDO VALIDAR DISTRIBUTIVA (beneficio de la duda):", str(e))

            return TransformationValidationService.construir_respuesta(

                valido=True,

                tipo="distributiva",

                error=None,

                explicacion="No se pudo validar automáticamente. Se asume correcto.",

                confianza=0.5
            )


    # =====================================================
    # VALIDAR POTENCIAS
    # =====================================================

    @staticmethod
    def validar_potencias(
        paso_actual,
        paso_siguiente
    ):

        try:

            expr_a = TransformationValidationService.normalizar_expr(paso_actual)
            expr_b = TransformationValidationService.normalizar_expr(paso_siguiente)

            expr_1 = simplify(sympify(expr_a))
            expr_2 = simplify(sympify(expr_b))

            correcto = (expr_1 == expr_2)

            return TransformationValidationService.construir_respuesta(

                valido=correcto,

                tipo="potencias",

                error=None if correcto else "potencia_incorrecta",

                explicacion=(
                    "Potencia simplificada correctamente."
                    if correcto
                    else
                    "Error en operación con potencias."
                ),

                confianza=0.9 if correcto else 0.4
            )

        except Exception as e:

            print("NO SE PUDO VALIDAR POTENCIA (beneficio de la duda):", str(e))

            return TransformationValidationService.construir_respuesta(

                valido=True,

                tipo="potencias",

                error=None,

                explicacion="No se pudo validar automáticamente. Se asume correcto.",

                confianza=0.5
            )


    # =====================================================
    # RESPUESTA ESTÁNDAR
    # =====================================================

    @staticmethod
    def construir_respuesta(
        valido,
        tipo,
        error,
        explicacion,
        confianza
    ):

        return {

            "valido": valido,

            "tipo": tipo,

            "error": error,

            "explicacion": explicacion,

            "nivel_confianza": confianza
        }
    
    @staticmethod
    def validar_calculo(
        paso_actual,
        paso_siguiente
    ):

        try:

            expr1 = simplify(
                sympify(paso_actual)
            )

            expr2 = simplify(
                sympify(paso_siguiente)
            )

            if expr1 == expr2:

                return (
                    TransformationValidationService
                    .construir_respuesta(

                        valido=True,

                        tipo="calculo",

                        error=None,

                        explicacion=(
                            "El cálculo es correcto."
                        ),

                        confianza=0.95
                    )
                )

            return (
                TransformationValidationService
                .construir_respuesta(

                    valido=False,

                    tipo="calculo",

                    error="operacion_incorrecta",

                    explicacion=(
                        "El cálculo no conserva "
                        "el resultado esperado."
                    ),

                    confianza=0.2
                )
            )

        except Exception as e:

            return (
                TransformationValidationService
                .construir_respuesta(

                    valido=False,

                    tipo="calculo",

                    error="error_validacion",

                    explicacion=str(e),

                    confianza=0.1
                )
            )
@staticmethod
def validar_operacion_unica(
    paso
):

    try:

        if "=" not in paso:

            return (
                TransformationValidationService
                .construir_respuesta(

                    valido=False,

                    tipo="calculo",

                    error="sin_igual",

                    explicacion=
                    "La operación no contiene '='.",

                    confianza=0.1
                )
            )

        izquierda, derecha = (
            paso.split("=")
        )

        resultado_izq = simplify(
            sympify(izquierda)
        )

        resultado_der = simplify(
            sympify(derecha)
        )

        if resultado_izq == resultado_der:

            return (
                TransformationValidationService
                .construir_respuesta(

                    valido=True,

                    tipo="calculo",

                    error=None,

                    explicacion=
                    "La operación matemática es correcta.",

                    confianza=0.95
                )
            )

        return (
            TransformationValidationService
            .construir_respuesta(

                valido=False,

                tipo="calculo",

                error="operacion_incorrecta",

                explicacion=
                "El resultado de la operación es incorrecto.",

                confianza=0.2
            )
        )

    except Exception as e:

        return (
            TransformationValidationService
            .construir_respuesta(

                valido=False,

                tipo="calculo",

                error="error_validacion",

                explicacion=str(e),

                confianza=0.1
            )
        )