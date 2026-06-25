import re
from sympy import (
    symbols,
    sympify,
    simplify
)
from app.services.reasoning_step_classifier import (
    ReasoningStepClassifier
)
from app.services.sympy_validation_service import (
    SympyValidationService
)

from app.services.transformation_validation_service import (
    TransformationValidationService
)
from app.services.error_classifier_service import (
    ErrorClassifierService
)
from app.services.RuleEngineService import( RuleEngineService)
from app.services.rules.curricular_rules import (
    CURRICULAR_RULES
)

class ProcedureValidationService:



    @staticmethod
    def normalizar_operadores(texto):

        texto = texto.replace("÷", "/")
        texto = texto.replace("×", "*")

        texto = re.sub(
            r'(\d)x(\d)',
            r'\1*\2',
            texto
        )

        return texto
    

    @staticmethod
    def es_ecuacion(
        expresion
    ):

        return "=" in expresion


    @staticmethod
    def obtener_lados(
        ecuacion
    ):

        try:

            izquierda, derecha = (

                ecuacion.split("=")
            )

            return (

                izquierda.strip(),
                derecha.strip()
            )

        except:

            return None, None


    @staticmethod
    def ecuaciones_equivalentes(
        ecuacion_1,
        ecuacion_2
    ):

        try:

            x = symbols('x')

            izq1, der1 = (

                ProcedureValidationService
                .obtener_lados(
                    ecuacion_1
                )
            )

            izq2, der2 = (

                ProcedureValidationService
                .obtener_lados(
                    ecuacion_2
                )
            )

             # NUEVO
            izq1 = ProcedureValidationService.normalizar_sympy(izq1)
            der1 = ProcedureValidationService.normalizar_sympy(der1)

            izq2 = ProcedureValidationService.normalizar_sympy(izq2)
            der2 = ProcedureValidationService.normalizar_sympy(der2)

            print("\nANTES DE SYMPY")
            print("IZQ1:", izq1)
            print("DER1:", der1)
            print("IZQ2:", izq2)
            print("DER2:", der2)

            expr1 = simplify(
                    sympify(izq1)
                    -
                    sympify(der1)
                )

            expr2 = simplify(
                sympify(izq2)
                -
                sympify(der2)
            )

            return simplify(
                expr1 - expr2
            ) == 0

        except Exception as e:

            print(
                "ERROR SYMPY:",
                str(e)
            )

            return False


    @staticmethod
    def validar_pasos(
        pasos
    ):

        if len(pasos) < 2:

            return {

                "valido": True,

                "motivo": "ejercicio_un_paso",

                "descripcion":
                    "Ejercicio con una única operación.",

                "cantidad_pasos":
                    len(pasos),

                "validaciones": [

                    {

                        "paso":
                            pasos[0],

                        "tipo":
                            "operacion_unica",

                        "valido":
                            True,

                        "explicacion":
                            "Operación de un solo paso."
                    }

                ]
            }

        validaciones = []

        procedimiento_valido = True

        for i in range(

            len(pasos) - 1
        ):

            paso_actual = pasos[i]

            paso_siguiente = pasos[i + 1]

          
            paso_actual = (
                ProcedureValidationService
                .normalizar_operadores(
                    paso_actual
                )
            )

            paso_siguiente = (
                ProcedureValidationService
                .normalizar_operadores(
                    paso_siguiente
                )
            )

            print("\nNORMALIZADO")
            print(paso_actual)
            print("---->")
            print(paso_siguiente)

            es_ec_actual = (
                ProcedureValidationService
                .es_ecuacion(
                    paso_actual
                )
            )

            es_ec_siguiente = (

                ProcedureValidationService
                .es_ecuacion(
                    paso_siguiente
                )
            )

            tipo_actual = (
            ReasoningStepClassifier
            .clasificar(
                paso_actual
            )
        )

            tipo_siguiente = (
            ReasoningStepClassifier
            .clasificar(
                paso_siguiente
            )
        )
            # =====================================
            # IGNORAR CONCLUSIONES TEXTUALES
            # =====================================

            if tipo_siguiente == "conclusion":

                print(
                    "CONCLUSION DETECTADA:",
                    paso_siguiente
                )

                continue

            print(
            "TIPOS:",
            tipo_actual,
            "->",
            tipo_siguiente
        )


            print(
                "ECUACION:",
                es_ec_actual,
                es_ec_siguiente
            )

            valido = True

            resultado_transformacion = {

                "valido": True,

                "tipo": "sin_validacion",

                "explicacion": "",

                "nivel_confianza": 0,

                "error": None
            }

            error = {

                        "tipo_error": None,

                        "descripcion": "",

                        "recomendacion": "",

                        "fase_polya": "",

                        "severidad": ""
                    }

            if (

                es_ec_actual
                and
                es_ec_siguiente

            ):

                #if not ProcedureValidationService.pasos_relacionados(

                    #paso_actual,
                    #paso_siguiente

                #):

                    resultado_transformacion = (

                        TransformationValidationService
                        .validar_transformacion(

                            paso_actual,
                            paso_siguiente
                    )
                )


                    valido = (

                        resultado_transformacion.get(
                            "valido",
                            False
                        )
                    )
            else:

                    resultado_transformacion = (
                        TransformationValidationService
                        .validar_transformacion(
                            paso_actual,
                            paso_siguiente
                        )
                    )

                    valido = (
                        resultado_transformacion.get(
                            "valido",
                            False
                        )
                    )

                # Detectar tipo de error

                    tipo_error = (

                    RuleEngineService
                    .detectar_error(

                        paso_actual,

                        paso_siguiente,

                        resultado_transformacion
                    )
                )
# =====================================
# RECUPERAR REGLA CURRICULAR
# =====================================
                    regla = CURRICULAR_RULES.get(

                        tipo_error,

                        CURRICULAR_RULES[
                            "tipo_desconocido"
                        ]
                    )

                    print(
                        "ERROR DETECTADO:",
                        resultado_transformacion.get(
                            "error"
                        )
                    )
                    print("\n====================")
                    print("REGLA CURRICULAR")
                    print("====================")
                    print(regla)
                    print("====================\n")

            if not valido:

                procedimiento_valido = False

                error = (

                ErrorClassifierService
                .clasificar_error_procedimiento({

                    "valido":
                        valido,

                    "paso_actual":
                        paso_actual,

                    "paso_siguiente":
                        paso_siguiente
                })
            )

            resultado_transformacion[
                "error"
            ] = error.get(
                "tipo_error"
            )

            resultado_transformacion[
                "explicacion"
            ] = error.get(
                "descripcion"
            )

            resultado_transformacion[
                "recomendacion"
            ] = error.get(
                "recomendacion"
            )

            resultado_transformacion[
                "fase_polya"
            ] = error.get(
                "fase_polya"
            )

            resultado_transformacion[
                "severidad"
            ] = error.get(
                "severidad"
            )

            # ==================================
                # REGLA CURRICULAR
                # ==================================

            tipo_error = (
                    resultado_transformacion.get(
                        "error"
                    )
                    or
                    "sin_error"
                )

            regla = CURRICULAR_RULES.get(

                    tipo_error,

                    CURRICULAR_RULES[
                        "tipo_desconocido"
                    ]
                )
            
            if tipo_actual == "conclusion":

                    resultado_transformacion = {

                    "valido": True,

                    "tipo": "fin_ejercicio",

                    "explicacion":
                        "Se detectó el final del ejercicio.",

                    "nivel_confianza": 1,

                    "error": None
                }


            validaciones.append({
                "tipo_paso_actual":
                tipo_actual,

                "tipo_paso_siguiente":
                    tipo_siguiente,

                "paso_actual":
                paso_actual,

                "paso_siguiente":
                paso_siguiente,

                "valido":
                valido,

                "tipo_transformacion":
                resultado_transformacion.get(
                    "tipo",
                    ""
                ),

                "explicacion":
                resultado_transformacion.get(
                    "explicacion",
                    ""
                ),

                "nivel_confianza":
                resultado_transformacion.get(
                    "nivel_confianza",
                    0
                ),

                "error_detectado":
                resultado_transformacion.get(
                    "error",
                    None
                ),

                "recomendacion":
                resultado_transformacion.get(
                    "recomendacion",
                    ""
                ),

                "fase_polya":
                resultado_transformacion.get(
                    "fase_polya",
                     ""
                ),

                "severidad":
                resultado_transformacion.get(
                    "severidad",
                    ""
                )

                ,

                # ==================================
                # CURRICULAR
                # ==================================

                "competencia":
                regla.get(
                    "competencia",
                    ""
                ),

                "capacidad":
                regla.get(
                    "capacidad",
                    ""
                ),

                "desempeno":
                regla.get(
                    "desempeno",
                    ""
                ),

                "nivel_logro":
                regla.get(
                    "nivel_logro",
                    ""
                ),

                "descripcion_pedagogica":
                regla.get(
                    "descripcion_pedagogica",
                    ""
                ),

                "fortalezas":
                regla.get(
                    "fortalezas",
                    []
                ),

                "debilidades":
                regla.get(
                    "debilidades",
                    []
                ),

                "recomendaciones":
                regla.get(
                    "recomendaciones",
                    []
                )
            })
                
            print(

                "TRANSFORMACION:",

                resultado_transformacion
            )
            print("\n")
            print("====================")
            print("RESULTADO VALIDACIÓN")
            print("====================")
            print(validaciones)
            print("====================")

        return {

            "valido":
            procedimiento_valido,

            "cantidad_pasos":
            len(pasos),

            "validaciones":
            validaciones
        }
    
    @staticmethod
    def pasos_relacionados(
        paso_actual,
        paso_siguiente
    ):

        numeros_actual = set(
            re.findall(r'\d+', paso_actual)
        )

        numeros_siguiente = set(
            re.findall(r'\d+', paso_siguiente)
        )

        coincidencias = (
            numeros_actual.intersection(
                numeros_siguiente
            )
        )

        variables_actual = set(
            re.findall(r'[a-zA-Z]', paso_actual)
        )

        variables_siguiente = set(
            re.findall(r'[a-zA-Z]', paso_siguiente)
        )

        variables_comunes = (
            variables_actual.intersection(
                variables_siguiente
            )
        )

        print("COINCIDEN:", coincidencias)
        print("VARIABLES:", variables_comunes)

        return (
            len(coincidencias) >= 2
            or
            len(variables_comunes) >= 1
        )

@staticmethod
def obtener_resultado_final(pasos):

    if not pasos:
        return None

    ultimo_paso = pasos[-1]

    if "=" in ultimo_paso:

        return ultimo_paso.split("=")[-1].strip()

    return ultimo_paso.strip()