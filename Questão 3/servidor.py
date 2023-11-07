import socket
import json
import os
import threading
import pickle

# Classes definidas para o exemplo (Médico, Especialidades, Consultas)

class Medico:
    def __init__(self, nome):
        self.nome = nome

class Especialidades:
    def __init__(self):
        self.medicos = []

    def adicionar_medico(self, medico):
        self.medicos.append(medico)

class Consultas:
    def __init__(self):
        self.consultas = []

    def marcar_consulta(self, paciente, especialidade, data):
        self.consultas.append({"paciente": paciente, "especialidade": especialidade, "data": data})

    def consultar_consultas_por_paciente(self, paciente):
        return [consulta for consulta in self.consultas if consulta['paciente'] == paciente]

def save_consultas_to_json(consultas):
    with open("consultas.json", "w") as json_file:
        json.dump(consultas.consultas, json_file)

def load_consultas_from_json(consultas):
    if os.path.exists("consultas.json"):
        with open("consultas.json", "r") as json_file:
            consultas.consultas = json.load(json_file)

especialidades = Especialidades()
consultas = Consultas()
load_consultas_from_json(consultas)

# Configuração do servidor
HOST = '127.0.0.1'
PORT = 12345

# Dicionário de especialidades e números correspondentes
especialidades_dict = {
    1: "Oftalmologista",
    2: "Patologista",
    3: "Clínico Geral",
}


def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        request = pickle.loads(data)

        if request['action'] == 'marcar_consulta':
            paciente = request['paciente']
            especialidade_num = request['especialidade']  
            if especialidade_num not in especialidades_dict:
                response = {"message": "Especialidade inválida."}
            else:
                especialidade = especialidades_dict[especialidade_num]
                data = request['data']
                consultas.marcar_consulta(paciente, especialidade, data)
                save_consultas_to_json(consultas)  
                response = {"message": "Consulta marcada com sucesso."}
            client_socket.send(pickle.dumps(response))
        
        elif request['action'] == 'consultar_consultas':
            paciente = request['paciente']
            consultas_paciente = consultas.consultar_consultas_por_paciente(paciente)
            response = {"consultas": consultas_paciente}
            client_socket.send(pickle.dumps(response))

    client_socket.close()




def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Servidor ouvindo em {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexão recebida de {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    main()
