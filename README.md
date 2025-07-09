# Pseudo-SO: Simulador de Sistema Operacional em Python

Este projeto é uma simulação de um sistema operacional básico, desenvolvido em Python, que gerencia processos, memória, recursos de E/S e um sistema de arquivos simples.  
O objetivo é demonstrar conceitos fundamentais de sistemas operacionais, como escalonamento de processos com prioridades, alocação de memória e gerenciamento de disco.

## Funcionalidades

- **Gerenciamento de Processos**: Criação e execução de processos com base em um arquivo de entrada.
- **Escalonador com Prioridades**: Utiliza múltiplas filas (tempo real, usuário) para escalonar processos.
- **Prevenção de Starvation**: Implementa uma técnica de *aging* para garantir que processos de baixa prioridade também sejam executados.
- **Gerenciamento de Memória**: Simula a alocação e liberação de blocos de memória principal (RAM) de forma contígua.
- **Gerenciamento de Recursos**: Controla a alocação de recursos de E/S, como impressoras e scanners.
- **Sistema de Arquivos**: Simula operações de criação e deleção de arquivos em um disco, com um mapa de ocupação.

## Pré-requisitos

Para executar este projeto, você precisará ter o **Python 3** instalado em seu sistema.  
Não são necessárias bibliotecas externas além das que já vêm com o Python.

## Estrutura de Arquivos

O projeto está organizado de forma modular para facilitar a compreensão e manutenção:

```
pseudo_so/
├── dispatcher.py         # Módulo principal (orquestrador)
├── processo.py           # Define a classe Processo (PCB)
├── memoria.py            # Gerenciador de Memória RAM
├── recursos.py           # Gerenciador de Recursos de E/S
├── arquivos.py           # Gerenciador do Sistema de Arquivos
├── filas.py              # Gerenciador das Filas de Processos
├── processes.txt         # Arquivo de entrada para definir os processos
└── files.txt             # Arquivo de entrada para operações de arquivo
```

## Configuração dos Arquivos de Entrada

O comportamento da simulação é definido por dois arquivos de texto: `processes.txt` e `files.txt`.

### 1. `processes.txt`

Cada linha neste arquivo representa um processo a ser criado.

**Formato por linha**:

```
<tempo de inicialização>, <prioridade>, <tempo de processador>, <blocos em memória>, <impressora>, <scanner>, <modem>, <disco>
```

**Exemplo**:

```
2, 0, 3, 64, 0, 0, 0, 0
8, 1, 2, 64, 0, 0, 0, 0
```

### 2. `files.txt`

Este arquivo descreve o estado inicial do disco e as operações de arquivo a serem executadas.

**Formato**:

- **Linha 1**: Quantidade total de blocos no disco.  
- **Linha 2**: Quantidade de arquivos já existentes no disco.  
- **Próximas linhas**: Descrição de cada arquivo existente:

```
<nome>, <bloco_inicial>, <tamanho>
```

- **Linhas seguintes**: Operações a serem executadas:

```
<ID_Processo>, <Código_Operação>, <Nome_Arquivo>[, <tamanho_se_criar>]
```

> **Código de Operação**:  
> `0` para criar, `1` para deletar.

**Exemplo**:

```
10
3
X, 0, 2
Y, 3, 1
Z, 5, 3
0, 0, A, 5
0, 1, X
2, 0, B, 2
```

## Como Executar

Siga os passos abaixo para rodar a simulação:

1. **Clone o Projeto**  
   Certifique-se de que todos os arquivos listados na estrutura do projeto estejam na mesma pasta.

2. **Prepare os Arquivos de Entrada**  
   Verifique se os arquivos `processes.txt` e `files.txt` estão na mesma pasta que os scripts Python e configurados conforme desejado.

3. **Abra um Terminal**  
   Navegue até o diretório onde você salvou os arquivos do projeto:

   ```bash
   cd caminho/para/a/pasta/pseudo_so
   ```

4. **Execute o Dispatcher**  
   Execute o script `dispatcher.py` passando os nomes dos arquivos de processos e de arquivos como argumentos de linha de comando:

   **Sintaxe**:

   ```bash
   python dispatcher.py <arquivo_de_processos> <arquivo_de_arquivos>
   ```

   **Exemplo**:

   ```bash
   python dispatcher.py processes.txt files.txt
   ```
