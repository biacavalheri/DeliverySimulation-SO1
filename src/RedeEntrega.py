import threading
import random
import time
from .GerenciadorEncomendas import GerenciadorEncomendas
from .GerenciadorVeiculos import GerenciadorVeiculos
import os
from datetime import datetime
from threading import Semaphore


class RedeEntrega:
    def __init__(self, s, c, p, a, update_queue):
        self.s = s  # Número de pontos de redistribuição
        self.c = c  # Número de veículos
        self.p = p  # Número de encomendas
        self.a = a  # Capacidade de carga de cada veículo
        self.update_queue = update_queue # Fila de eventos para a interface
        
        self.pontos = [Semaphore(1) for _ in range(s)] # Semáforos para controle de acesso exclusivo a cada ponto de redistribuição
        self.filas = [[] for _ in range(s)] # Filas para armazenar encomendas em cada ponto
        self.filas_semaforo = [Semaphore(1) for _ in range(s)] # Semáforos adicionais para proteger o acesso às filas (preciosismo)

        self.veiculos_pos = [random.randint(0, s - 1) for _ in range(c)] # Posição Aleatoria dos carrinhos entre 0 e o máximo de pontos de entrega
        self.veiculos_status = [{"posicao": pos, "status": "Parado"} for pos in self.veiculos_pos] # Status iniciais dos carrinhos
        self.veiculos_carga = [[] for _ in range(c)] # fila de carga de cada carrinho

        self.lock = threading.Lock() # Lock para proteger variáveis compartilhadas entre threads

        self.enc_entregues = 0 # Guarda o numero de entregas feitas
        self.finalizado = False # Guarda se o sistema já finalizou

        # Gerenciadores
        self.gerenciador_veiculos = GerenciadorVeiculos(self) 
        self.gerenciador_encomendas = GerenciadorEncomendas(self)

    # A função principal
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

        # Thread para monitorar o término da simulação
        monitor = threading.Thread(target=self.verificar_fim)
        monitor.start()
        threads.append(monitor)

        # Aguardar todas as threads terminarem
        for t in threads:
            t.join()

    # Monitora se todas as encomendas foram entregues
    def verificar_fim(self):
        while True:
            with self.lock:  # Acesso exclusivo ao contador de encomendas entregues
                if self.enc_entregues >= self.p: # Todas as encomendas foram entregues
                    self.finalizado = True
                    self.update_queue.put(
                        ("Fim", "Simulação finalizada!"))
                    break
            time.sleep(0.1) # Aguarda um curto intervalo antes de verificar novamente

    # Gerencia a interação do veículo com o ponto de redistribuição
    def gerenciar_ponto(self, proximo_ponto, id_veiculo):
        with self.pontos[proximo_ponto]: # Garante exclusividade no acesso ao ponto
            nova_carga = []

            with self.filas_semaforo[proximo_ponto]: # Protege o acesso à fila do ponto
                # Processa as encomendas que chegaram ao destino
                for encomenda in self.veiculos_carga[id_veiculo]:
                    if encomenda.destino == proximo_ponto:
                        encomenda.registrar_entrega()
                        self.salvar_rastro_encomenda(encomenda)
                        with self.lock:
                            self.enc_entregues += 1
                        
                        self.update_queue.put(
                            ("Status Atualizado", {"id_veiculo": id_veiculo, "status": "Descarregando..."})
                        )

                        time.sleep(random.uniform(1, 5)) # Tempo entrega

                        self.update_queue.put(
                            ("Log", f"Veículo {id_veiculo} entregou encomenda {encomenda.id_enc} no ponto {encomenda.destino}"))
                        self.update_queue.put(
                            ("Entrega", (id_veiculo, encomenda.id_enc, encomenda.destino)))
                    else:
                        nova_carga.append(encomenda)

                # Atualiza a carga do veículo
                self.veiculos_carga[id_veiculo] = nova_carga

                # Carrega novas encomendas no veículo, se houver espaço
                while len(self.veiculos_carga[id_veiculo]) < self.a and self.filas[proximo_ponto]:
                    encomenda = self.filas[proximo_ponto].pop(
                        0)  # Retirar encomenda da fila
                    encomenda.registrar_carregamento()
                    self.veiculos_carga[id_veiculo].append(encomenda)
                    
                    self.update_queue.put(
                        ("Status Atualizado", {"id_veiculo": id_veiculo, "status": "Carregando..."})
                    )

                    time.sleep(random.uniform(5, 10))  # Simula o tempo de carregamento

                    self.update_queue.put(
                        ("Log", f"Veículo {id_veiculo} carregou encomenda {encomenda.id_enc} no ponto {proximo_ponto}"))
                    self.update_queue.put(
                        ("Fila Atualizada", (proximo_ponto, len(self.filas[proximo_ponto]))))
                    

    def salvar_rastro_encomenda(self, encomenda):
        pasta_logs = "logs"
        if not os.path.exists(pasta_logs):
            os.makedirs(pasta_logs)
            print(f"Pasta '{pasta_logs}' criada.")

        agora = datetime.now()

        log_dia = agora.strftime("%Y_%m_%d_%H_%M_%S")

        nome_arquivo = os.path.join(
            pasta_logs, f"rastro_encomenda_{encomenda.id_enc}_{log_dia}.txt")

        with open(nome_arquivo, "w") as file:
            file.write(str(encomenda))
        print(
            f"Rastro da encomenda {encomenda.id_enc} salvo no arquivo {nome_arquivo}")
