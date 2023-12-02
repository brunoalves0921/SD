from rotas import app
from utils import load_json


if __name__ == '__main__':
    load_json('pacientes')
    load_json('medicos')
    load_json('consultas')

    app.run(debug=True)
