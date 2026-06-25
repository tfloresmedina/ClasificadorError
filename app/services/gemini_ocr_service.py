import os
import re
import google.generativeai as genai


class GeminiOCRService:

    @staticmethod
    def extraer_texto(ruta_imagen):

        try:

            genai.configure(
                api_key=os.getenv(
                    "GEMINI_API_KEY"
                )
            )

            modelo = genai.GenerativeModel(
                "gemini-2.5-flash"
            )

            extension = os.path.splitext(
                ruta_imagen
            )[1].lower()

            mime_type = "image/png"

            if extension == ".jpg":
                mime_type = "image/jpeg"

            elif extension == ".jpeg":
                mime_type = "image/jpeg"

            elif extension == ".pdf":
                mime_type = "application/pdf"

            with open(
                ruta_imagen,
                "rb"
            ) as archivo:

                contenido = archivo.read()

            respuesta = modelo.generate_content([

                """
                Extrae exactamente el contenido del examen.

                Conserva:
                - numeración
                - operaciones
                - ecuaciones
                - resultados
                - procedimientos

                No expliques nada.
                No agregues texto extra.
                """,

                {
                    "mime_type": mime_type,
                    "data": contenido
                }
            ])

            texto = respuesta.text.strip()

            texto = re.sub(
                r'[ \t]+',
                ' ',
                texto
            )

            return {

                "valido": True,

                "texto": texto,

                "confianza": 99
            }

        except Exception as e:

            print(
                "ERROR GEMINI:",
                str(e)
            )

            return {

                "valido": False,

                "error": str(e)
            }