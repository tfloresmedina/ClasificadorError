import re


class MathNormalizerService:


    @staticmethod
    def normalizar_expresion(texto):

        if not texto:

            return ''


        texto = texto.strip()


        # símbolos matemáticos

        reemplazos = {

            '×': '*',
            '÷': '/',
            '^': '**',
            '−': '-',
            ',': '.'
        }


        for origen, destino in reemplazos.items():

            texto = texto.replace(
                origen,
                destino
            )


        # eliminar espacios duplicados

        texto = re.sub(
            r'\s+',
            ' ',
            texto
        )


        # multiplicación implícita

        # 2x -> 2*x

        texto = re.sub(
            r'(\d)([a-zA-Z])',
            r'\1*\2',
            texto
        )


        # 2(x+1) -> 2*(x+1)

        texto = re.sub(
            r'(\d)\(',
            r'\1*(',
            texto
        )


        # x(x+1) -> x*(x+1)

        texto = re.sub(
            r'([a-zA-Z])\(',
            r'\1*(',
            texto
        )


        # )( -> )*(

        texto = re.sub(
            r'\)\(',
            r')*(',
            texto
        )
        
        texto = re.sub(
        r'([+\-*/])\n(\d)',
        r'\1\2',
        texto
        )


        texto = re.sub(
            r"(\d+)\s+(\d+)/(\d+)",
            lambda m: str(
                (
                    int(m.group(1))
                    * int(m.group(3))
                    +
                    int(m.group(2))
                )
            ) + "/" + m.group(3),
            texto
        )

        # limpiar espacios finales

        texto = texto.replace(
            ' ',
            ''
        )


        return texto