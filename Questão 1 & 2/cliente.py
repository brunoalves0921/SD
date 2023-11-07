import socket
import pickle

class Pessoa:
    def __init__(self, nome, cpf, idade):
        self.nome = nome
        self.cpf = cpf
        self.idade = idade

class PessoasOutputStream:
    def __init__(self, pessoas, output_stream):
        self.pessoas = pessoas
        self.output_stream = output_stream

    def enviar(self):
        try:
            pickle.dump(self.pessoas, self.output_stream)
        except Exception as e:
            print(f"Erro ao enviar dados: {e}")

def cliente_remoto():
    host = 'localhost'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print('')
        print(f"Conectado ao servidor {host}:{port}")
        print('')
    except Exception as e:
        print(f"Erro ao conectar com o servidor: {e}")
        return

    pessoas = []
    qtd_Pessoas = int(input("Digite a quantidade de pessoas que serão cadastradas: "))


    print('--------------------------------------------------')
    for i in range(qtd_Pessoas):
        nome = input("Digite o nome da pessoa: ")
        cpf = int(input("Digite o cpf da pessoa: "))
        idade = int(input("Digite a idade da pessoa: "))
        pessoa = Pessoa(nome, cpf, idade)
        pessoas.append(pessoa)
        print('--------------------------------------------------')

    output_stream = PessoasOutputStream(pessoas, client_socket.makefile('wb'))
    try:
        output_stream.enviar()
        print("Dados enviados com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar dados: {e}")

    client_socket.close()

if __name__ == "__main__":
    cliente_remoto()
