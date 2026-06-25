from app import create_app

from app.database.seed import (
    seed_academico
)

app = create_app()


with app.app_context():

        seed_academico()


if __name__ == '__main__':

    app.run(debug=True)