class ResultViewService:


    @staticmethod
    def construir_resultado_visual(
        resultado,
        confianza_ocr=0
    ):


        return {

            'estado':

                'Correcto'

                if resultado.get(
                    'correcto'
                )

                else

                'Incorrecto',


            'tipo_error':

                resultado.get(
                    'tipo_error'
                ),


            'descripcion':

                resultado.get(
                    'descripcion'
                ),


            'recomendacion':

                resultado.get(
                    'recomendacion'
                ),


            'expresion_original':

                resultado.get(
                    'expresion_original'
                ),


            'expresion_normalizada':

                resultado.get(
                    'expresion_normalizada'
                ),


            'expresion_sympy':

                resultado.get(
                    'expresion_sympy'
                ),


            'nivel_confianza':

                resultado.get(
                    'nivel_confianza'
                ),


            'confianza_ocr':

                confianza_ocr,


            'alerta_ocr':

                ResultViewService
                .generar_alerta_ocr(
                    confianza_ocr
                )
        }


    @staticmethod
    def generar_alerta_ocr(
        confianza
    ):


        if confianza >= 85:

            return (
                'Lectura OCR confiable.'
            )


        if confianza >= 60:

            return (
                'Lectura OCR aceptable.'
            )


        return (
            'OCR con baja confianza. '
            'Verificar imagen.'
        )