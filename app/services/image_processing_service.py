import cv2

import os

import uuid


class ImageProcessingService:


    @staticmethod
    def procesar_imagen(ruta_imagen):


        imagen = cv2.imread(
            ruta_imagen
        )


        if imagen is None:

            return None


        # escala de grises

        gris = cv2.cvtColor(
            imagen,
            cv2.COLOR_BGR2GRAY
        )


        # reducción de ruido

        blur = cv2.GaussianBlur(
            gris,
            (5, 5),
            0
        )


        # binarización

        binaria = cv2.adaptiveThreshold(

            blur,

            255,

            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

            cv2.THRESH_BINARY,

            11,

            2
        )


        # carpeta salida

        carpeta_salida = (
            'app/static/uploads/procesadas'
        )

        os.makedirs(
            carpeta_salida,
            exist_ok=True
        )


        nombre_archivo = (
            f'{uuid.uuid4()}.png'
        )

        ruta_salida = os.path.join(
            carpeta_salida,
            nombre_archivo
        )


        cv2.imwrite(
            ruta_salida,
            binaria
        )


        return ruta_salida