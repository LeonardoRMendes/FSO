class GerenciadorArquivos:
    def __init__(self, total_blocos, arquivos_iniciais):
        self.total_blocos = int(total_blocos)
        self.mapa_disco = [None] * self.total_blocos
        self.tabela_arquivos = {} # Mapeia nome do arquivo para (bloco_inicial, tamanho)

        for nome, bloco_inicial, tamanho in arquivos_iniciais:
            bloco_inicial = int(bloco_inicial)
            tamanho = int(tamanho)
            self.tabela_arquivos[nome] = (bloco_inicial, tamanho)
            for i in range(bloco_inicial, bloco_inicial + tamanho):
                self.mapa_disco[i] = nome

    def criar_arquivo(self, nome, tamanho):
        """Cria um novo arquivo (alocação contígua - First-Fit)."""
        if nome in self.tabela_arquivos:
            return False, "arquivo já existe"

        contador_livre = 0
        inicio_bloco = -1
        for i, bloco in enumerate(self.mapa_disco):
            if bloco is None:
                if contador_livre == 0:
                    inicio_bloco = i
                contador_livre += 1
                if contador_livre == tamanho:
                    # Espaço encontrado
                    for j in range(inicio_bloco, inicio_bloco + tamanho):
                        self.mapa_disco[j] = nome
                    self.tabela_arquivos[nome] = (inicio_bloco, tamanho)
                    return True, f"blocos {inicio_bloco} a {inicio_bloco + tamanho - 1}"
            else:
                contador_livre = 0
                inicio_bloco = -1
        
        return False, "falta de espaço"

    def deletar_arquivo(self, nome):
        """Deleta um arquivo do disco."""
        if nome not in self.tabela_arquivos:
            return False, "arquivo não existe"

        bloco_inicial, tamanho = self.tabela_arquivos[nome]
        for i in range(bloco_inicial, bloco_inicial + tamanho):
            self.mapa_disco[i] = None
        
        del self.tabela_arquivos[nome]
        return True, "sucesso"

    def display_mapa(self):
        """Exibe o mapa de ocupação do disco."""
        print("Mapa de ocupação do disco:")
        mapa_str = ""
        for bloco in self.mapa_disco:
            if bloco:
                mapa_str += f"{bloco} "
            else:
                mapa_str += "- "
        print(mapa_str.strip())