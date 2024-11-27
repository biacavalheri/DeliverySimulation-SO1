import threading
from queue import Queue
from src.Interface import Interface
from src.RedeEntrega import RedeEntrega


def main():

    while True:
        s = int(input("Digite o número de pontos de redistribuição (S): "))
        c = int(input("Digite o número de veículos (C): "))
        p = int(input("Digite o número de encomendas (P): "))
        a = int(input("Digite o número de espaços de carga em cada veículo (A): "))

        if not (p > a > c):
            print("\nErro: Deve-se assegurar que P (encomendas) >> A (espaços de carga) >> C (veículos).")
            print("Por favor, insira valores que satisfaçam esta condição.\n")
        else:
            break

    # Guarda os eventos para a interface
    update_queue = Queue()
    # Aplicação
    rede_entrega = RedeEntrega(s, c, p, a, update_queue)
    # Inicia as threads para o sistema dar inicio
    threading.Thread(target=rede_entrega.iniciar_threads).start()

    # Interface gráfica
    app = Interface(rede_entrega)
    app.start()

if __name__ == "__main__":
    main()