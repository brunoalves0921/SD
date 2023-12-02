import socket
import pickle

# Configuração do cliente
HOST = '127.0.0.1'
PORT = 12345

# Dicionário de especialidades e números correspondentes
especialidades_dict = {
    1: "Oftalmologista",
    2: "Patologista",
    3: "Clínico Geral",
}

def send_request(request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.send(pickle.dumps(request))
    return client_socket
0
if __name__ == '__main__':
    while True:
        action = input("Escolha uma ação:\n1. Marcar consulta\n2. Listar consultas por paciente\n3. Sair\nOpção: ")
        if action == '1':
            paciente = input("Nome do paciente: ")
            print("Especialidades:")
            for num, especialidade in especialidades_dict.items():
                print(f"{num}. {especialidade}")
            especialidade_num = int(input("Escolha o número da especialidade desejada: "))
            if especialidade_num not in especialidades_dict:
                print("Especialidade inválida.")
                continue
            data = input("Data da consulta: ")
            request = {
                "action": "marcar_consulta",
                "paciente": paciente,
                "especialidade": especialidade_num, 
                "data": data
            }
            client_socket = send_request(request)
            response = client_socket.recv(1024)
            response_data = pickle.loads(response)
            print(response_data['message'])
            client_socket.close()
        elif action == '2':
            paciente = input("Nome do paciente para consulta: ")
            request = {
                "action": "consultar_consultas",
                "paciente": paciente
            }
            client_socket = send_request(request)
            response = client_socket.recv(1024)
            response_data = pickle.loads(response)
            consultas_paciente = response_data.get('consultas', [])
            if consultas_paciente:
                print("Consultas do paciente:")
                for consulta in consultas_paciente:
                    print(f"Paciente: {consulta['paciente']}, Especialidade: {consulta['especialidade']}, Data: {consulta['data']}")
            else:
                print("Nenhuma consulta encontrada para o paciente.")
            client_socket.close()
        elif action == '3':
            break
