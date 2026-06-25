from app.database.connection import db

from app.models.grado import Grado
from app.models.seccion import Seccion
from app.models.docente import Docente

def seed_academico():

    # GRADO

    existe_grado = Grado.query.filter_by(
        nombre='1° Secundaria'
    ).first()

    if not existe_grado:

        grado = Grado(
            nombre='1° Secundaria'
        )

        db.session.add(grado)

    # SECCIONES

    secciones = [
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H'
    ]

    for nombre in secciones:

        existe = Seccion.query.filter_by(
            nombre=nombre
        ).first()

        if not existe:

            seccion = Seccion(
                nombre=nombre
            )

            db.session.add(seccion)

    db.session.commit()
 # DOCENTES

    docentes = [

        {
            'codigo': 'DOC001',
            'nombres': 'Docente',
            'apellidos': 'Matemática 01'
        },

        {
            'codigo': 'DOC002',
            'nombres': 'Docente',
            'apellidos': 'Matemática 02'
        },

        {
            'codigo': 'DOC003',
            'nombres': 'Docente',
            'apellidos': 'Matemática 03'
        },

        {
            'codigo': 'DOC004',
            'nombres': 'Docente',
            'apellidos': 'Matemática 04'
        }
    ]


    for data in docentes:

        existe_docente = (
            Docente.query.filter_by(
                codigo=data['codigo']
            ).first()
        )

        if not existe_docente:

            docente = Docente(

                codigo=data['codigo'],

                nombres=data['nombres'],

                apellidos=data['apellidos']
            )

            db.session.add(docente)

    db.session.commit()
    
    print(
        'Datos académicos iniciales registrados.'
    )