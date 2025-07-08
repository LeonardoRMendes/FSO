class Processo:
    def __init__(self, pid, tempo_inicializacao, prioridade, tempo_processador, blocos_memoria, impressora_req, scanner_req, modem_req, disco_req):
        self.pid = pid
        self.tempo_inicializacao = int(tempo_inicializacao)
        self.prioridade = int(prioridade)
        self.tempo_processador = int(tempo_processador)
        self.blocos_memoria = int(blocos_memoria)
        self.impressora_req = int(impressora_req)
        self.scanner_req = bool(int(scanner_req))
        self.modem_req = bool(int(modem_req))
        self.disco_req = int(disco_req)
        
        self.estado = 'novo' # Estados possíveis: novo, pronto, executando, bloqueado, terminado
        self.offset_memoria = -1
        self.tempo_restante = self.tempo_processador

    def __str__(self):
        """Representação em string do processo para fácil visualização."""
        return (
            f"PID: {self.pid}\n"
            f"offset: {self.offset_memoria}\n"
            f"blocks: {self.blocos_memoria}\n"
            f"priority: {self.prioridade}\n"
            f"time: {self.tempo_processador}\n"
            f"printers: {self.impressora_req}\n"
            f"scanners: {self.scanner_req}\n"
            f"modems: {self.modem_req}\n"
            f"drives: {self.disco_req}"
        )

    def executar(self):
        """Simula a execução do processo."""
        print(f"process {self.pid} =>")
        print(f"P{self.pid} STARTED")
        for i in range(1, self.tempo_processador + 1):
            print(f"P{self.pid} instruction {i}")
            self.tempo_restante -= 1
        print(f"P{self.pid} return SIGINT")
