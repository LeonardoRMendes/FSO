class Processo:
    """
    Representa o Bloco de Controle de Processo (PCB).
    Armazena todas as informações vitais sobre um processo.
    """
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
        
        self.estado = 'novo'
        self.offset_memoria = -1
        # Mantém o controle do tempo restante para o processo.
        self.tempo_restante = self.tempo_processador
        # Contador para saber qual instrução está sendo executada.
        self.instrucao_atual = 1

    def __str__(self):
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

    def executar_quantum(self):
        """
        Executa uma única instrução (quantum de 1ms) do processo.
        Retorna True se o processo terminou, False caso contrário.
        """
        if self.tempo_restante > 0:
            if self.instrucao_atual == 1:
                 print(f"process {self.pid} =>")
                 print(f"P{self.pid} STARTED")
                 
            print(f"P{self.pid} instruction {self.instrucao_atual}")
            self.tempo_restante -= 1
            self.instrucao_atual += 1

            if self.tempo_restante == 0:
                print(f"P{self.pid} return SIGINT")
                return True  # Processo terminou
        
        return False # Processo ainda não terminou