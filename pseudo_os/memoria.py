class GerenciadorMemoria:
    TAMANHO_TOTAL_MEMORIA = 1024

    def __init__(self):
        # Inicializa a memória: None indica um bloco livre, PID indica um bloco ocupado.
        self.memoria = [None] * self.TAMANHO_TOTAL_MEMORIA

    def alocar(self, processo):
        """
        Aloca um bloco contíguo de memória para um processo (First-Fit).
        Retorna o offset se bem-sucedido, None caso contrário.
        """
        blocos_necessarios = processo.blocos_memoria
        contador_livre = 0
        inicio_bloco = -1

        for i, bloco in enumerate(self.memoria):
            if bloco is None:
                if contador_livre == 0:
                    inicio_bloco = i
                contador_livre += 1
                if contador_livre == blocos_necessarios:
                    # Bloco encontrado, realiza a alocação
                    for j in range(inicio_bloco, inicio_bloco + blocos_necessarios):
                        self.memoria[j] = processo.pid
                    processo.offset_memoria = inicio_bloco
                    return inicio_bloco
            else:
                contador_livre = 0
                inicio_bloco = -1
        
        return None # Não há espaço contíguo suficiente

    def liberar(self, processo):
        """Libera o bloco de memória alocado para um processo."""
        if processo.offset_memoria == -1:
            return False
        
        for i in range(processo.offset_memoria, processo.offset_memoria + processo.blocos_memoria):
            if i < len(self.memoria):
                self.memoria[i] = None
        
        processo.offset_memoria = -1
        return True