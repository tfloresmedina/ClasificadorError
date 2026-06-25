import json

from app.services.analysis_service_gemini import (
    AnalysisServiceGemini
)

with open(
    "resultado_gemini.json",
    "r",
    encoding="utf-8"
) as f:

    ejercicios = json.load(f)

resultado = (
    AnalysisServiceGemini
    .analizar_ejercicios(
        ejercicios
    )
)

for r in resultado:

    print("\n===================")
    print(
        "EJERCICIO",
        r["numero"]
    )
    print("===================")

    print(
        r["validacion"]
    )