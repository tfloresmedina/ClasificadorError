class CompetencyMappingService:


    @staticmethod
    def obtener_competencia(
        tipo_ejercicio
    ):


        mapa = {


            'ecuacion':

            'Resuelve problemas '
            'de regularidad, '
            'equivalencia y cambio.',


            'simplificacion':

            'Resuelve problemas '
            'de regularidad, '
            'equivalencia y cambio.',


            'operaciones':

            'Resuelve problemas '
            'de cantidad.',


            'fracciones':

            'Resuelve problemas '
            'de cantidad.',


            'proporcionalidad':

            'Resuelve problemas '
            'de gestión de datos.',


            'geometria':

            'Resuelve problemas '
            'de forma, movimiento '
            'y localización.'
        }


        return mapa.get(

            tipo_ejercicio,

            'Competencia matemática '
            'general.'
        )