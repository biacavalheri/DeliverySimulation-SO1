# DeliverySimulation-SO1
Este projeto simula o comportamento de uma rede de entregas, onde encomendas são transportadas por veículos de pontos de redistribuição até seus destinos. A aplicação foi desenvolvida em Python utilizando conceitos de programação concorrente com threads, semáforos e variáveis de controle.

## Funcionalidades
- Simulação de **S** pontos de redistribuição.
- **C** veículos que transportam encomendas.
- **P** encomendas a serem entregues.
- Cada veículo possui **A** espaços de carga para acomodar as encomendas.

## Como Funciona

### Pontos de Redistribuição:
- Cada ponto é responsável por gerenciar uma fila de encomendas que aguardam para ser despachadas.
- O acesso a cada ponto é sincronizado utilizando um `Lock`, garantindo que apenas um veículo seja atendido por vez.

### Veículos:
- Os veículos são representados por threads que circulam entre os pontos de redistribuição.
- Cada veículo tenta despachar encomendas de um ponto atual, e, se não houver encomendas disponíveis, move-se para o próximo ponto.
- O tempo de viagem entre pontos é aleatório, simulando a variabilidade nas entregas.

### Encomendas:
- As encomendas também são tratadas como threads que gerenciam seu ciclo de vida, desde a chegada em um ponto até a entrega no destino.
- Ao chegar ao ponto de origem, a encomenda é adicionada à fila do ponto e espera para ser carregada por um veículo.
- O rastro de cada encomenda é salvo em um arquivo, registrando horários de chegada, carregamento e descarregamento.

## Dependências
- Python 3.x

## Estrutura do Código
- **PontoRedistribuicao**: Classe que representa um ponto de redistribuição, gerencia a fila de encomendas.
- **Veiculo**: Classe que representa um veículo, é responsável por carregar e entregar encomendas.
- **Encomenda**: Classe que representa uma encomenda, gerencia seu ciclo de vida e grava seu rastro.
- **main()**: Função principal que inicializa os pontos, veículos e encomendas, gerenciando sua execução.
