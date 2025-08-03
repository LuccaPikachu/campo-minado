import random

class CampoMinado:
    def __init__(self, linhas=8, colunas=8, minas=10):
        self.linhas = linhas
        self.colunas = colunas
        self.minas = minas
        self.tabuleiro = [[0 for _ in range(colunas)] for _ in range(linhas)]
        self.revelado = [[False for _ in range(colunas)] for _ in range(linhas)]
        self.marcado = [[False for _ in range(colunas)] for _ in range(linhas)]
        self.game_over = False
        self.vitoria = False
        self._colocar_minas()
        self._calcular_numeros()

    def _colocar_minas(self):
        minas_colocadas = 0
        while minas_colocadas < self.minas:
            linha = random.randint(0, self.linhas - 1)
            coluna = random.randint(0, self.colunas - 1)
            if self.tabuleiro[linha][coluna] != -1:
                self.tabuleiro[linha][coluna] = -1
                minas_colocadas += 1

    def _calcular_numeros(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.tabuleiro[i][j] != -1:
                    count = 0
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < self.linhas and 0 <= nj < self.colunas:
                                if self.tabuleiro[ni][nj] == -1:
                                    count += 1
                    self.tabuleiro[i][j] = count

    def revelar(self, linha, coluna):
        if self.game_over or self.revelado[linha][coluna] or self.marcado[linha][coluna]:
            return

        self.revelado[linha][coluna] = True

        if self.tabuleiro[linha][coluna] == -1:
            self.game_over = True
            return

        if self.tabuleiro[linha][coluna] == 0:
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    ni, nj = linha + di, coluna + dj
                    if 0 <= ni < self.linhas and 0 <= nj < self.colunas:
                        if not self.revelado[ni][nj]:
                            self.revelar(ni, nj)

        self._verificar_vitoria()

    def marcar(self, linha, coluna):
        if not self.revelado[linha][coluna]:
            self.marcado[linha][coluna] = not self.marcado[linha][coluna]

    def _verificar_vitoria(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.tabuleiro[i][j] != -1 and not self.revelado[i][j]:
                    return
        self.vitoria = True

    def mostrar_tabuleiro(self):
        print("   ", end="")
        for j in range(self.colunas):
            print(f"{j:2}", end=" ")
        print()

        for i in range(self.linhas):
            print(f"{i:2} ", end="")
            for j in range(self.colunas):
                if self.marcado[i][j]:
                    print(" F", end=" ")
                elif not self.revelado[i][j]:
                    print(" .", end=" ")
                elif self.tabuleiro[i][j] == -1:
                    print(" *", end=" ")
                elif self.tabuleiro[i][j] == 0:
                    print("  ", end=" ")
                else:
                    print(f"{self.tabuleiro[i][j]:2}", end=" ")
            print()

def main():
    print("=== CAMPO MINADO ===")
    print("Comandos:")
    print("r linha coluna - revelar célula")
    print("m linha coluna - marcar/desmarcar bandeira")
    print("q - sair")
    print()

    jogo = CampoMinado()

    while not jogo.game_over and not jogo.vitoria:
        jogo.mostrar_tabuleiro()
        print()
        
        comando = input("Digite seu comando: ").strip().split()
        
        if not comando:
            continue
            
        if comando[0] == 'q':
            break
            
        if len(comando) != 3:
            print("Comando inválido! Use: r linha coluna ou m linha coluna")
            continue
            
        try:
            acao = comando[0]
            linha = int(comando[1])
            coluna = int(comando[2])
            
            if not (0 <= linha < jogo.linhas and 0 <= coluna < jogo.colunas):
                print("Posição inválida!")
                continue
                
            if acao == 'r':
                jogo.revelar(linha, coluna)
            elif acao == 'm':
                jogo.marcar(linha, coluna)
            else:
                print("Comando inválido! Use 'r' para revelar ou 'm' para marcar")
                
        except ValueError:
            print("Digite números válidos para linha e coluna!")

    jogo.mostrar_tabuleiro()
    
    if jogo.vitoria:
        print("\n🎉 PARABÉNS! VOCÊ VENCEU! 🎉")
    elif jogo.game_over:
        print("\n💥 GAME OVER! Você pisou em uma mina! 💥")

if __name__ == "__main__":
    main()