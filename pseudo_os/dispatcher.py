import sys
from processo import Processo
from memoria import GerenciadorMemoria
from recursos import GerenciadorRecursos
from arquivos import GerenciadorArquivos
from filas import GerenciadorFilas

def ler_arquivo_processos(caminho_arquivo):
    """Lê o arquivo de processos e retorna uma lista de objetos Processo."""
    processos = []
    with open(caminho_arquivo, 'r') as f:
        for pid, linha in enumerate(f):
            partes = linha.strip().split(',')
            processos.append(Processo(pid, *partes))
    return processos

def ler_arquivo_operacoes(caminho_arquivo):
    """Lê o arquivo de arquivos/operações e retorna os dados."""
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

def main():
    if len(sys.argv) != 3:
        print("Uso: python dispatcher.py <arquivo_processos> <arquivo_arquivos>")
        return

    # Inicialização dos Módulos
    gerenciador_memoria = GerenciadorMemoria()
    gerenciador_recursos = GerenciadorRecursos()
    gerenciador_filas = GerenciadorFilas()
    
    # Carregar Processos
    lista_processos = ler_arquivo_processos(sys.argv[1])
    for p in lista_processos:
        gerenciador_filas.adicionar_processo(p)

    # Carregar Sistema de Arquivos
    total_blocos, arquivos_iniciais, operacoes = ler_arquivo_operacoes(sys.argv[2])
    gerenciador_arquivos = GerenciadorArquivos(total_blocos, arquivos_iniciais)
    
    # Loop Principal de Execução (Simulação)
    while (processo_atual := gerenciador_filas.proximo_processo()):
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
        else:
            # Falha na alocação
            print(f"Processo {processo_atual.pid} não pôde ser alocado.")
            # Aqui, poderíamos colocar o processo de volta na fila para tentar mais tarde
        
        print("-" * 20)

    # Execução das Operações de Arquivo
    print("Sistema de arquivos =>")
    for i, op in enumerate(operacoes):
        pid_op = int(op[0])
        cod_op = int(op[1])
        nome_arq = op[2]

        # Verifica se o processo que solicitou a operação existe
        if pid_op >= len(lista_processos):
            print(f"Operação {i+1} => Falha")
            print(f"O processo {pid_op} não existe.")
            continue

        if cod_op == 0: # Criar
            tamanho_arq = int(op[3])
            sucesso, msg = gerenciador_arquivos.criar_arquivo(nome_arq, tamanho_arq)
            if sucesso:
                print(f"Operação {i+1} => Sucesso")
                print(f"O processo {pid_op} criou o arquivo {nome_arq} ({msg}).")
            else:
                print(f"Operação {i+1} => Falha")
                print(f"O processo {pid_op} não pode criar o arquivo {nome_arq} ({msg}).")

        elif cod_op == 1: # Deletar
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
