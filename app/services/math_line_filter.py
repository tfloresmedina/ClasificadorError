import re


class MathLineFilter:
    """
    Elimina encabezados e información administrativa
    que no aporta al análisis matemático.
    """

    PALABRAS_BASURA = [
        "EXAMEN",
        "BIMESTRAL",
        "TRIMESTRAL",
        "COLEGIO",
        "INSTITUCION",
        "EDUCATIVA",
        "NOMBRE",
        "APELLIDOS",
        "ALUMNO",
        "ESTUDIANTE",
        "DOCENTE",
        "PROFESOR",
        "GRADO",
        "SECCION",
        "FECHA",
        "INDICACIONES",
        "DURACION",
        "TIEMPO",
        "DESARROLLA",
        "RESUELVE",
        "PUNTOS",
        "PUNTAJE"
    ]

    @classmethod
    def es_linea_valida(cls, linea):

        if not linea:
            return False

        texto = linea.upper()

        for palabra in cls.PALABRAS_BASURA:
            if palabra in texto:
                return False

        return True

    @classmethod
    def filtrar(cls, lineas):

        resultado = []

        for linea in lineas:

            if cls.es_linea_valida(linea):
                resultado.append(linea)

        return resultado