# Beatriz de Oliveira Cavalheri
# Larissa Rodrigues Ferrari
# Murilo Augusto Venturato

import threading
import random
import time
import datetime

class PontoRedistribuicao:
    def __init__(self, id):
        self.id = id
        self.fila_encomendas = []
        self.lock = threading.Lock()

    def adicionar_encomenda(self, encomenda):
        with self.lock:
            self.fila_encomendas.append(encomenda)
            print(f"Encomenda {encomenda.id} adicionada à fila no ponto {self.id}")

    def despachar_encomenda(self):
        with self.lock:
            if self.fila_encomendas:
                return self.fila_encomendas.pop(0)
            return None

class Veiculo(threading.Thread):
    def __init__(self, id, pontos):
        threading.Thread.__init__(self)
        self.id = id
        self.pontos = pontos
        self.ponto_atual = random.randint(0, len(pontos) - 1)

    def run(self):
        while True:
            ponto = self.pontos[self.ponto_atual]
            encomenda = ponto.despachar_encomenda()

            if encomenda:
                self.carregar_encomenda(encomenda)
                self.entregar_encomenda(encomenda)

            self.ponto_atual = (self.ponto_atual + 1) % len(self.pontos)
            time.sleep(random.uniform(1, 2))  # Espera aleatória para simular o tempo de viagem

    def carregar_encomenda(self, encomenda):
        print(f"Encomenda {encomenda.id} carregada no veículo {self.id} no ponto {self.ponto_atual}")

    def entregar_encomenda(self, encomenda):
        tempo_entrega = random.uniform(1, 3)
        time.sleep(tempo_entrega)
        print(f"Encomenda {encomenda.id} entregue no ponto {encomenda.destino}")

class Encomenda(threading.Thread):
    def __init__(self, id, origem, destino, ponto):
        threading.Thread.__init__(self)
        self.id = id
        self.origem = origem
        self.destino = destino
        self.ponto = ponto
        self.hora_chegada = None
        self.hora_carregamento = None
        self.hora_descarregamento = None

    def run(self):
        self.hora_chegada = datetime.datetime.now()
        print(f"Encomenda {self.id} chegou ao ponto {self.ponto.id} às {self.hora_chegada}")
        self.ponto.adicionar_encomenda(self)

        # Simular o carregamento da encomenda em um veículo
        time.sleep(random.uniform(0.5, 1.5))
        self.hora_carregamento = datetime.datetime.now()
        print(f"Encomenda {self.id} carregada no veículo {self.id} no ponto {self.ponto.id} às {self.hora_carregamento}")

        # Simular o descarregamento da encomenda
        time.sleep(random.uniform(0.5, 1.5))
        self.hora_descarregamento = datetime.datetime.now()
        print(f"Encomenda {self.id} entregue no ponto {self.destino} às {self.hora_descarregamento}")

        # Salvar o rastro da encomenda
        self.salvar_rastro()

    def salvar_rastro(self):
        with open(f"rastro_encomenda_{self.id}.txt", "w") as file:
            file.write(f"ID da Encomenda: {self.id}\n")
            file.write(f"Origem: {self.origem}\n")
            file.write(f"Destino: {self.destino}\n")
            file.write(f"Hora de Chegada na Origem: {self.hora_chegada}\n")
            file.write(f"Hora de Carregamento: {self.hora_carregamento}\n")
            file.write(f"Hora de Descarregamento: {self.hora_descarregamento}\n")

def main():
    S = int(input("Digite o número de pontos de redistribuição (S): "))
    C = int(input("Digite o número de veículos (C): "))
    P = int(input("Digite o número de encomendas (P): "))
    A = int(input("Digite o número de espaços de carga em cada veículo (A): "))

    pontos = [PontoRedistribuicao(i) for i in range(S)]
    veiculos = [Veiculo(i, pontos) for i in range(C)]

    for veiculo in veiculos:
        veiculo.start()

    for i in range(P):
        origem = random.randint(0, S - 1)
        destino = random.randint(0, S - 1)
        while destino == origem:
            destino = random.randint(0, S - 1)
        encomenda = Encomenda(i, origem, destino, pontos[origem])
        encomenda.start()

    for veiculo in veiculos:
        veiculo.join()

if __name__ == "__main__":
    main()
