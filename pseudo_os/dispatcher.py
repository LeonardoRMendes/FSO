# pseudo_so/dispatcher.py

import sys
from processo import Processo
from memoria import GerenciadorMemoria
from recursos import GerenciadorRecursos
from arquivos import GerenciadorArquivos
from filas import GerenciadorFilas # Agora com a lógica de prioridade

# --- Funções de leitura de arquivo (permanecem as mesmas) ---
def ler_arquivo_processos(caminho_arquivo):
    processos = []
    with open(caminho_arquivo, 'r') as f:
        for pid, linha in enumerate(f):
            partes = linha.strip().split(',')
            # Certifique-se de que a prioridade é um inteiro
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

    # Constante para a técnica de Aging
    # A cada N processos executados, o envelhecimento é acionado.
    CICLOS_PARA_AGING = 3

    # Inicialização dos Módulos
    gerenciador_memoria = GerenciadorMemoria()
    gerenciador_recursos = GerenciadorRecursos()
    gerenciador_filas = GerenciadorFilas() # Nova implementação
    
    # Carregar Processos
    lista_processos = ler_arquivo_processos(sys.argv[1])
    # Organiza os processos por tempo de inicialização antes de adicionar às filas
    lista_processos.sort(key=lambda p: p.tempo_inicializacao)
    for p in lista_processos:
        gerenciador_filas.adicionar_processo(p)

    # Carregar Sistema de Arquivos
    total_blocos, arquivos_iniciais, operacoes = ler_arquivo_operacoes(sys.argv[2])
    gerenciador_arquivos = GerenciadorArquivos(total_blocos, arquivos_iniciais)
    
    # Loop Principal de Execução (Simulação)
    ciclos_dispatcher = 0
    while gerenciador_filas.tem_processos():
        processo_atual = gerenciador_filas.proximo_processo()
        if not processo_atual:
            # Isso não deveria acontecer se .tem_processos() for True, mas é uma boa prática
            break
            
        print("dispatcher =>")
        
        # Alocar memória e recursos
        offset = gerenciador_memoria.alocar(processo_atual)
        recursos_ok = gerenciador_recursos.alocar(processo_atual)

        if offset is not None and recursos_ok:
            processo_atual.estado = 'pronto'
            print(processo_atual)
            
            # Simular execução
            processo_atual.estado = 'executando'
            processo_atual.executar()
            processo_atual.estado = 'terminado'
            
            # Liberar memória e recursos
            gerenciador_memoria.liberar(processo_atual)
            gerenciador_recursos.liberar(processo_atual)

            ciclos_dispatcher += 1
            # Aciona o envelhecimento a cada N ciclos
            if ciclos_dispatcher % CICLOS_PARA_AGING == 0:
                print("-" * 20)
                gerenciador_filas.envelhecer_processos()
                print("-" * 20)

        else:
            print(f"Falha ao alocar recursos para o processo {processo_atual.pid}. Reenfileirando.")
            # Libera o que quer que tenha sido pré-alocado
            if offset is not None:
                gerenciador_memoria.liberar(processo_atual)
            # Devolve o processo para o início da sua fila de prioridade para tentar novamente no futuro
            gerenciador_filas.filas_por_prioridade[processo_atual.prioridade].insert(0, processo_atual)
        
        print("-" * 20)

    # Execução das Operações de Arquivo (lógica inalterada)
    print("Sistema de arquivos =>")
    for i, op in enumerate(operacoes):
        pid_op = int(op[0])
        cod_op = int(op[1])
        nome_arq = op[2]

        if pid_op >= len(lista_processos):
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