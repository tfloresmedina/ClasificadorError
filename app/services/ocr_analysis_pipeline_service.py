from app.services.image_processing_service import (
    ImageProcessingService
)

from app.services.ocr_service import (
    OCRService
)

from app.services.analysis_service import (
    AnalysisService
)


class OCRAnalysisPipelineService:


    @staticmethod
    def procesar_respuesta(
        ruta_imagen,
        respuesta_correcta
    ):


        # PROCESAMIENTO IMAGEN

        ruta_procesada = (
            ImageProcessingService
            .procesar_imagen(
                ruta_imagen
            )
        )


        if not ruta_procesada:

            return {

                'valido': False,

                'error':
                'No se pudo procesar la imagen.'
            }


        # OCR

        resultado_ocr = (
            OCRService.extraer_texto(
                ruta_procesada
            )
        )


        if not resultado_ocr['valido']:

            return {

                'valido': False,

                'error':
                resultado_ocr['error']
            }


        texto_detectado = (
            resultado_ocr['texto']
        )

        confianza_ocr = (
            resultado_ocr.get(
                'confianza',
                0
            )
        )
        # ANÁLISIS

        resultado_analisis = (
            AnalysisService
            .analizar_respuesta(

                texto_detectado,

                respuesta_correcta
            )
        )


        return {

            'valido': True,

            'ruta_procesada':
            ruta_procesada,

            'texto_ocr':
            texto_detectado,

            'confianza_ocr':
            confianza_ocr,

            'resultado':
            resultado_analisis
        }