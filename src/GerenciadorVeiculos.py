import random
import time


class GerenciadorVeiculos:
    def __init__(self, sistema):
        self.sistema = sistema

    def inicializar_veiculos(self):
        pontos_disponiveis = list(range(self.sistema.s))
        random.shuffle(pontos_disponiveis)
        for i in range(self.sistema.c):
            self.sistema.veiculos_pos[i] = pontos_disponiveis[i % len(pontos_disponiveis)]

    def gerenciar_veiculo(self, id_veiculo):
        while not self.sistema.finalizado:
            posicao_atual = self.sistema.veiculos_pos[id_veiculo]
            time.sleep(random.uniform(0.5, 1.5))

            proximo_ponto = (posicao_atual + 1) % self.sistema.s            

            self.sistema.gerenciar_ponto(
                proximo_ponto, id_veiculo, posicao_atual)

            self.sistema.update_queue.put(
                ("Movimento", (id_veiculo, proximo_ponto)))
            self.sistema.veiculos_pos[id_veiculo] = proximo_ponto
