import os

structure = {
    "app": {
        "models": [
            "usuario.py",
            "docente.py",
            "estudiante.py",
            "grado.py",
            "seccion.py",
            "evaluacion.py",
            "ejercicio.py",
            "examen.py",
            "resultado.py",
            "error_matematico.py",
            "recomendacion.py"
        ],

        "routes": [
            "auth_routes.py",
            "docente_routes.py",
            "estudiante_routes.py",
            "grado_routes.py",
            "seccion_routes.py",
            "evaluacion_routes.py",
            "examen_routes.py",
            "resultado_routes.py",
            "dashboard_routes.py",
            "reportes_routes.py"
        ],

        "services": [
            "ocr_service.py",
            "image_processing_service.py",
            "ast_service.py",
            "sympy_service.py",
            "validation_service.py",
            "error_classifier_service.py",
            "recommendation_service.py",
            "report_service.py"
        ],

        "templates": {
            "auth": [
                "login.html",
                "register.html"
            ],

            "dashboard": [
                "dashboard.html"
            ],

            "estudiantes": [
                "listar.html",
                "crear.html",
                "editar.html",
                "detalle.html"
            ],

            "docentes": [
                "listar.html",
                "crear.html",
                "editar.html"
            ],

            "evaluaciones": [
                "listar.html",
                "crear.html",
                "ejercicios.html",
                "cargar_examen.html"
            ],

            "resultados": [
                "resultado.html",
                "errores.html",
                "recomendaciones.html"
            ],

            "reportes": [
                "reportes.html"
            ]
        },

        "static": {
            "css": ["styles.css"],
            "js": ["app.js"],
            "img": [],
            "uploads": {
                "examenes": [],
                "procesados": []
            }
        },

        "database": [
            "connection.py",
            "seed.py"
        ],

        "utils": [
            "helpers.py",
            "validators.py",
            "parser.py",
            "image_utils.py",
            "constants.py"
        ]
    },

    "migrations": [],
    "tests": [
        "test_auth.py",
        "test_sympy.py",
        "test_ocr.py",
        "test_validation.py"
    ],

    "docs": {
        "diagramas": [],
        "capturas": [],
        "evidencias": []
    }
}

root_files = [
    "run.py",
    "requirements.txt",
    ".env",
    ".gitignore",
    "README.md"
]


def create(path, tree):
    if isinstance(tree, dict):
        os.makedirs(path, exist_ok=True)

        for key, value in tree.items():
            create(os.path.join(path, key), value)

    elif isinstance(tree, list):
        os.makedirs(path, exist_ok=True)

        for item in tree:
            if isinstance(item, str):
                open(os.path.join(path, item), "w").close()
            else:
                create(path, item)


# Crear estructura principal
create(".", structure)

# Crear archivos raíz
for file in root_files:
    open(file, "w").close()

# Crear archivos base
open("app/__init__.py", "w").close()
open("app/config.py", "w").close()

print("✅ Estructura I.E Elvira García Y García creada correctamente")