# DeliverySimulation-SO1

**Disciplina**: Sistemas Operacionais I  
**Professor**: Prof. Dr. Caetano Mazzoni Ranieri  
**Instituição**: Universidade Estadual Paulista (UNESP)  
**Departamento**: Estatística, Matemática Aplicada e Computação

---

## Descrição do Projeto

Este projeto simula o comportamento de uma rede de entregas onde veículos transportam encomendas de pontos de redistribuição até seus destinos. A aplicação foi desenvolvida em Python utilizando conceitos de programação concorrente, como threads, semáforos e variáveis de controle.

---

## Funcionalidades

- Simulação de **S** pontos de redistribuição.
- **C** veículos responsáveis pelo transporte das encomendas.
- **P** encomendas a serem entregues.
- Cada veículo possui **A** espaços de carga para acomodar as encomendas.

---

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

---

## Dependências
- Python 3.x
- Bibliotecas utilizadas:
    -   `tkinter` (para interface gráfica).

---

## Como Executar

1. Clone este repositório:

    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd <NOME_DO_REPOSITORIO>
    ```

2. Execute o programa principal:

    ```bash
    python main.py
    ```

3. Insira os parâmetros solicitados:

    - **S**: Número de pontos de redistribuição.
    - **C**: Número de veículos.
    - **P**: Número de encomendas.
    - **A**: Número de espaços de carga por veículo.

4. A interface gráfica será aberta, e os arquivos de logs serão gerados no diretório `logs`.

---

## Argumentos de Entrada

O programa solicita os seguintes parâmetros de entrada:

| Parâmetro | Descrição                               |
| --------- | --------------------------------------- |
| **S**     | Número de pontos de redistribuição.     |
| **C**     | Número de veículos disponíveis.         |
| **P**     | Número total de encomendas.             |
| **A**     | Número de espaços de carga por veículo. |

### Exemplo de Entrada

```
Digite o número de pontos de redistribuição (S): 5
Digite o número de veículos (C): 3
Digite o número de encomendas (P): 10
Digite o número de espaços de carga em cada veículo (A): 2
```

---

## Saídas

1. **Interface gráfica**:

    - Exibe os pontos de redistribuição, veículos e status das filas em tempo real.

2. **Logs de rastreamento**:
    - Diretório `logs/` contendo um arquivo para cada encomenda.
    - Exemplo de arquivo de log:
        ```
        logs/rastro_encomenda_0.txt
        ```
        **Conteúdo do log**:
        ```
        ID da Encomenda: 0
        Origem: 2
        Destino: 4
        Hora de Chegada na Origem: 1698439200.123456
        Hora de Carregamento: 1698439205.654321
        Hora de Descarregamento: 1698439210.789012
        ```

---

## Estrutura do Projeto

```
.
├── main.py               # Ponto de entrada da aplicação
├── src/
│   ├── Interface.py      # Interface gráfica (Tkinter)
│   ├── RedeEntrega.py    # Gerenciamento central do sistema
│   ├── GerenciadorEncomendas.py  # Controle das encomendas
│   ├── GerenciadorVeiculos.py    # Controle dos veículos
└── logs/                 # Diretório onde os logs são salvos
```

---

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

---

## Desenvolvedores

-   Beatriz Cavalheri
-   Larissa Rodrigues Ferrari
-   Murilo Augusto Venturato

