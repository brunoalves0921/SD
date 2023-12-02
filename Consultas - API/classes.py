class Medico:
    def __init__(self, nome, cpf, especialidade):
        self.nome = nome
        self.cpf = cpf
        self.especialidade = especialidade

class Paciente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
    
class Consulta:
    def __init__(self, paciente_cpf: str, medico_cpf: str, data):
        self.paciente_cpf = paciente_cpf
        self.medico_cpf = medico_cpf
        self.data = data
