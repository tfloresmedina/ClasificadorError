import os
import json
import google.generativeai as genai


class GeminiExamService:

    @staticmethod
    def extraer_ejercicios(ruta_pdf):

        try:

            genai.configure(
                api_key=os.getenv(
                    "GEMINI_API_KEY"
                )
            )

            modelo = genai.GenerativeModel(
                "gemini-2.5-flash"
            )

            with open(
                ruta_pdf,
                "rb"
            ) as archivo:

                contenido = archivo.read()

            prompt = """
Eres un experto en análisis de exámenes matemáticos escolares.

Analiza el examen resuelto y extrae cada ejercicio.

IMPORTANTE:

1. Cada ejercicio debe contener:
   - enunciado
   - pasos de resolución
   - respuesta final

2. Los pasos deben representar transformaciones matemáticas completas.

CORRECTO:

[
    "5/8 + 3/8 = 8/8",
    "8/8 ÷ 2 = 8/16",
    "8/16 = 1/2"
]

INCORRECTO:

[
    "5",
    "8",
    "8/8",
    "1/2"
]

3. Nunca separes números o fracciones que pertenezcan a una misma operación.

4. Si una ecuación continúa en varias líneas del examen, reconstruye la ecuación completa.

5. Conserva exactamente los símbolos matemáticos:
   + - × ÷ = / ( )

6. No inventes pasos.

7. No elimines pasos visibles.

8. Mantén el orden original.

9. Si detectas fracciones verticales, reconstruye la fracción completa.

10. Verifica que la respuesta final coincida con los pasos de resolución.

11. No inventes cantidades o unidades.

12. Si los pasos indican un resultado diferente, utiliza el resultado matemático obtenido en los pasos
13. Si existen símbolos matemáticos ambiguos,
mal escritos, incompletos o difíciles de reconocer
(>, <, ≤, ≥, =, fracciones, exponentes, raíces, etc.),
marca el ejercicio como:

"requires_teacher_review": true

y explica el motivo en:

"review_reason".

14. Nunca asumas un símbolo si no existe suficiente evidencia visual.
15. Mantén completas todas las expresiones matemáticas.

Una expresión matemática nunca debe dividirse en elementos independientes.

CORRECTO:

[
    "1/2 + 1/3 = 5/6"
]

INCORRECTO:

[
    "1/2",
    "1/3",
    "5/6"
]
16. Si la confianza visual es baja, solicita revisión docente.


Formato:

[
  {
    "exercise_number": 1,
    "problem_statement": "",
    "solution_steps": [],
    "final_answer": "",
    "requires_teacher_review": false,
    "review_reason": ""
  }
]

Devuelve únicamente JSON válido.

REGLAS CRÍTICAS:

- NO RESUELVAS los ejercicios.
- NO CORRIJAS los ejercicios.
- NO INTERPRETES los valores.
- TRANSCRIBE exactamente los números visibles.
- Si observas 3/5 debes devolver 3/5.
- Si observas 3/8 debes devolver 3/8.
- Está prohibido sustituir fracciones o números.

Si el ejercicio contiene una única operación compuesta, descompón la resolución en pasos matemáticos equivalentes.

Ejemplo:

17/20 - 6/10

↓

17/20 - 12/20

↓

5/20

↓

1/4

17. Mantén completas todas las comparaciones matemáticas.

CORRECTO:

[
    "13/27 < 1/2"
]

[
    "x > 5"
]

INCORRECTO:

[
    "13/27",
    "1/2"
]
18. Mantén completos los números mixtos, fracciones, potencias, raíces y expresiones algebraicas.

CORRECTO:

[
    "1 1/4 = 5/4"
]

[
    "√16 = 4"
]

[
    "x² + 3x = 10"
]

INCORRECTO:

[
    "1",
    "1/4"
]

[
    "√",
    "16"
]
19. No devuelvas números o fracciones aisladas como pasos matemáticos.

Cada elemento de "solution_steps" debe representar una operación,
transformación, comparación o conclusión completa.

Si no es posible reconstruir la expresión completa:

"requires_teacher_review": true

"""
            with open(
                ruta_pdf,
                "rb"
            ) as archivo:

                contenido = archivo.read()
            # =====================================
            # DETECTAR TIPO DE ARCHIVO
            # =====================================

            extension = os.path.splitext(
                ruta_pdf
            )[1].lower()

            if extension == ".pdf":

                mime = "application/pdf"

            elif extension == ".png":

                mime = "image/png"

            elif extension in [".jpg", ".jpeg"]:

                mime = "image/jpeg"

            else:

                raise Exception(
                    f"Formato no soportado: {extension}"
                )

            print("\n====================")
            print("TIPO ARCHIVO GEMINI")
            print("====================")
            print("ARCHIVO:", ruta_pdf)
            print("MIME:", mime)
            print("====================")

            respuesta = modelo.generate_content([

                
                prompt,

                {
                    "mime_type": mime,

                    "data": contenido
                }
            ])

            texto = respuesta.text.strip()

            texto = texto.replace(
                "```json",
                ""
            )

            texto = texto.replace(
                "```",
                ""
            )

            resultado = json.loads(
                texto
            )

            print("\n====================")
            print("JSON GEMINI")
            print("====================")

            print(
                json.dumps(
                    resultado,
                    indent=4,
                    ensure_ascii=False
                )
            )

            print("====================\n")

            # =====================================
            # LOG CANTIDAD
            # =====================================

            print("\n====================")
            print("TOTAL EJERCICIOS IA")
            print("====================")
            print(len(resultado))
            print("====================")

            # =====================================
            # LOG NUMEROS
            # =====================================

            print("\n====================")
            print("NUMEROS DETECTADOS")
            print("====================")

            for ejercicio in resultado:

                print(
                    "EJERCICIO:",
                    ejercicio.get(
                        "exercise_number"
                    )
                )

            print("====================\n")

            # =====================================
            # LOG DETALLE
            # =====================================

            print("\n====================")
            print("JSON GEMINI CRUDO")
            print("====================")
            for ejercicio in resultado:

                print(
                    "\nEJERCICIO:",
                    ejercicio.get(
                        "exercise_number"
                    )
                )

                print(
                    ejercicio.get(
                        "problem_statement"
                    )
                )

                print(
                    ejercicio.get(
                        "solution_steps"
                    )
                )

                print(
                    ejercicio.get(
                        "final_answer"
                    )
                )

            print("\n====================")
            print("FIN LOG GEMINI")
            print("====================\n")

            return {

                "valido": True,

                "texto": "",

                "ejercicios": resultado
            }
        except Exception as e:

            print(
                "ERROR GEMINI:",
                str(e)
            )

            if "429" in str(e):

                return {
                    "valido": False,
                    "error":
                    "Límite de Gemini alcanzado. Intente más tarde."
                }

            return {
                "valido": False,
                "error": str(e)
            }