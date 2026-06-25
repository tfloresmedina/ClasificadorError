from app.services.gemini_exam_service import (
    GeminiExamService
)

ruta_pdf = r"uploads\CamScanner 01-06-2026 15.39 (1).pdf"

resultado_ocr = (
    GeminiExamService
    .extraer_ejercicios(
        ruta_pdf
    )
)

print("\n===== RESULTADO GEMINI =====\n")

if resultado_ocr.get("valido"):

    ejercicios = resultado_ocr.get(
        "ejercicios",
        []
    )

    print(
        f"TOTAL EJERCICIOS: {len(ejercicios)}"
    )

    print("\n====================\n")
    for ejercicio in ejercicios:

            print(
                ejercicio.keys()
            )

            break

    for ejercicio in ejercicios:

        print(
        f"EJERCICIO {ejercicio.get('exercise_number')}"
    )

    print("\nENUNCIADO:")

    print(
        ejercicio.get(
            "problem_statement"
        )
    )

    print("\nRESPUESTA FINAL:")

    print(
        ejercicio.get(
            "final_answer"
        )
    )

    print("\nPASOS:")

    for paso in ejercicio.get(
        "solution_steps",
        []
    ):

        print("-", paso)

    print(
        "\n" + "=" * 60 + "\n"
    )