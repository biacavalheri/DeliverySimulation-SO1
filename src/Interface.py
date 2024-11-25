import tkinter as tk


class Interface:
    def __init__(self, sistema):
        self.sistema = sistema
        self.root = tk.Tk()
        self.root.title("Rede de Entregas")
        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.canvas.pack()

        # Criação do widget para exibição de logs
        self.log_text = tk.Text(self.root, height=10, width=80, wrap=tk.WORD)
        self.log_text.pack()

        self.update_queue = sistema.update_queue
        self.pontos_ui = []
        self.veiculos_ui = []
        self.veiculos_labels = []  # Lista para armazenar os labels dos veículos
        self.setup_pontos()

        # Atualizações periódicas
        self.root.after(100, self.update_interface)

    def setup_pontos(self):
        """Desenhar os pontos de redistribuição no canvas."""
        spacing = 800 // self.sistema.s
        for i in range(self.sistema.s):
            x = spacing * i + spacing // 2
            y = 200
            ponto = self.canvas.create_oval(
                x - 20, y - 20, x + 20, y + 20, fill="blue")
            label = self.canvas.create_text(x, y - 30, text=f"Ponto {i}")
            self.pontos_ui.append((ponto, label))

        # Criar veículos e adicionar números ao lado
        for i in range(self.sistema.c):
            x = spacing * self.sistema.veiculos_pos[i] + spacing // 2
            y = 150
            veiculo = self.canvas.create_rectangle(
                x - 10, y - 10, x + 10, y + 10, fill="red")
            veiculo_label = self.canvas.create_text(
                x, y - 30, text=f"V{i}")  # Adiciona o número do veículo (V0, V1, etc.)
            self.veiculos_ui.append(veiculo)
            self.veiculos_labels.append(veiculo_label)

    def update_interface(self):
        """Atualizar elementos gráficos em tempo real."""
        while not self.update_queue.empty():
            event_type, data = self.update_queue.get()
            if event_type == "Movimento":
                veiculo_id, posicao = data
                spacing = 800 // self.sistema.s
                x = spacing * posicao + spacing // 2
                y = 150
                # Atualizar a posição do veículo
                self.canvas.coords(
                    self.veiculos_ui[veiculo_id], x - 10, y - 10, x + 10, y + 10)
                # Atualizar a posição do número do veículo
                self.canvas.coords(self.veiculos_labels[veiculo_id], x, y - 30)
            elif event_type == "Fila Atualizada":
                ponto, fila_tamanho = data
                _, label = self.pontos_ui[ponto]
                self.canvas.itemconfig(
                    label, text=f"Ponto {ponto} (Fila: {fila_tamanho})")
            elif event_type == "Log":
                log_message = data
                # Adicionar o log no widget de texto
                self.log_text.insert(tk.END, log_message + "\n")
                self.log_text.yview(tk.END)  # Scroll para o final do log

        # Continuar atualizando a interface
        self.root.after(100, self.update_interface)

    def start(self):
        self.root.mainloop()