import random
import time

# Constantes para controle de layout (usadas na interface)
spacing= 130
padding_left= 25

class GerenciadorVeiculos:
    def __init__(self, sistema):
        self.sistema = sistema

    # Inicializa as posições iniciais dos veículos. Cada veículo é posicionado aleatoriamente em um dos pontos de redistribuição.
    def inicializar_veiculos(self):
        pontos_disponiveis = list(range(self.sistema.s))
        random.shuffle(pontos_disponiveis)
        for i in range(self.sistema.c):
            self.sistema.veiculos_pos[i] = pontos_disponiveis[i % len(pontos_disponiveis)]


    # Gerencia o comportamento de um veículo.Cada veículo percorre os pontos de redistribuição circularmente, atualiza seu status e posição, interage com os pontos (carregar/descarregar encomendas).
    def gerenciar_veiculo(self, id_veiculo):
        while not self.sistema.finalizado:
            posicao_atual = self.sistema.veiculos_status[id_veiculo]["posicao"]
            proximo_ponto = (posicao_atual + 1) % self.sistema.s

            # Atualiza o status para "Em Viagem"
            self.sistema.veiculos_status[id_veiculo].update({"status": "Em Viagem"})
            self.sistema.update_queue.put(
                ("Status Atualizado", {"id_veiculo": id_veiculo, "status": "Em Viagem"})
            )

            # Simulação da viagem
            tempo_total_viagem = random.uniform(3, 10)  # Tempo total da viagem (segundos)
            intervalos = 20  # Número de passos da viagem
            tempo_por_intervalo = tempo_total_viagem / intervalos
            
            # Calcula a posição inicial e final do veículo
            x_inicio = padding_left + spacing * posicao_atual + spacing // 2
            x_fim = padding_left + spacing * proximo_ponto + spacing // 2
            y = 150  # Mantém o eixo Y fixo

            # Calcula a posição inicial e final do veículo
            for i in range(1, intervalos + 1):
                # Interpolação linear
                x_atual = x_inicio + (x_fim - x_inicio) * (i / intervalos)

                # Atualiza a posição do veículo na interface
                self.sistema.update_queue.put(
                    ("Movimento Parcial", {"id_veiculo": id_veiculo, "x": x_atual, "y": y})
                )
                time.sleep(tempo_por_intervalo)  # Intervalo de tempo entre cada passo

            # Ao final da viagem, atualiza a posição final
            self.sistema.veiculos_status[id_veiculo].update({
                "posicao": proximo_ponto,
                "status": "Aguardando"
            })
            self.sistema.update_queue.put(
                ("Movimento", (id_veiculo, proximo_ponto))
            )

            # Acessa o próximo ponto
            self.sistema.gerenciar_ponto(proximo_ponto, id_veiculo)

            # Marca como parado
            self.sistema.veiculos_status[id_veiculo].update({"status": "Parado"})
            self.sistema.update_queue.put(
                ("Status Atualizado", {"id_veiculo": id_veiculo, "status": "Parado"})
            )
           

