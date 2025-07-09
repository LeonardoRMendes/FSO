# pseudo_so/dispatcher.py

import sys
from processo import Processo
from memoria import GerenciadorMemoria
from recursos import GerenciadorRecursos
from arquivos import GerenciadorArquivos
from filas import GerenciadorFilas

def ler_arquivo_processos(caminho_arquivo):
    processos = []
    with open(caminho_arquivo, 'r') as f:
        for pid, linha in enumerate(f):
            partes = linha.strip().split(',')
            # Certificar que a prioridade é um inteiro
            partes[1] = int(partes[1])
            processos.append(Processo(pid, *partes))
    return processos

def ler_arquivo_operacoes(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        linhas = [linha.strip() for linha in f.readlines()]
    total_blocos = int(linhas[0])
    num_segmentos = int(linhas[1])
    arquivos_iniciais = []
    for i in range(2, 2 + num_segmentos):
        partes = linhas[i].split(',')
        arquivos_iniciais.append((partes[0].strip(), int(partes[1]), int(partes[2])))
    operacoes = []
    for i in range(2 + num_segmentos, len(linhas)):
        partes = [p.strip() for p in linhas[i].split(',')]
        operacoes.append(partes)
    return total_blocos, arquivos_iniciais, operacoes
# --- Fim das funções de leitura ---

def main():
    if len(sys.argv) != 3:
        print("Uso: python dispatcher.py <arquivo_processos> <arquivo_arquivos>")
        return

    CICLOS_PARA_AGING = 5 

    # Inicialização dos Módulos
    gerenciador_memoria = GerenciadorMemoria()
    gerenciador_recursos = GerenciadorRecursos()
    gerenciador_filas = GerenciadorFilas()
    
    lista_processos_inicial = ler_arquivo_processos(sys.argv[1])
    num_total_processos = len(lista_processos_inicial) #Salva o número total de processos para referência futura
    lista_processos_inicial.sort(key=lambda p: p.tempo_inicializacao)

    total_blocos, arquivos_iniciais, operacoes = ler_arquivo_operacoes(sys.argv[2])
    gerenciador_arquivos = GerenciadorArquivos(total_blocos, arquivos_iniciais)
    
    # Loop Principal de Execução com Preempção
    ciclos_dispatcher = 0
    processos_na_memoria = {} # Mapeia PID para processo

    while True:
        # Adiciona novos processos às filas conforme o tempo passa
        processos_chegando = [p for p in lista_processos_inicial if p.tempo_inicializacao <= ciclos_dispatcher]
        for p in processos_chegando:
            gerenciador_filas.adicionar_processo(p)
            lista_processos_inicial.remove(p)

        # Pega o próximo processo a ser executado
        processo_atual = gerenciador_filas.proximo_processo()

        if not processo_atual:
            if not lista_processos_inicial and not processos_na_memoria:
                # Se não há mais processos para chegar e nenhum na memória, termina.
                break
            # Avança o tempo se não houver processos prontos
            ciclos_dispatcher += 1
            continue

        # Se o processo não está na memória, tenta alocar
        if processo_atual.pid not in processos_na_memoria:
            offset = gerenciador_memoria.alocar(processo_atual)
            recursos_ok = gerenciador_recursos.alocar(processo_atual)

            if offset is not None and recursos_ok:
                processos_na_memoria[processo_atual.pid] = processo_atual
                print("dispatcher =>")
                print(processo_atual)
            else:
                # Se falhar a alocação de memória ou recursos, desfaz qualquer coisa feita
                if offset is not None:
                    gerenciador_memoria.liberar(processo_atual)
                if recursos_ok:
                    gerenciador_recursos.liberar(processo_atual)

                print(f"Falha ao alocar recursos/memória para o processo {processo_atual.pid}. Reenfileirando.")
                gerenciador_filas.filas_por_prioridade[processo_atual.prioridade].insert(0, processo_atual)
                ciclos_dispatcher += 1
                continue
        
        # --- LÓGICA DE PREEMPÇÃO ---
        terminou = False
        # Processos de tempo real (prioridade 0) não são preemptados
        if processo_atual.prioridade == 0:
            while not terminou:
                terminou = processo_atual.executar_quantum()
        else:
            # Processos de usuário são preemptados após 1 quantum
            terminou = processo_atual.executar_quantum()

        if terminou:
            # Se o processo terminou, libera seus recursos
            gerenciador_memoria.liberar(processo_atual)
            del processos_na_memoria[processo_atual.pid]
            gerenciador_recursos.liberar(processo_atual)
            print("-" * 20)
        else:
            # Se não terminou, volta para o FIM da sua fila (Round-Robin)
            gerenciador_filas.reenfileirar_processo(processo_atual)

        # Lógica de Aging
        if ciclos_dispatcher % CICLOS_PARA_AGING == 0 and ciclos_dispatcher > 0:
            gerenciador_filas.envelhecer_processos()

        ciclos_dispatcher += 1

    # Execução das Operações de Arquivo
    print("Sistema de arquivos =>")
    for i, op in enumerate(operacoes):
        pid_op = int(op[0])
        cod_op = int(op[1])
        nome_arq = op[2]

        if pid_op >= num_total_processos:
            print(f"Operação {i+1} => Falha")
            print(f"O processo {pid_op} não existe.")
            continue

        if cod_op == 0:
            tamanho_arq = int(op[3])
            sucesso, msg = gerenciador_arquivos.criar_arquivo(nome_arq, tamanho_arq)
            if sucesso:
                print(f"Operação {i+1} => Sucesso")
                print(f"O processo {pid_op} criou o arquivo {nome_arq} ({msg}).")
            else:
                print(f"Operação {i+1} => Falha")
                print(f"O processo {pid_op} não pode criar o arquivo {nome_arq} ({msg}).")

        elif cod_op == 1:
            sucesso, msg = gerenciador_arquivos.deletar_arquivo(nome_arq)
            if sucesso:
                print(f"Operação {i+1} => Sucesso")
                print(f"O processo {pid_op} deletou o arquivo {nome_arq}.")
            else:
                print(f"Operação {i+1} => Falha")
                print(f"O processo {pid_op} não pode deletar o arquivo {nome_arq} porque ele não existe.")
    
    print("-" * 20)
    gerenciador_arquivos.display_mapa()

if __name__ == "__main__":
    main()