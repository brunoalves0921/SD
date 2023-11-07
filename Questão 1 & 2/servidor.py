import socket
import pickle
import os

class Pessoa:
    def __init__(self, nome, cpf, idade):
        self.nome = nome
        self.cpf = cpf
        self.idade = idade
    
class PessoasInputStream:
    def __init__(self, input_stream):
        self.input_stream = input_stream

    def receber(self):
        try:
            received_data = pickle.load(self.input_stream)
            return received_data
        except Exception as e:
            print(f"Erro ao receber dados: {e}")

def calcular_tamanho_bytes_arquivo(nome_arquivo):
    tamanho_bytes = os.stat(nome_arquivo).st_size
    return tamanho_bytes

def servidor_remoto():
    host = 'localhost'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Servidor escutando em {host}:{port}")

    client_socket, client_address = server_socket.accept()
    print(f"Conexão de {client_address}")

    input_stream = PessoasInputStream(client_socket.makefile('rb'))
    received_pessoas = input_stream.receber()

    with open('pessoas_output.txt', 'w') as output_file:
        for pessoa in received_pessoas:
            output_file.write(f"Nome: {pessoa.nome}, CPF: {pessoa.cpf}, Idade: {pessoa.idade}\n")
            tamanho_bytes_pessoa_gravada = len(f"Nome: {pessoa.nome}, CPF: {pessoa.cpf}, Idade: {pessoa.idade}\n")
            print(f"Nome: {pessoa.nome}, CPF: {pessoa.cpf}, Idade: {pessoa.idade}, Tamanho em bytes por pessoa: {tamanho_bytes_pessoa_gravada + 1}")

        qtd_Pessoas = len(received_pessoas)
        print(f"Quantidade de pessoas: {qtd_Pessoas}")
    print(f"Tamanho total em bytes: {calcular_tamanho_bytes_arquivo('pessoas_output.txt')}")

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    servidor_remoto()
