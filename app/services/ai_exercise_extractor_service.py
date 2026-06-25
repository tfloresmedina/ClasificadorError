import os
import json
import google.generativeai as genai


class AIExerciseExtractorService:

    @staticmethod
    def extraer_ejercicios(texto_ocr):

        try:

            genai.configure(
                api_key=os.getenv(
                    "GEMINI_API_KEY"
                )
            )

            modelo = genai.GenerativeModel(
                "gemini-2.5-flash"
            )

            prompt = f"""
Analiza este OCR de un examen matemático.

Devuelve únicamente JSON válido.

Formato:

{{
  "ejercicios":[
    {{
      "numero":1,
      "pasos":[]
    }}
  ]
}}

OCR:

{texto_ocr}
"""

            respuesta = modelo.generate_content(
                prompt
            )

            print(
                "\n===== RESPUESTA GEMINI =====\n"
            )

            print(
                respuesta.text
            )

            return {

                "ok": True,

                "respuesta":
                    respuesta.text
            }

        except Exception as e:

            return {

                "ok": False,

                "error": str(e)
            }