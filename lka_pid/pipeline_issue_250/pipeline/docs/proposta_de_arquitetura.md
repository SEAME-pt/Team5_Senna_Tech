# Proposta de Arquitetura

## Introdução

A arquitetura proposta para o pipeline ADAS tem como objetivo criar um sistema robusto, eficiente e modular, que permita a evolução contínua do projeto sem comprometer a qualidade do código nem a performance do sistema. Esta proposta define regras para a organização do código, a separação de responsabilidades entre módulos, a estrutura da `main` e a forma como novas features devem ser integradas ao pipeline.

Os princípios adotados nesta proposta são os seguintes:

1. **Conceito de camadas:** baseado em "Software Architecture in Practice", de Len Bass, Paul Clements e Rick Kazman. O sistema deve ser organizado em camadas com responsabilidades claras, onde camadas superiores dependem de serviços ou contratos das camadas inferiores, e não do contrário. Isso promove separação de responsabilidades e reduz acoplamento.

2. **Padrão Pipe-and-Filter:** também baseado em "Software Architecture in Practice". Cada etapa da pipeline deve receber um input definido, processá-lo e produzir um output consumido pela etapa seguinte. Isso facilita testes isolados, substituição de componentes e evolução controlada do fluxo.

3. **Princípios de responsabilidade e baixo acoplamento:** a proposta aplica principalmente os conceitos de `Single Responsibility` e `Dependency Inversion`, para garantir que cada módulo tenha uma responsabilidade clara e que as dependências entre partes do sistema sejam feitas por contratos estáveis, e não por detalhes internos de implementação.

## 1. Regras gerais para a pipeline de execucao do codigo ADAS

Nosso codigo de execucao do pipeline ADAS cresceu de forma organica, com foco em funcionalidade e resultados imediatos. Agora, para garantir a sustentabilidade do projeto, precisamos estabelecer regras claras de arquitetura que guiem a organizacao do codigo, a interacao entre modulos e a implementacao de novas features.

Os objetivos principais dessas regras sao:

- **Eficiencia:** Uma vez que precisamos ter um bom FPS, a arquitetura deve ser leve e otimizada, evitando sobrecarga desnecessaria e garantindo que cada modulo execute sua funcao de forma eficiente.
- **Modularidade:** O codigo deve ser dividido em modulos independentes, cada um com uma responsabilidade clara e interfaces bem definidas. Isso facilita a manutencao, o teste e a evolucao do sistema.
- **Orquestracao centralizada:** A `main` deve ser o ponto de controlo da execucao, mas sem conter logica de negocio. Ela deve coordenar a ordem de execucao dos modulos, garantir a passagem correta de dados e gerir o ciclo de vida da aplicacao.
- **Organizacao funcional:** Os modulos devem ser organizados com base na funcao que desempenham no sistema, evitando acoplamentos desnecessarios e promovendo a coesao interna de cada parte do codigo.
- **Evolucao controlada:** Toda nova feature deve ser implementada respeitando a arquitetura ja definida, garantindo que o sistema evolua de forma consistente e sem degradar a estrutura existente.

Essas regras servem para transformar a pipeline num sistema previsivel, testavel e evolutivo. Ao seguir essa base arquitetural, o projeto reduz o risco de regressao, melhora a clareza do fluxo de execucao e facilita a manutencao ao longo das proximas iteracoes.

## 2. Modulos e responsabilidades

Para garantir uma arquitetura clara e funcional, os modulos do sistema devem ser organizados com base em suas responsabilidades. Cada pacote pode utilizar um `__init__.py` para expor sua API publica quando isso fizer sentido, mas a definicao da interface do modulo deve estar principalmente nas classes, funcoes e contratos de dados que ele disponibiliza. A seguir, uma proposta de organizacao:

- **Camera:** responsavel por capturar imagens e fornecer frames ao pipeline.
- **Inference:** responsavel por executar os modelos de inferencia e devolver resultados crus.
- **Post-Processing:** responsavel por traduzir os outputs crus dos modelos em estruturas utilizaveis pelo dominio.
- **LFA:** responsavel pela logica de deteccao e interpretacao de faixa. Dentro deste modulo ficam etapas como `BEV Transform`, `Sliding Windows` e calculo de `CTE`.
- **Object Perception:** responsavel pela deteccao, classificacao e interpretacao de objetos relevantes para a conducao.
- **Decision and Control:** responsavel por FSM, PID e definicao da resposta do veiculo.
- **CAN Bus / External Interfaces:** responsavel por enviar comandos ao veiculo e integrar interfaces externas, como CAN e Kuksa.
- **Display/Debug:** responsavel por visualizacao, overlays e suporte a validacao durante o desenvolvimento.

Essa organizacao evita confundir etapa de processamento com fronteira arquitetural. `BEV`, `Sliding Windows` e `CTE`, por exemplo, fazem parte do dominio de LFA, mas nao precisam necessariamente existir como modulos independentes de primeiro nivel.

Cada modulo deve ser projetado para ser o mais independente possivel, com interfaces claras e bem definidas. Isso permite que cada parte do sistema evolua de forma isolada, facilitando a manutencao e a adicao de novas funcionalidades sem impactar outras partes do codigo.

## 3. Organizaçao da `main` e orquestracao da execucao

A `main` deve seguir uma estrutura de controlo clara, onde cada etapa do pipeline e executada numa ordem logica, garantindo que os dados fluam de forma consistente e previsivel. A `main` deve funcionar como orquestradora do sistema e nao como concentradora de regras de negocio.

De forma geral, a ordem de execucao pode seguir o seguinte fluxo:

1. Captura de frames da camera
2. Execucao dos modelos de inferencia
3. Post-processamento dos resultados da inferencia
4. Transformacao para BEV
5. Aplicacao de sliding windows
6. Calculo do CTE
7. Execucao do controlador PID
8. Envio de comandos para o veiculo atraves do CAN Bus

Cada etapa deve ser claramente separada, com chamadas a funcoes ou metodos dos modulos correspondentes. A `main` deve ser responsavel apenas por coordenar a execucao e garantir a passagem correta de dados entre os modulos, sem conter logica de negocio, formulas de decoder, regras de geometria ou processamento especifico de hardware que possa ser encapsulado noutro componente.

Essa abordagem torna a `main` mais facil de compreender, manter e testar. Quanto mais enxuta ela for, mais claro fica o fluxo do sistema e menor e o risco de transformar a orquestracao central num novo ponto de acoplamento.

## 4. Comunicação entre modulos e contratos de dados

A comunicacao entre os modulos deve ser feita atraves de interfaces bem definidas, onde cada modulo expoe apenas as funcionalidades necessarias para interagir com os demais. Os contratos de dados devem ter inputs e outputs claros, garantindo que cada modulo saiba exatamente o que recebe e o que deve produzir.

Exemplo de inputs e outputs ao longo da pipeline:

- **Camera:** input inexistente; output `bgr (H, W, 3) uint8`
- **Inference:** input `bgr`; output `outputs_lane (dict)`, `outputs_obj (dict)`
- **Post-Processing:** input `outputs_lane`; output `binary_mask (H, W) uint8`
- **BEV Transform:** input `binary_mask`; output `bev_mask (H, W) uint8`
- **Sliding Windows:** input `bev_mask`; output `fit_result (LaneFitResult)`
- **CTE:** input `fit_result.cte_norm`; output `cte (float [-1, 1])`
- **PID:** input `cte`, `dt`; output `pid_return (float [-1, 1])`
- **CAN Bus:** input `pid_return`, `current_state`; output comando CAN `0x110`, `0x001`

Sempre que possivel, esses contratos devem ser representados por tipos, dataclasses, enums ou estruturas documentadas. Isso reduz ambiguidades, melhora a legibilidade do codigo e facilita testes unitarios e de integracao.

Essa abordagem reforca a separacao de responsabilidades e melhora a identificacao de falhas, porque cada modulo passa a ter comportamento esperado e fronteiras tecnicas mais claras.

## 5. Implementação de novas features e evolução do sistema

Toda nova feature deve ser implementada respeitando a arquitetura ja definida, garantindo que o sistema evolua de forma consistente e sem degradar a estrutura existente. Isso significa que qualquer nova funcionalidade deve ser adicionada como um novo modulo ou como extensao de um modulo existente, seguindo as regras de comunicacao e os contratos de dados estabelecidos.

Antes da implementacao, e importante responder a algumas perguntas:

- Em que camada a feature pertence?
- Qual e o input esperado?
- Qual e o output esperado?
- Ela adiciona acoplamento desnecessario a `main`?
- Ela pode ser testada de forma isolada?

Tambem e importante garantir que novas features sejam testadas com testes unitarios e de integracao sempre que possivel. Isso ajuda a identificar regressões, validar contratos e reduzir o risco de impacto negativo sobre a performance ou o comportamento global da pipeline.

Cada modulo deve conter documentacao clara sobre suas responsabilidades, interfaces e relacao com a arquitetura geral do sistema. Isso facilita a compreensao do codigo por parte de outros desenvolvedores e melhora a colaboracao dentro da equipa.

## 6. Conclusão

A arquitetura proposta para o pipeline ADAS e baseada em principios de separacao de responsabilidades, modularidade, contratos claros de dados e orquestracao centralizada. Ao seguir essas diretrizes, o projeto ganha previsibilidade, melhora a capacidade de manutencao e reduz o custo de evolucao ao longo do tempo.

Mais do que reorganizar ficheiros, esta proposta define uma regra de implementacao para o pipeline. O objetivo e garantir que o sistema possa crescer de forma controlada, mantendo clareza estrutural, consistencia tecnica e alinhamento com as necessidades atuais e futuras do projeto.
