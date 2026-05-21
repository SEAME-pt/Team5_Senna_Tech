# [ADR-005] Arquitectura Modular da Pipeline ADAS
Status: Accepted

Date: 21-05-2026

### 1. Contexto e Problema

A pipeline ADAS cresceu de forma orgânica, com foco em funcionalidade e resultados imediatos. O código inicial concentrava inferência, pós-processamento, lógica de decisão e display num único script, criando acoplamento elevado, dificuldade de manutenção e risco de regressão a cada nova feature adicionada.

Estado actual: pipeline modular implementada em `pipeline_issue_250/` com módulos `camera`, `inference`, `post_processing`, `LFA`, `decision`, `kuksa_publish` e `utils`, orquestrados por um `main.py` sem lógica de negócio.

Driver/Trigger: Necessidade de escalar o sistema com novas features (obstacle avoidance, adaptive cruise, lane tracking) sem degradar a estrutura existente nem introduzir regressões.

### 2. Opções Consideradas

Opção A: Pipeline Monolítica — manter toda a lógica num único script, crescendo por adição de funções e variáveis globais.

Opção B: Arquitectura Modular em Camadas com Pipe-and-Filter — organizar o sistema em módulos independentes com responsabilidades claras, contratos de dados definidos e `main` como orquestrador puro.

Opção C: Microserviços com IPC/Sockets — isolar cada módulo como processo independente com comunicação via sockets ou filas de mensagens.

### 3. Decisão

Chosen Option: Opção B — Arquitectura Modular em Camadas com Pipe-and-Filter, porque equilibra separação de responsabilidades com performance real-time na Raspberry Pi 5 + Hailo-8, sem o overhead de comunicação inter-processo da Opção C.

### 4. Pros e Cons das Opções

**Opção A: Pipeline Monolítica**

* Good: Rápida de prototipar e simples de correr.
* Good: Sem overhead de imports ou interfaces entre módulos.
* Bad: Acoplamento total — uma alteração pode quebrar qualquer parte do sistema.
* Bad: Impossível testar componentes em isolamento.
* Bad: `main` torna-se um concentrador de lógica de negócio, difícil de ler e manter.

**Opção B: Arquitectura Modular em Camadas com Pipe-and-Filter**

* Good: Cada módulo tem responsabilidade única e interface clara.
* Good: Permite substituir ou evoluir componentes sem impacto nos outros módulos.
* Good: `main` actua como orquestrador puro — fácil de ler e auditar o fluxo completo.
* Good: Contratos de dados explícitos (`LaneFitResult`, `EnvironmentState`) reduzem ambiguidade.
* Good: Compatível com os requisitos de performance real-time do Raspberry Pi 5 + Hailo-8.
* Bad: Requer disciplina para manter as fronteiras entre módulos ao longo do tempo.
* Bad: Maior overhead inicial de organização comparado com a abordagem monolítica.

**Opção C: Microserviços com IPC/Sockets**

* Good: Máximo isolamento — falha num processo não derruba os outros.
* Bad: Latência de comunicação inter-processo inaceitável para pipeline real-time a 15+ FPS.
* Bad: Complexidade operacional elevada (gestão de processos, sincronização, serialização).

### 5. Follow-up Tasks

[ None ]
