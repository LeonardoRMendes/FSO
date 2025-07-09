class GerenciadorRecursos:
    NUM_IMPRESSORAS = 2
    NUM_SCANNERS = 1
    NUM_MODEMS = 1
    NUM_DISCOS = 2

    def __init__(self):
        self.impressoras = [False] * self.NUM_IMPRESSORAS
        self.scanners = [False] * self.NUM_SCANNERS
        self.modems = [False] * self.NUM_MODEMS
        self.discos = [False] * self.NUM_DISCOS

    def alocar(self, processo):
        """
        Tenta alocar os recursos pedidos pelo processo.
        Retorna True se todos os recursos forem alocados com sucesso.
        """
        # Processos de tempo real não usam recursos
        if processo.prioridade == 0:
            return True

        # Impressora
        if processo.impressora_req > 0:
            idx = processo.impressora_req - 1
            if idx >= self.NUM_IMPRESSORAS or self.impressoras[idx]:
                return False
            self.impressoras[idx] = True

        # Scanner
        if processo.scanner_req > 0:
            if self.scanners[0]:
                return False
            self.scanners[0] = True

        # Modem
        if processo.modem_req > 0:
            if self.modems[0]:
                return False
            self.modems[0] = True

        # Disco
        if processo.disco_req > 0:
            idx = processo.disco_req - 1
            if idx >= self.NUM_DISCOS or self.discos[idx]:
                return False
            self.discos[idx] = True

        return True

    def liberar(self, processo):
        """Libera os recursos usados pelo processo."""
        if processo.prioridade == 0:
            return

        # Impressora
        if processo.impressora_req > 0:
            idx = processo.impressora_req - 1
            if idx < self.NUM_IMPRESSORAS:
                self.impressoras[idx] = False

        # Scanner
        if processo.scanner_req > 0:
            self.scanners[0] = False

        # Modem
        if processo.modem_req > 0:
            self.modems[0] = False

        # Disco
        if processo.disco_req > 0:
            idx = processo.disco_req - 1
            if idx < self.NUM_DISCOS:
                self.discos[idx] = False