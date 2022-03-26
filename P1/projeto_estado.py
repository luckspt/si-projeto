from searchPlus import *


class PacmanPastilhas(Problem):
    def __init__(self, pacman=(1, 1), goal=1, pastilhas={}, obstacles={}, dim=10):
        super().__init__(pacman, goal)
        self.pastilhas = pastilhas
        self.obstacles = obstacles
        self.dim = dim

    def actions(self):
        """Possíveis ações a patir da localização atual."""
        a = self.pacman  # posição atual
        hipoteses = [(a[0], a[1] + 1), (a[0] + 1, a[1]), (a[0], a[1] - 1)]  # Cima, Direita, Baixo, Esquerda
        pass

    def result(self):
        """Resultado obtido após determinada ação."""
        pass

    def goal_test(self):
        """Testar se o objetivo foi alcançado."""
        pass

    def line(self, x, y, dx, dy, length):
        """Uma linha de células de comprimento 'length' começando em (x, y) na direcção (dx, dy)."""
        return {(x + i * dx, y + i * dy) for i in range(length)}

    def quadro(self, x, y, length):
        """Uma moldura quadrada de células de comprimento 'length' começando no topo esquerdo (x, y)."""
        return self.line(x, y, 0, 1, length) | self.line(x + length - 1, y, 0, 1, length) | self.line(x, y, 1, 0,
                                                                                                      length) | self.line(
            x, y + length - 1, 1, 0, length)

    def display(self, state):
        for y in range(0, self.dim):
            for x in range(0, self.dim):
                if (x, y) in self.obstacles:
                    print('=', end=' ')
                elif (x, y) == state:
                    print('@', end=' ')
                else:
                    printed = False
                    for k, v in self.pastilhas.items():
                        if (x, y) in v:
                            print(k, end=' ')
                            printed = True
                            continue
                    if not printed:
                        print('.', end=' ')
            print()
        return ''


# l = line(2,2,1,0,6)
# c = line(2,3,0,1,4)
# fronteira = quadro(0,0,10)
# g = PacmanPastilhas(pacman=(1,1),goal=1,pastilhas={},obstacles=fronteira | l | c,dim=10)


l = PacmanPastilhas().line(2, 2, 1, 0, 6)  # iniciox, inicioy, horizontal, vertical, tamanho
# print(l)
c = PacmanPastilhas().line(2, 3, 0, 1, 4)
# print(c)
d = PacmanPastilhas().line(6, 3, 0, 1, 3)
fronteira = PacmanPastilhas().quadro(0, 0, 10)
# print(fronteira)
p = PacmanPastilhas(pacman=(1, 1), goal=1, pastilhas={'N': {(2, 1), (3, 7)}, 'C': {(7, 3)}, 'D': {(4, 5)}},
                                 obstacles=fronteira | l | c | d, dim=10)
print(p.display(p.initial))