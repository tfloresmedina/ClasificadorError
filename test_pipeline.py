from app import create_app

from app.services.ocr_analysis_pipeline_service import (
    OCRAnalysisPipelineService
)


app = create_app()


with app.app_context():


    ruta_imagen = (
        'app/static/test/test_1.png'
    )


    respuesta_correcta = (
        '2*x+2'
    )


    resultado = (
        OCRAnalysisPipelineService
        .procesar_respuesta(

            ruta_imagen,

            respuesta_correcta
        )
    )


    print('\n========== RESULTADO ==========\n')

    print(resultado)