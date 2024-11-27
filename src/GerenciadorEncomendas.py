import time
from .Encomenda import Encomenda

class GerenciadorEncomendas:
    def __init__(self, sistema):
        self.sistema = sistema

    # Gerencia uma encomenda específica.Cada thread gerencia uma única encomenda que: registra sua chegada ao ponto de origem, é adicionada à fila do ponto de origem e aguarda o carregamento por um veículo.
    def gerenciar_encomenda(self, id_enc, origem, destino):
        encomenda = Encomenda(id_enc, origem, destino)
        encomenda.registrar_chegada()
        self.sistema.update_queue.put(("Nova Encomenda", (id_enc, origem, destino)))
        while not self.sistema.finalizado:
            with self.sistema.pontos[origem]:
                self.sistema.filas[origem].append(encomenda)
                self.sistema.update_queue.put(
                    ("Fila Atualizada", (origem, len(self.sistema.filas[origem]))))
                break
            time.sleep(0.1)

