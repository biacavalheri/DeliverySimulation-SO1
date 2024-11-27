# DeliverySimulation-SO1

Este projeto simula o comportamento de uma rede de entregas onde veículos transportam encomendas de pontos de redistribuição até seus destinos. A aplicação foi desenvolvida em Python utilizando conceitos de programação concorrente, como threads, semáforos e variáveis de controle.

## Funcionalidades

- Simulação de **S** pontos de redistribuição.
- **C** veículos responsáveis pelo transporte das encomendas.
- **P** encomendas a serem entregues.
- Cada veículo possui **A** espaços de carga para acomodar as encomendas.

## Como Funciona

### Pontos de Redistribuição:
- Cada ponto de redistribuição é responsável por gerenciar uma fila de encomendas que aguardam para serem despachadas.
- O acesso a cada ponto é sincronizado utilizando um `semáforo`, garantindo que apenas um veículo seja atendido por vez.
  
### Veículos:
- Os veículos são representados como threads que circulam entre os pontos de redistribuição.
- Cada veículo tenta despachar encomendas do ponto em que está. Caso não haja encomendas disponíveis, o veículo se move para o próximo ponto.
- O tempo de viagem entre os pontos é aleatório, simulando a variabilidade nas entregas.

### Encomendas:
- As encomendas são tratadas como threads, gerenciando seu ciclo de vida, desde a chegada ao ponto de origem até a entrega no destino.
- Ao chegar a um ponto de origem, a encomenda é colocada na fila de espera do ponto e aguarda para ser carregada por um veículo.
- O rastro de cada encomenda é registrado em um arquivo, contendo horários de chegada, carregamento e descarregamento.

## Dependências
- Python 3.x

## Estrutura do Código

A estrutura do código é organizada em classes que representam os diferentes elementos da simulação. Cada classe tem responsabilidades específicas, de forma que a simulação seja executada de maneira eficiente.

- **PontoRedistribuicao**:  
  Classe que representa um ponto de redistribuição. Cada ponto é responsável por gerenciar uma fila de encomendas que aguardam para serem despachadas. O ponto utiliza um **semáforo** para controlar o número de veículos que podem ser atendidos simultaneamente.  
  Responsabilidades:
  - Gerenciar a fila de encomendas.
  - Controlar o acesso ao ponto de redistribuição através de semáforo.

- **Veiculo**:  
  Classe que representa um veículo na simulação. Cada veículo é responsável por transportar encomendas de um ponto de redistribuição até o seu destino. Os veículos são representados por **threads**, permitindo que eles operem de forma concorrente, visitando vários pontos e realizando entregas.  
  Responsabilidades:
  - Transportar encomendas entre pontos de redistribuição.
  - Despachar e carregar encomendas em pontos de redistribuição.
  - Garantir a movimentação entre pontos com intervalos de tempo simulados aleatoriamente.

- **Encomenda**:  
  Classe que representa uma encomenda na simulação. Cada encomenda é tratada como uma thread, com seu ciclo de vida registrado desde o momento em que chega a um ponto de redistribuição até a entrega final.  
  Responsabilidades:
  - Gerenciar o ciclo de vida da encomenda, desde a chegada até a entrega.
  - Registrar os horários de chegada, carregamento e descarregamento da encomenda em um arquivo de rastreamento.

- **main()**:  
  Função principal do programa. Ela inicializa os pontos de redistribuição, veículos e encomendas, gerenciando a execução da simulação. A função também coordena a criação e execução das threads, controlando o andamento da entrega das encomendas.  
  Responsabilidades:
  - Inicializar os pontos de redistribuição, veículos e encomendas.
  - Iniciar a execução das threads.
  - Gerenciar o ciclo completo da simulação, controlando o tempo de execução e o rastreamento das encomendas.

Cada componente da simulação é independente, mas trabalha em conjunto para criar uma rede de entregas eficiente e realista, utilizando conceitos de concorrência para simular o transporte e a entrega das encomendas.
