import re


class ExerciseDetectorService:

    @staticmethod
    def detectar_ejercicios(texto):

        if not texto:
            return []
        # =====================================
        # NORMALIZAR NUMERACIÓN DE EJERCICIOS
        # =====================================

        texto = re.sub(
            r'(\d+\))',
            r'\n\1',
            texto
        )

        texto = re.sub(
            r'\n+',
            '\n',
            texto
        )
        texto = texto.replace("①", "\n① ")
        texto = texto.replace("②", "\n② ")
        texto = texto.replace("③", "\n③ ")
        texto = texto.replace("④", "\n④ ")
        texto = texto.replace("⑤", "\n⑤ ")
        texto = texto.replace("⑥", "\n⑥ ")
        texto = texto.replace("⑦", "\n⑦ ")
        texto = texto.replace("⑧", "\n⑧ ")
        texto = texto.replace("⑨", "\n⑨ ")
        texto = texto.replace("⑩", "\n⑩ ")
        lineas = [
            l.strip()
            for l in texto.split("\n")
            if l.strip()
        ]

        ejercicios = []
        print("\n===== TEXTO OCR =====")
        print(texto)
        print("=====================\n")
        ejercicio_actual = []

                
        inicio_examen = False
        for linea in lineas:
         
            if re.match(
                r'^(\d+[\)\.]|[①②③④⑤⑥⑦⑧⑨⑩])',
                linea.strip()
            ):
                inicio_examen = True

                if not inicio_examen:
                    continue

                if ejercicio_actual:

                   
                    ejercicios.append(
                        ejercicio_actual
                    )

                ejercicio_actual = []

                linea = re.sub(
                    r'^(\d+\)|[①②③④⑤⑥⑦⑧⑨⑩])',
                    '',
                    linea
                ).strip()

                if linea:

                   

                    ejercicio_actual.append(
                        linea
                    )

                continue

            # línea normal
            

            ejercicio_actual.append(
                linea
            )

        # fuera del for
        if ejercicio_actual:

            ejercicios.append(
                ejercicio_actual
            )

            # Eliminar ejercicios vacíos
        ejercicios = [

            e

            for e in ejercicios

            if len(e) > 0
        ]

        ejercicios = [

        e

        for e in ejercicios

        if not (
            len(e) == 1
            and
            "PRUEBA DE" in e[0].upper()
        )
    ]

        print("\n=====================")
        print("EJERCICIOS DETECTADOS")
        print("=====================")


        print("\n===== EJERCICIOS CRUDOS =====")
        for i, ejercicio in enumerate(
            ejercicios,
            start=1
        ):

            print(f"\nEJERCICIO {i}")

            for paso in ejercicio:
                print(paso)

        print("\n=====================\n")

        return ejercicios