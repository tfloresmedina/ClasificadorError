from app import create_app

from app.services.ocr_analysis_pipeline_service import (
    OCRAnalysisPipelineService
)

from app.services.result_view_service import (
    ResultViewService
)


app = create_app()


with app.app_context():


    ruta_imagen = (
        'app/static/test/test_1.png'
    )


    respuesta_correcta = (
        '2*x+2'
    )


    resultado_pipeline = (

        OCRAnalysisPipelineService
        .procesar_respuesta(

            ruta_imagen,

            respuesta_correcta
        )
    )


    resultado_visual = (

        ResultViewService
        .construir_resultado_visual(

            resultado_pipeline[
                'resultado'
            ],

            resultado_pipeline.get(
                'confianza_ocr',
                0
            )
        )
)


    print('\n========== RESULTADO VISUAL ==========\n')


    for clave, valor in resultado_visual.items():

        print(f'{clave}: {valor}')