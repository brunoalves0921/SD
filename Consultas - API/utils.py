import os
import json
from flask import Response
from classes import Paciente, Medico, Consulta

especialidades = ("Oftalmologista", "Patologista", "Clínico Geral")
    
pacientes: list[Paciente] = []
medicos: list[Medico] = []
consultas: list[Consulta] = []
resources = { 'pacientes': pacientes, 'medicos': medicos, 'consultas': consultas }

def json_message(message: str, status_code: int = 200):
    return Response(json.dumps({'message': message}), status=status_code, mimetype='application/json')


# Pacientes functions

def adicionar_paciente(nome: str, cpf: str):
    if next((paciente for paciente in pacientes if paciente['cpf'] == cpf), None):
        return json_message('Paciente já cadastrado.', 400)

    pacientes.append({ 'nome': nome, 'cpf': cpf })
    save_json('pacientes')

def consultar_paciente(cpf: str):
    for paciente in pacientes:
        if paciente['cpf'] == cpf:
            return paciente

def deletar_paciente(cpf: str):
    paciente = consultar_paciente(cpf)
    if paciente:
        pacientes.remove(paciente)
        save_json('pacientes')
        return json_message('Paciente removido com sucesso.')
    else:
        return json_message('Paciente não encontrado.', 404)


# Médicos functions

def adicionar_medico(nome: str, cpf: str, especialidade: str):
    if next((medico for medico in medicos if medico['cpf'] == cpf), None):
        return json_message('Médico já cadastrado.', 400)

    medicos.append({ 'nome': nome, 'cpf': cpf, 'especialidade': especialidade})
    save_json('medicos')

def consultar_medico(cpf: str):
    for medico in medicos:
        if medico['cpf'] == cpf:
            return medico

def consultar_medicos_por_especialidade(especialidade: str):
    return [medico for medico in medicos if medico['especialidade'] == especialidade]

def deletar_medico(cpf: str):
    medico = consultar_medico(cpf)
    if medico:
        medicos.remove(medico)
        save_json('medicos')
        return json_message('Médico removido com sucesso.')
    else:
        return json_message('Médico não encontrado.', 404)


# Consultas functions

def marcar_consulta(paciente: Paciente, medico: Medico, data):
    consultas.append({"paciente": paciente, "medico": medico, "data": data})
    save_json('consultas')

def consultar_consultas_por_medico(medico_cpf: str):
    return [consulta for consulta in consultas if consulta['medico']['cpf'] == medico_cpf]

def consultar_consultas_por_paciente(paciente_cpf: str):
    return [consulta for consulta in consultas if consulta['paciente']['cpf'] == paciente_cpf]

def deletar_consulta(paciente_cpf: str, medico_cpf: str, data: str):
    consulta = next((consulta for consulta in consultas if consulta['paciente']['cpf'] == paciente_cpf and consulta['medico']['cpf'] == medico_cpf and consulta['data'] == data), None)
    if consulta:
        consultas.remove(consulta)
        save_json('consultas')
        return json_message('Consulta removida com sucesso.')
    else:
        return json_message('Consulta não encontrada.', 404)

def save_json(resource: str):
    with open(f"{resource}.json", "w") as json_file:
        json.dump(resources[resource], json_file)

def load_json(resource: str):
    if os.path.exists(f"{resource}.json"):
        with open(f"{resource}.json", "r") as json_file:
            resources[resource].extend(json.load(json_file))
    else:
        with open(f"{resource}.json", "w") as json_file:
            json.dump([], json_file)
