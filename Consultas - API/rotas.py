import utils
from flask import Flask, jsonify, request, Response


app = Flask(__name__)


# Rotas de pacientes

@app.route('/pacientes/', methods=['GET', 'POST'])
def get_pacientes():
    if request.method == 'POST':
        data = request.get_json()
        error = utils.adicionar_paciente(data['nome'], data['cpf'])
        if error:
            return error

        return utils.json_message('Paciente adicionado com sucesso.')

    if request.method == 'GET':
        return jsonify({'pacientes': utils.pacientes})

@app.route('/pacientes/<cpf>/', methods=['GET', 'DELETE'])
def get_paciente(cpf):
    if request.method == 'DELETE':
        return utils.deletar_paciente(cpf)

    if request.method == 'GET':
        paciente = utils.consultar_paciente(cpf)
        if paciente:
            return jsonify({'paciente': paciente})
        else:
            return utils.json_message('Paciente não encontrado.', 404)


# Rotas de médicos

@app.route('/medicos/', methods=['GET', 'POST', 'DELETE'])
def get_medicos():
    if request.method == 'POST':
        data = request.get_json()
        error = utils.adicionar_medico(data['nome'], data['cpf'], utils.especialidades[data['especialidade']])
        if error:
            return error

        return utils.json_message('Médico adicionado com sucesso.')

    if request.method == 'GET': 
        especialidade = request.args.get('especialidade')
        return jsonify({'medicos': utils.medicos if not especialidade else utils.consultar_medicos_por_especialidade(utils.especialidades[int(especialidade)])})
    
    
@app.route('/medicos/<cpf>/', methods=['GET', 'DELETE'])
def get_medico(cpf):
    if request.method == 'DELETE':
        return utils.deletar_medico(cpf)
    medico = utils.consultar_medico(cpf)
    if medico:
        return jsonify({'medico': medico})
    else:
        return utils.json_message('Médico não encontrado.', 404)


# Rotas de consultas

@app.route('/consultas/', methods=['GET', 'POST', 'DELETE'])
def get_consultas():

    if request.method == 'POST':
        data = request.get_json()
        paciente = utils.consultar_paciente(data['paciente_cpf'])
        medico = utils.consultar_medico(data['medico_cpf'])

        if not paciente:
            return utils.json_message('Paciente não encontrado.', 404)
        if not medico:
            return utils.json_message('Médico não encontrado.', 404)
        
        utils.marcar_consulta(paciente, medico, data['data'])
        return jsonify({'message': 'Consulta marcada com sucesso.'})

    if request.method == 'GET':
        medico_cpf = request.args.get('medico_cpf')
        paciente_cpf = request.args.get('paciente_cpf')

        if medico_cpf:
            return jsonify({'consultas': utils.consultar_consultas_por_medico(medico_cpf)})
        elif paciente_cpf:
            return jsonify({'consultas': utils.consultar_consultas_por_paciente(paciente_cpf)})
        else:
            return jsonify({'consultas': utils.consultas})
    
    if request.method == 'DELETE':
        data = request.get_json()
        return utils.deletar_consulta(data['paciente_cpf'], data['medico_cpf'], data['data'])


@app.route('/especialidades/', methods=['GET'])
def get_especialidades():
    return jsonify({'especialidades': dict(enumerate(utils.especialidades))})
