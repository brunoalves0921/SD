# Documentação da API

Esta documentação descreve os endpoints e funcionalidades da API.

## Introdução

A API fornece funcionalidades para gerenciamento de pacientes, médicos e consultas. Utiliza o formato JSON para comunicação.

## Autenticação

A API não requer autenticação no momento.

## Endpoints

### Pacientes

#### 1. Listar Pacientes

- **Endpoint:** `/pacientes/`
- **Métodos:** `GET`
- **Descrição:** Retorna a lista de todos os pacientes.

#### 2. Adicionar Paciente

- **Endpoint:** `/pacientes/`
- **Métodos:** `POST`
- **Descrição:** Adiciona um novo paciente.
- **Parâmetros:**
  - `nome` (string): Nome do paciente.
  - `cpf` (string): CPF do paciente.

#### 3. Consultar Paciente

- **Endpoint:** `/pacientes/<cpf>/`
- **Métodos:** `GET`
- **Descrição:** Retorna os detalhes de um paciente específico.
- **Parâmetros:**
  - `cpf` (string): CPF do paciente.

#### 4. Deletar Paciente

- **Endpoint:** `/pacientes/<cpf>/`
- **Métodos:** `DELETE`
- **Descrição:** Remove um paciente com base no CPF.
- **Parâmetros:**
  - `cpf` (string): CPF do paciente.

### Médicos

#### 1. Listar Médicos

- **Endpoint:** `/medicos/`
- **Métodos:** `GET`
- **Descrição:** Retorna a lista de todos os médicos.
- **Parâmetros:**
  - `especialidade` (opcional): Filtra os médicos por especialidade.

#### 2. Adicionar Médico

- **Endpoint:** `/medicos/`
- **Métodos:** `POST`
- **Descrição:** Adiciona um novo médico.
- **Parâmetros:**
  - `nome` (string): Nome do médico.
  - `cpf` (string): CPF do médico.
  - `especialidade` (string): Especialidade do médico (0 - Oftalmologista, 1 - Patologista, 2 - Clínico Geral).

#### 3. Consultar Médico

- **Endpoint:** `/medicos/<cpf>/`
- **Métodos:** `GET`
- **Descrição:** Retorna os detalhes de um médico específico.
- **Parâmetros:**
  - `cpf` (string): CPF do médico.

#### 4. Deletar Médico

- **Endpoint:** `/medicos/<cpf>/`
- **Métodos:** `DELETE`
- **Descrição:** Remove um médico com base no CPF.
- **Parâmetros:**
  - `cpf` (string): CPF do médico.

### Consultas

#### 1. Listar Consultas

- **Endpoint:** `/consultas/`
- **Métodos:** `GET`
- **Descrição:** Retorna a lista de todas as consultas.
- **Parâmetros:**
  - `medico_cpf` (opcional): Filtra as consultas por CPF do médico.
  - `paciente_cpf` (opcional): Filtra as consultas por CPF do paciente.

#### 2. Marcar Consulta

- **Endpoint:** `/consultas/`
- **Métodos:** `POST`
- **Descrição:** Marca uma nova consulta.
- **Parâmetros:**
  - `paciente_cpf` (string): CPF do paciente.
  - `medico_cpf` (string): CPF do médico.
  - `data` (string): Data da consulta (formato: DD-MM-YYYY).

#### 3. Deletar Consulta

- **Endpoint:** `/consultas/`
- **Métodos:** `DELETE`
- **Descrição:** Remove uma consulta.
- **Parâmetros:**
  - `paciente_cpf` (string): CPF do paciente.
  - `medico_cpf` (string): CPF do médico.
  - `data` (string): Data da consulta (formato: DD-MM-YYYY).

### Especialidades

#### 1. Listar Especialidades

- **Endpoint:** `/especialidades/`
- **Métodos:** `GET`
- **Descrição:** Retorna a lista de especialidades disponíveis.

## Considerações Finais

Esta documentação fornece uma visão geral dos endpoints disponíveis na API. Certifique-se de fornecer os parâmetros corretos ao fazer solicitações para garantir o funcionamento adequado da API.

Utilize o programa "main.py" para consumir e testar essa API se preferir, é mais fácil fazer a manipulação por ele.
