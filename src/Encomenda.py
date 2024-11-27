from datetime import datetime, timedelta

class Encomenda:
    FATOR_ESCALA = 3600
    tempo_simulado_inicial = datetime(2024, 11, 27, 0, 0, 0)
    tempo_real_inicial = datetime.now()

    def __init__(self, id_enc, origem, destino):
        self.id_enc = id_enc
        self.origem = origem
        self.destino = destino
        self.hora_chegada = None
        self.hora_carregamento = None
        self.hora_entrega = None

    @staticmethod
    def obter_tempo_simulado():
        tempo_real_atual = datetime.now()
        diferenca_real = tempo_real_atual - Encomenda.tempo_real_inicial
        diferenca_simulada = diferenca_real.total_seconds() * Encomenda.FATOR_ESCALA
        return Encomenda.tempo_simulado_inicial + timedelta(seconds=diferenca_simulada)

    def registrar_chegada(self):
        self.hora_chegada = self.obter_tempo_simulado()

    def registrar_carregamento(self):
        self.hora_carregamento = self.obter_tempo_simulado()

    def registrar_entrega(self):
        self.hora_entrega = self.obter_tempo_simulado()

    def __str__(self):
        return (
            f"ID da Encomenda: {self.id_enc}\n"
            f"Origem: {self.origem}\n"
            f"Destino: {self.destino}\n"
            f"Hora de Chegada na Origem: {self.hora_chegada.strftime('%d/%m/%Y %H:%M:%S') if self.hora_chegada else 'N/A'}\n"
            f"Hora de Carregamento: {self.hora_carregamento.strftime('%d/%m/%Y %H:%M:%S') if self.hora_carregamento else 'N/A'}\n"
            f"Hora de Entrega: {self.hora_entrega.strftime('%d/%m/%Y %H:%M:%S') if self.hora_entrega else 'N/A'}\n"
        )
