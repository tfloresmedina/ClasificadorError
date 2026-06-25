print("CARGANDO ANALYSIS SERVICE GEMINI")
import re

from app.services.procedure_validation_service import (
    ProcedureValidationService
)


class AnalysisServiceGemini:



    @staticmethod
    def analizar_ejercicios(
        ejercicios
    ):

        resultados = []

        for ejercicio in ejercicios:

            numero = (
                ejercicio.get(
                    "exercise_number"
                )
                or ejercicio.get(
                    "number"
                )
                or ejercicio.get(
                    "problem_number"
                )
            )

            pregunta = (
                ejercicio.get(
                    "question"
                )
                or ejercicio.get(
                    "question_text"
                )
                or ejercicio.get(
                    "problem_statement"
                )
                or ""
            )

            solucion = (
                ejercicio.get(
                    "solution"
                )
                or ejercicio.get(
                    "student_solution"
                )
                or "\n".join(
                ejercicio.get(
                    "solution_steps",
                    []
                )
            )
            or "\n".join(
                ejercicio.get(
                    "student_solution_steps",
                    []
                )
            )
            or ""
        )

            respuesta = (
                ejercicio.get(
                    "final_answer"
                )
                or ejercicio.get(
                    "student_final_answer"
                )
                or ""
            )

            pasos = (
                    AnalysisServiceGemini
                    .extraer_pasos(
                        solucion
                    )
                )


        try:

            validacion = (
                ProcedureValidationService
                .validar_pasos(
                    pasos
                )
            )

            # =====================================
            # REVISIÓN DOCENTE GEMINI
            # =====================================
          

            if ejercicio.get(
                "requires_teacher_review",
                False
            ):

                validacion["valido"] = False

                validacion[
                    "requiere_revision"
                ] = True

                validacion[
                    "motivo_revision"
                ] = ejercicio.get(
                    "review_reason",
                    ""
                )

        except Exception as e:

            print(
                "ERROR VALIDACION PROCEDIMIENTO:",
                str(e)
            )

            validacion = {

                "valido": False,

                "motivo": str(e),

                "validaciones": []
            }

            print("\n====================")
            print("EJERCICIO")
            print(numero)

            print("PASOS:")
            print(pasos)

            print("VALIDACION:")
            print(validacion)

            print("====================")

            resultados.append({
                
                "numero":
                numero,

                "pregunta":
                pregunta,

                "pasos":
                pasos,

                "respuesta":
                respuesta,

                "validacion":
                validacion,

                "requires_teacher_review":
                ejercicio.get(
                "requires_teacher_review",
                False
                ),

                "review_reason":
                ejercicio.get(
                "review_reason",
                ""
                )

            })



        return resultados


    @staticmethod
    def extraer_pasos(solucion):

        if not solucion:
            return []

        pasos = []

        for linea in solucion.split("\n"):

            linea = linea.strip()

            if not linea:
                continue
            
            # =====================================
            # LIMPIEZA OCR
            # =====================================

            # Ignorar números sueltos

            if re.fullmatch(
                r"\d+",
                linea
            ):

                print(
                    "DESCARTADO OCR:",
                    linea
                )

                continue

            # Ignorar líneas demasiado cortas

            if len(
                linea.strip()
            ) <= 2:

                print(
                    "DESCARTADO CORTO:",
                    linea
                )

                continue


            print("\n===================")
            print("LINEA OCR")
            print(linea)
            print("===================")

            # Detener cuando se encuentre la respuesta final
            if linea.lower().startswith(
                ("rpta", "respuesta")
            ):

                pasos.append(linea)
                break

            # Ignorar líneas incompletas
            if linea.startswith("="):
                continue

            # Ecuaciones múltiples
            if linea.count("=") > 1:

                partes = [

                    p.strip()

                    for p in linea.split("=")

                    if p.strip()
                ]

                for i in range(
                    len(partes) - 1
                ):

                    pasos.append(

                        partes[i]
                        + " = "
                        + partes[i + 1]
                    )

            else:

                pasos.append(
                    linea
                )

            print(
                "PASO AGREGADO:",
                pasos
            )

        # IMPORTANTE: fuera del for
        return pasos
