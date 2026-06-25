import os
import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

modelo = genai.GenerativeModel(
    "gemini-2.5-flash"
)

respuesta = modelo.generate_content(
    "Responde solamente: FUNCIONA"
)

print(respuesta.text)