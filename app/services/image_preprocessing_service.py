import cv2
import os


class ImagePreprocessingService:


    @staticmethod
    def preprocessar_imagen(
        ruta_imagen
    ):

        try:

            # =============================================
            # LEER IMAGEN
            # =============================================

            imagen = cv2.imread(
                ruta_imagen
            )

            if imagen is None:

                raise Exception(
                    "No se pudo leer la imagen."
                )

            # =============================================
            # ESCALA GRISES
            # =============================================

            gris = cv2.cvtColor(

                imagen,

                cv2.COLOR_BGR2GRAY
            )

            # =============================================
            # AUMENTAR TAMAÑO
            # =============================================

            alto, ancho = gris.shape

            if ancho < 1500:

                gris = cv2.resize(

                    gris,

                    None,

                    fx=3,

                    fy=3,

                    interpolation=cv2.INTER_CUBIC
                )

            # =============================================
            # CLAHE (MEJOR CONTRASTE)
            # =============================================

            clahe = cv2.createCLAHE(

                clipLimit=2.0,

                tileGridSize=(8,8)
            )

            gris = clahe.apply(
                gris
            )

            # =============================================
            # REDUCCIÓN DE RUIDO
            # =============================================

            gris = cv2.GaussianBlur(

                gris,

                (3,3),

                0
            )

            # =============================================
            # BINARIZACIÓN OTSU
            # =============================================

            _, binaria = cv2.threshold(

                gris,

                0,

                255,

                cv2.THRESH_BINARY +
                cv2.THRESH_OTSU
            )

            # =============================================
            # GUARDAR IMAGEN PROCESADA
            # =============================================

            nombre, extension = os.path.splitext(
                ruta_imagen
            )

            ruta_procesada = (

                f"{nombre}_procesada{extension}"
            )

            cv2.imwrite(

                ruta_procesada,

                binaria
            )

            print("\n")
            print("================================")
            print("IMAGEN ORIGINAL")
            print(ruta_imagen)
            print("================================")
            print("IMAGEN PROCESADA")
            print(ruta_procesada)
            print("================================")
            print("\n")

            return {

                'valido': True,

                'ruta_procesada':
                    ruta_procesada
            }

        except Exception as e:

            return {

                'valido': False,

                'error': str(e)
            }
        # =============================================
        # MORFOLOGÍA SUAVE
        # =============================================

        kernel = cv2.getStructuringElement(

            cv2.MORPH_RECT,

            (1,1)
        )

        binaria = cv2.morphologyEx(

            binaria,

            cv2.MORPH_OPEN,

            kernel
        )