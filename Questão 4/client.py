import socket
import json

# Função para exibir a lista de candidatos
def display_candidates(candidates):
    print("Candidatos disponíveis:")
    for candidate in candidates:
        print(f"{candidate['id']}. {candidate['name']}")

# Função para exibir os resultados das eleições
def display_results(results):
    print("Eleições já estão encerradas!")
    print("\nResultados das eleições:")
    for candidate in results["candidates"]:
        print(f"{candidate['name']}: {candidate['votes']} votos")
    print(f"Total de votos: {results['total_votes']} votos")
    if results['winner_name'] == 'Empate':
        print("Empate!")
    elif results['winner_name'] == 'Nenhum voto':
        print("Nenhum voto!")
    else:
        print(f"Vencedor: {results['winner_name']} com {results['winner_votes']} votos ({results['winner_percentage']:.2f}% dos votos)")

# Configuração do cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

try:
    voter_id = input("Digite seu CPF: ")
    client.send(voter_id.encode())
    response = client.recv(1024).decode()

    if response:
        if "Acesso de administrador concedido!" in response:
            # O usuário é um administrador
            print("Acesso de administrador concedido!")
            print("Opções de administrador:")
            print("1. Adicionar candidato")
            print("2. Remover candidato")
            admin_choice = input("Escolha uma opção de administrador: ")
            client.send(admin_choice.encode())

            if admin_choice == "1":
                # Adicionar candidato
                new_candidate_name = input("Digite o nome do novo candidato: ")
                client.send(new_candidate_name.encode())
                response = client.recv(1024).decode()
                print("Candidato adicionado com sucesso!")
            elif admin_choice == "2":
                # Remover candidato
                candidate_index = input("Digite o índice do candidato que deseja remover: ")
                client.send(candidate_index.encode())
                response = client.recv(1024).decode()
                print("Candidato removido com sucesso!")
        else:
            try:
                candidates = json.loads(response)
                if "winner_name" in candidates:
                    # Se a resposta inclui o nome do vencedor, então são os resultados
                    display_results(candidates)
                else:
                    display_candidates(candidates)

                    # Escolha do candidato
                    candidate_id = int(input("Digite o número do candidato que deseja votar: "))
                    client.send(str(candidate_id).encode())

                    response = client.recv(1024).decode()
                    print(response)
            except json.decoder.JSONDecodeError:
                print("Você já votou!")
    else:
        print("Erro na conexão com o servidor.")
except ConnectionRefusedError:
    print("Não foi possível conectar ao servidor. Certifique-se de que o servidor está ativo.")
finally:
    client.close()
