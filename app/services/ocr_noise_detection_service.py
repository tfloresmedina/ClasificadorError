class OCRNoiseDetectionService:


    @staticmethod
    def detectar_ruido(
        expresion
    ):


        simbolos_sospechosos = [

            'O',
            'I',
            'l',
            'S'
        ]


        encontrados = []


        for simbolo in (
            simbolos_sospechosos
        ):

            if simbolo in expresion:

                encontrados.append(
                    simbolo
                )


        return {

            'ruido_detectado':

                len(encontrados) > 0,

            'simbolos':
                encontrados
        }