import socket
import json
import threading
import time

# Carregando os dados iniciais a partir do arquivo JSON
with open("voting_data.json", "r") as file:
    data = json.load(file)

candidates = data["candidates"]
voters = data["voters"]
vote_timeout = 50
start_time = time.time()

# Carregando dados de administradores a partir do arquivo JSON
with open("admins.json", "r") as admin_file:
    admin_data = json.load(admin_file)
admins = admin_data["admins"]

# Função para verificar se um CPF é de um administrador
def is_admin(cpf):
    for admin in admins:
        if admin["cpf"] == cpf:
            return admin
    return None

# Função para adicionar um novo candidato
def add_candidate(candidate_name):
    new_candidate = {"id": len(candidates) + 1, "name": candidate_name, "votes": 0}
    candidates.append(new_candidate)
    with open("voting_data.json", "w") as file:
        json.dump(data, file)

# Função para remover um candidato pelo índice
def remove_candidate(candidate_index):
    if 0 <= candidate_index < len(candidates):
        removed_candidate = candidates.pop(candidate_index)
        with open("voting_data.json", "w") as file:
            json.dump(data, file)
        return removed_candidate
    return None

# Função para lidar com a conexão de um cliente
def handle_client(client_socket):
    voter_id = client_socket.recv(1024).decode()
    admin = is_admin(voter_id)

    if admin:
        # Se o usuário é um administrador, permita o acesso direto às opções do administrador
        client_socket.send(b"Acesso de administrador concedido!\n")
        client_socket.send(b"Opcoes de administrador:\n")
        client_socket.send(b"1. Adicionar candidato\n")
        client_socket.send(b"2. Remover candidato\n")

        try:
            admin_choice = client_socket.recv(1024).decode()
        except ConnectionResetError:
            print("Administrador encerrou conexão antes de selecionar opção.")
            return
        if admin_choice == "1":
            # Adicionar candidato
            client_socket.send(b"Digite o nome do novo candidato: ")
            new_candidate_name = client_socket.recv(1024).decode()
            add_candidate(new_candidate_name)
            print(f"Novo candidato adicionado: {new_candidate_name}")
        elif admin_choice == "2":
            # Remover candidato
            client_socket.send(b"Digite o indice do candidato que deseja remover: ")
            try:
                candidate_index = int(client_socket.recv(1024).decode())
                removed_candidate = remove_candidate(candidate_index)
                if removed_candidate:
                    message = f"Candidato removido: {removed_candidate['name']}\n"
                    try:
                        client_socket.send(message.encode())
                    except ConnectionResetError:
                        print("Erro ao enviar mensagem ao cliente.")
                else:
                    client_socket.send(b"Indice de candidato invalido.\n")
            except ValueError:
                client_socket.send(b"Indice de candidato invalido.\n")
        else:
            client_socket.send(b"Opcao de administrador invalida.\n")
    elif time.time() - start_time >= vote_timeout:
        # Se o tempo de votação já acabou, envie os resultados
        results = {"candidates": candidates}
        total_votes = sum(candidate["votes"] for candidate in candidates)
        
        # Verifique se há empate (mesma quantidade de votos entre os principais candidatos)
        top_candidates = [candidate for candidate in candidates if candidate["votes"] == max(candidates, key=lambda x: x["votes"])["votes"]]
        
        if total_votes > 0 and len(top_candidates) == 1:
            # Caso em que há um vencedor claro
            winner = top_candidates[0]
            winner_percentage = (winner["votes"] / total_votes) * 100
            winner_name = winner["name"]
        else:
            # Caso em que há um empate ou nenhum voto
            winner_name = "Empate" if total_votes > 0 else "Nenhum voto"
            winner_percentage = 0
        
        results["total_votes"] = total_votes
        results["winner_name"] = winner_name
        results["winner_votes"] = top_candidates[0]["votes"] if top_candidates else 0
        results["winner_percentage"] = winner_percentage
        client_socket.send(json.dumps(results).encode())

    else:
        if voter_id not in voters:
            client_socket.send(json.dumps(candidates).encode())
            try:
                candidate_id = int(client_socket.recv(1024).decode())
            except ValueError:
                candidate_id = 0
                print("Candidato foi desconectado antes de votar.")

            if 1 <= candidate_id <= len(candidates):
                candidates[candidate_id - 1]["votes"] += 1
                voters[voter_id] = candidate_id

                # Atualizando os dados no arquivo JSON
                with open("voting_data.json", "w") as file:
                    json.dump(data, file)

                client_socket.send(b"Voto registrado com sucesso!\n")
            else:
                client_socket.send(b"Candidato invalido!\n")
        else:
            client_socket.send(b"Voce ja votou!\n")

    client_socket.close()
    print(f"Conexao encerrada.")

# Configuracao do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9999))
server.listen(5)

print("Servidor de votacao ativo e aguardando conexoes...")
while True:
    client, addr = server.accept()
    print(f"Conexao recebida de {addr[0]}:{addr[1]}")
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
