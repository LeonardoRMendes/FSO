class GerenciadorFilas:
    def __init__(self):
        self.fila_de_prontos = []

    def adicionar_processo(self, processo):
        self.fila_de_prontos.append(processo)
        # Ordena a fila pelo tempo de inicialização para simular a chegada
        self.fila_de_prontos.sort(key=lambda p: p.tempo_inicializacao)

    def proximo_processo(self):
        """Retorna o próximo processo a ser executado."""
        if self.fila_de_prontos:
            return self.fila_de_prontos.pop(0)
        return None
