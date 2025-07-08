class GerenciadorRecursos:
    NUM_IMPRESSORAS = 2
    NUM_SCANNERS = 1
    NUM_MODEMS = 1
    NUM_DISCOS = 2

    def __init__(self):
        self.impressoras = [False] * self.NUM_IMPRESSORAS
        self.scanner = [False] * self.NUM_SCANNERS
        self.modem = [False] * self.NUM_MODEMS
        self.discos = [False] * self.NUM_DISCOS

    def alocar(self, processo):
        """Verifica se os recursos pedidos pelo processo estão disponíveis."""
        if processo.impressora_req > 0 and processo.impressora_req > self.NUM_IMPRESSORAS:
            print(f"Erro: Processo {processo.pid} requisitou impressora inexistente.")
            return False
        if processo.scanner_req and self.NUM_SCANNERS == 0:
            print(f"Erro: Processo {processo.pid} requisitou scanner inexistente.")
            return False
        return True

    def liberar(self, processo):
        """Libera os recursos que estavam alocados para o processo."""
        pass