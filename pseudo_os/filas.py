class GerenciadorFilas:
    def __init__(self):
        # Dicionário para manter filas separadas para cada nível de prioridade.
        # Prioridade 0 é a mais alta.
        self.filas_por_prioridade = {
            0: [],  # Fila de Tempo Real (Maior Prioridade)
            1: [],  # Fila de Usuário (Prioridade Média)
            2: []   # Fila de Batch (Menor Prioridade)
        }

    def adicionar_processo(self, processo):
        """Adiciona um processo à fila correspondente à sua prioridade."""
        prioridade = processo.prioridade
        if prioridade in self.filas_por_prioridade:
            self.filas_por_prioridade[prioridade].append(processo)
        else:
            # Caso um processo com prioridade inesperada apareça,
            # ele é colocado na fila de menor prioridade.
            print(f"AVISO: Processo {processo.pid} com prioridade inválida ({prioridade}). Alocado na fila de menor prioridade.")
            self.filas_por_prioridade[max(self.filas_por_prioridade.keys())].append(processo)

    def reenfileirar_processo(self, processo):
        """Adiciona um processo de volta ao FIM da sua fila de prioridade."""
        self.filas_por_prioridade[processo.prioridade].append(processo)

    def proximo_processo(self):
        for prioridade in sorted(self.filas_por_prioridade.keys()):
            if self.filas_por_prioridade[prioridade]:
                return self.filas_por_prioridade[prioridade].pop(0)
        return None

    def envelhecer_processos(self):
        """
        Implementa a técnica de aging para evitar starvation.
        Promove o processo mais antigo de uma fila de menor prioridade para uma mais alta.
        """
        # Começa a verificar da penúltima fila para cima
        for prioridade in sorted(self.filas_por_prioridade.keys(), reverse=True)[:-1]:
            fila_inferior_idx = prioridade
            fila_superior_idx = prioridade - 1

            if fila_superior_idx in self.filas_por_prioridade and self.filas_por_prioridade[fila_inferior_idx]:
                # Pega o processo que está esperando há mais tempo (o primeiro da fila)
                processo_a_promover = self.filas_por_prioridade[fila_inferior_idx].pop(0)
                
                # Diminui o valor da prioridade (ex: de 2 para 1) para promovê-lo
                processo_a_promover.prioridade = fila_superior_idx
                
                # Adiciona à fila de prioridade mais alta
                self.filas_por_prioridade[fila_superior_idx].append(processo_a_promover)
                
                print(f"AGING: Processo {processo_a_promover.pid} promovido para a prioridade {fila_superior_idx}.")
                # Para o loop para promover apenas um processo por vez
                return

    def tem_processos(self):
        """Verifica se ainda existe algum processo em qualquer uma das filas."""
        return any(self.filas_por_prioridade.values())