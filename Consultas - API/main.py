import requests

BASE_URL = "http://127.0.0.1:5000"  # Substitua pela URL correta da sua API

def menu():
    while True:

        print("\nMENU:")
        print("1. Listar Pacientes")
        print("2. Adicionar Paciente")
        print("3. Deletar Paciente")
        print("4. Listar Médicos")
        print("5. Adicionar Médico")
        print("6. Deletar Médico")
        print("7. Listar Consultas")
        print("8. Marcar Consulta")
        print("9. Deletar Consulta")
        print("10. Sair")

        choice = input("Escolha uma opção: ")
        try:
            if choice == "1":
                listar_pacientes()
            elif choice == "2":
                adicionar_paciente()
            elif choice == "3":
                deletar_paciente()
            elif choice == "4":
                listar_medicos()
            elif choice == "5":
                adicionar_medico()
            elif choice == "6":
                deletar_medico()
            elif choice == "7":
                listar_consultas()
            elif choice == "8":
                marcar_consulta()
            elif choice == "9":
                deletar_consulta()
            elif choice == "10":
                break
            else:
                print("Opção inválida. Tente novamente.")
        except requests.exceptions.ConnectionError:
            print()
            print("ERROR: Não foi possível estabelecer uma conexão. Tente novamente.")

def formatar_pacientes(data):
    print("\nPacientes:")
    print("--------------------------------------------------------------------")
    for paciente in data['pacientes']:
        print(f"Nome: {paciente['nome']}, CPF: {paciente['cpf']}")
        print("--------------------------------------------------------------------")
    print()

def formatar_medicos(data):
    print("\nMédicos:")
    print("--------------------------------------------------------------------")
    for medico in data['medicos']:
        print(f"Nome: {medico['nome']}, CPF: {medico['cpf']}, Especialidade: {medico['especialidade']}")
        print("--------------------------------------------------------------------")
    print()

def formatar_consultas(data):
    print("\nConsultas:")
    print("--------------------------------------------------------------------")
    for consulta in data['consultas']:
        print(f"Data: {consulta['data']}")
        print(f"Paciente: {consulta['paciente']['nome']}, CPF: {consulta['paciente']['cpf']}")
        print(f"Médico: {consulta['medico']['nome']}, CPF: {consulta['medico']['cpf']}, Especialidade: {consulta['medico']['especialidade']}")
        print("--------------------------------------------------------------------")
    print()

def listar_pacientes():
    response = requests.get(f"{BASE_URL}/pacientes/")
    formatar_pacientes(response.json())

def adicionar_paciente():
    nome = input("Digite o nome do paciente: ")
    cpf = input("Digite o CPF do paciente: ")
    if len(cpf.strip()) != 0 and len(nome.strip()) != 0:
        data = {"nome": nome, "cpf": cpf}
        response = requests.post(f"{BASE_URL}/pacientes/", json=data)
        print(response.json())
    else:
        print("Nome ou CPF inválido.")

def deletar_paciente():
    cpf = input("Digite o CPF do paciente a ser deletado: ")
    if len(cpf.strip()) != 0:
        response = requests.delete(f"{BASE_URL}/pacientes/{cpf}/")
        print(response.json())
    else:
        print("CPF inválido. Tente novamente.")

def listar_medicos():
    response = requests.get(f"{BASE_URL}/medicos/")
    formatar_medicos(response.json())

def adicionar_medico():
    nome = input("Digite o nome do médico: ")
    cpf = input("Digite o CPF do médico: ")
    if len(cpf.strip()) != 0 and len(nome.strip()) != 0:
        #printe todas as especialidades disponíveis
        print("Especialidades disponíveis:")
        print()
        print("0. Oftalmologista")
        print("1. Patologista")
        print("2. Clínico Geral")
        print()
        try:
            especialidade = int(input("Digite o número da especialidade do médico: "))
        except ValueError:
            print("Valor inválido. Tente novamente.")
            return
        data = {"nome": nome, "cpf": cpf, "especialidade": especialidade}
        response = requests.post(f"{BASE_URL}/medicos/", json=data)
        print(response.json())
    else:
        print("Nome ou CPF inválido.")

def deletar_medico():
    cpf = input("Digite o CPF do médico a ser deletado: ")
    if len(cpf.strip()) != 0:
        response = requests.delete(f"{BASE_URL}/medicos/{cpf}/")
        print(response.json())
    else:
        print("CPF inválido. Tente novamente.")

def listar_consultas():
    response = requests.get(f"{BASE_URL}/consultas/")
    formatar_consultas(response.json())

def marcar_consulta():
    paciente_cpf = input("Digite o CPF do paciente: ")
    medico_cpf = input("Digite o CPF do médico: ")
    if len(paciente_cpf.strip()) != 0 and len(medico_cpf.strip()) != 0:
        data = input("Digite a data da consulta (DD/MM/YYYY): ")
        data = {"paciente_cpf": paciente_cpf, "medico_cpf": medico_cpf, "data": data}
        response = requests.post(f"{BASE_URL}/consultas/", json=data)
        print(response.json())
    else:
        print("CPF inválido. Tente novamente.")

def deletar_consulta():
    paciente_cpf = input("Digite o CPF do paciente: ")
    medico_cpf = input("Digite o CPF do médico: ")
    data = input("Digite a data da consulta (DD/MM/YYYY): ")
    if len(paciente_cpf.strip()) != 0 and len(medico_cpf.strip()) != 0 and len(data.strip()) != 0:
        data = {"paciente_cpf": paciente_cpf, "medico_cpf": medico_cpf, "data": data}
        response = requests.delete(f"{BASE_URL}/consultas/", json=data)
        print(response.json())
    else:
        print("Dados inválidos. Tente novamente.")

if __name__ == "__main__":
    menu()
