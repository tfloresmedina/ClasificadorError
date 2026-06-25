class ErrorFrequencyService:


    @staticmethod
    def calcular_frecuencia(
        resultados
    ):


        frecuencias = {}


        for resultado in resultados:


            tipo_error = (

                resultado.get(
                    'tipo_error'
                )
            )


            if not tipo_error:
                continue


            if tipo_error not in (
                frecuencias
            ):

                frecuencias[
                    tipo_error
                ] = 0


            frecuencias[
                tipo_error
            ] += 1


        return frecuencias