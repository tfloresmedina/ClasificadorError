class ErrorSeverityService:


    @staticmethod
    def obtener_severidad(
        tipo_error
    ):


        severidades = {


            'ocr_vacio':
            'baja',


            'ocr_insuficiente':
            'baja',


            'error_signos':
            'media',


            'error_distributiva':
            'media',


            'error_jerarquia':
            'media',


            'terminos_incompletos':
            'media',


            'multiplicacion_incorrecta':
            'media',


            'variables_invalidas':
            'alta',


            'division_cero':
            'alta',


            'operador_invalido':
            'alta',


            'estructura_invalida':
            'alta',


            'error_algebraico':
            'alta'
        }


        return severidades.get(
            tipo_error,
            'media'
        )