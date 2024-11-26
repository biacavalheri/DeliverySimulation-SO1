import threading
import random
import time
from .GerenciadorEncomendas import GerenciadorEncomendas
from .GerenciadorVeiculos import GerenciadorVeiculos
import os


class RedeEntrega:
    def __init__(self, s, c, p, a, update_queue):
        self.s = s  # Pontos de redistribuição
        self.c = c  # Veículos
        self.p = p  # Encomendas
        self.a = a  # Espaços por veículo
        self.update_queue = update_queue

        self.pontos = [threading.Semaphore(1) for _ in range(s)]
        self.filas = [[] for _ in range(s)]
        self.veiculos_pos = [random.randint(0, s - 1) for _ in range(c)]
        self.veiculos_carga = [[] for _ in range(c)]
        self.lock = threading.Lock()
        self.enc_entregues = 0
        self.finalizado = False

        self.gerenciador_veiculos = GerenciadorVeiculos(self)
        self.gerenciador_encomendas = GerenciadorEncomendas(self)

    def iniciar_threads(self):
        threads = []

        # Inicializa os veículos e garante que eles começam em pontos diferentes
        self.gerenciador_veiculos.inicializar_veiculos()

        # Criar threads de veículos
        for i in range(self.c):
            t = threading.Thread(
                target=self.gerenciador_veiculos.gerenciar_veiculo, args=(i,))
            t.start()
            threads.append(t)
            self.update_queue.put(
                ("Log", f"Veículo {i} criado no ponto {self.veiculos_pos[i]}"))

        # Criar threads de encomendas
        for i in range(self.p):
            origem = random.randint(0, self.s - 1)
            destino = random.randint(0, self.s - 1)
            while destino == origem:
                destino = random.randint(0, self.s - 1)
            t = threading.Thread(
                target=self.gerenciador_encomendas.gerenciar_encomenda, args=(i, origem, destino))
            t.start()
            threads.append(t)

        # Monitorar o término
        monitor = threading.Thread(target=self.verificar_fim)
        monitor.start()
        threads.append(monitor)

        # Aguardar todas as threads terminarem
        for t in threads:
            t.join()

    def verificar_fim(self):
        while True:
            with self.lock:
                if self.enc_entregues >= self.p:
                    self.finalizado = True
                    self.update_queue.put(
                        ("Simulação", "Simulação finalizada!"))
                    break
            time.sleep(0.1)

    def buscar_proximo_ponto(self, ponto_atual):
        for i in range(1, self.s):
            proximo_ponto = (ponto_atual + i) % self.s
            if proximo_ponto not in self.veiculos_pos:
                return proximo_ponto
        return -1

    def gerenciar_ponto(self, proximo_ponto, id_veiculo, posicao_atual):
        with self.pontos[proximo_ponto]:
            nova_carga = []
            for id_enc, destino in self.veiculos_carga[id_veiculo]:
                if destino == proximo_ponto:
                    hora_chegada = time.time()
                    hora_carregamento = time.time()
                    hora_descarregamento = time.time()
                    self.salvar_rastro_encomenda(
                        id_enc, posicao_atual, destino, hora_chegada, hora_carregamento, hora_descarregamento)
                    with self.lock:
                        self.enc_entregues += 1
                    self.update_queue.put(
                        ("Log", f"Veículo {id_veiculo} entregou encomenda {id_enc} no ponto {destino}"))
                    self.update_queue.put(
                        ("Entrega", (id_veiculo, id_enc, destino)))
                else:
                    nova_carga.append((id_enc, destino))
            self.veiculos_carga[id_veiculo] = nova_carga

            while len(self.veiculos_carga[id_veiculo]) < self.a and self.filas[proximo_ponto]:
                encomenda = self.filas[proximo_ponto].pop(0)
                self.veiculos_carga[id_veiculo].append(encomenda)
                self.update_queue.put(
                    ("Log", f"Veículo {id_veiculo} carregou encomenda {encomenda[0]} no ponto {proximo_ponto}"))
                self.update_queue.put(
                    ("Fila Atualizada", (proximo_ponto, len(self.filas[proximo_ponto]))))

    def salvar_rastro_encomenda(self, id_enc, origem, destino, hora_chegada, hora_carregamento, hora_descarregamento):
        # Verifica e cria a pasta 'logs' se não existir
        pasta_logs = "logs"
        if not os.path.exists(pasta_logs):
            os.makedirs(pasta_logs)
            print(f"Pasta '{pasta_logs}' criada.")

        # Define o caminho completo do arquivo
        nome_arquivo = os.path.join(pasta_logs, f"rastro_encomenda_{id_enc}.txt")

        # Salva o rastro da encomenda no arquivo
        with open(nome_arquivo, "w") as file:
            file.write(f"ID da Encomenda: {id_enc}\n")
            file.write(f"Origem: {origem}\n")
            file.write(f"Destino: {destino}\n")
            file.write(f"Hora de Chegada na Origem: {hora_chegada}\n")
            file.write(f"Hora de Carregamento: {hora_carregamento}\n")
            file.write(f"Hora de Descarregamento: {hora_descarregamento}\n")
        print(f"Rastro da encomenda {id_enc} salvo no arquivo {nome_arquivo}")
