import threading
from queue import Queue
from src.Interface import Interface
from src.RedeEntrega import RedeEntrega


def main():

    s = int(input("Digite o número de pontos de redistribuição (S): "))
    c = int(input("Digite o número de veículos (C): "))
    p = int(input("Digite o número de encomendas (P): "))
    a = int(input("Digite o número de espaços de carga em cada veículo (A): "))

    update_queue = Queue()
    rede_entrega = RedeEntrega(s, c, p, a, update_queue)
    threading.Thread(target=rede_entrega.iniciar_threads).start()

    # Interface gráfica
    app = Interface(rede_entrega)
    app.start()

if __name__ == "__main__":
    main()
    
    
    
# veiculo não verificava se tinha encomenda na fila
# a capacidade do veiculo não influenciava no código 
# dentro do ponto de redistribuição não estava sendo usado um semáforo