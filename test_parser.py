# test_parser.py

from app.services.exercise_detector_service import (
    ExerciseDetectorService
)

texto = """
1) 1/2 + 1/3 = 5/6

2) 10/2 = 5
5*5 = 25

3) 3/40 = 15
40 = 200
"""

resultado = (
    ExerciseDetectorService
    .detectar_ejercicios(texto)
)

print(resultado)