class RecommendationEngineService:


    @staticmethod
    def generar_recomendacion(
        tipo_error
    ):


        recomendaciones = {


            'error_signos':

                'Reforzar operaciones con signos algebraicos.',


            'error_distributiva':

                'Practicar propiedad distributiva paso a paso.',


            'error_jerarquia':

                'Revisar jerarquía de operaciones matemáticas.',


            'terminos_incompletos':

                'Completar el desarrollo algebraico completo.',


            'multiplicacion_incorrecta':

                'Practicar multiplicación de términos algebraicos.',


            'variables_invalidas':

                'Revisar variables utilizadas en el ejercicio.',


            'division_cero':

                'Evitar divisiones entre cero.',


            'operador_invalido':

                'Corregir operadores matemáticos inválidos.',


            'ocr_vacio':

                'Subir una imagen más clara del ejercicio.',


            'ocr_insuficiente':

                'Verificar legibilidad del contenido matemático.'
        }


        return (

            recomendaciones.get(

                tipo_error,

                'Revisar procedimiento matemático.'
            )
        )