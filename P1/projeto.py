from typing import Tuple

from searchPlus import *
import time as t, timeit


class PacmanEstado:
    def __init__(self, pacman=(1, 1), pastilhas=None, cellsVisited=None, points=0):

        self.pacman    = pacman
        self.pastilhas = pastilhas
        self.points    = points

        if pastilhas is None:
            pastilhas = {}

        if cellsVisited is None:
            self.cellsVisited = {pacman: 1}
        else:
            self.cellsVisited = cellsVisited
        """ cellsVisited
            Key: (x,y) of visited cell
            Value: How many times it was visited
        """

    def __lt__(self, other) -> bool:
        raise Exception('EXCEÇÃO LT')

    def visitCell(self, cell, start):
        if cell not in self.cellsVisited:
            self.cellsVisited[cell] = 0        

        self.cellsVisited[cell] += 1

        if cell in self.pastilhas:
            self.eatGum(cell, start)

    def eatGum(self, gum, start):
        if self.pastilhas[gum] == 'N':
            self.points += 1
        elif self.pastilhas[gum] == 'D':
            self.points += max(0, 5-(t.time()-start))
        elif self.pastilhas[gum] == 'C':
            self.points += t.time()-start

        del self.pastilhas[gum]

class PacmanPastilhas(Problem):
    def __init__(self, pacman=(1, 1), goal=1, pastilhas={}, obstacles={}, dim=10):
        super().__init__(PacmanEstado(pacman, pastilhas), goal)
        self.dim = dim
        self.obstacles = obstacles
        self.timeStart = t.time()
        self.directions = {"N":(0, -1), "W":(-1, 0), "E":(1,  0),"S":(0, +1)}  

    def actions(self, state: PacmanEstado):
        """
        Return the actions that can be executed in the given
        state.
        """
        x, y = state.pacman
        return [act for act in self.directions.keys()
                if (x + self.directions[act][0], y + self.directions[act][1]) not in self.obstacles]

    def result(self, state: PacmanEstado, action):
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        """
        x, y = state.pacman
        dx, dy = self.directions[action]

        e = PacmanEstado((x+dx, y+dy), state.pastilhas, state.cellsVisited, state.points)
        e.visitCell(e.pacman, self.timeStart)
        return e

    def goal_test(self, state: PacmanEstado):
        """
        Return True if the state is a goal.
        """
        return state.points >= self.goal

    def path_cost(self, c: int, state1: PacmanEstado, action, state2: PacmanEstado):
        """
        Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1.
        """
        # c -> custo até de todo o caminho até state1
        # state1 -> estado antgo
        # state2 -> estado novo #SALAZAR 17499 dias
        # action -> ação de state1 para state2

        #state2 = self.result(state1,action)

        # ir ao dicionario ver qt custa state2 e
        # soma ao custo que está associado a state1 
        
        return c + state2.cellsVisited[state2.pacman]

    def exec(self, state, actions) -> Tuple[PacmanEstado, int]:
        """Um tuplo com o estado atual do Pacman e o restivo custo acumulado"""
        custo = 0
        for a in actions:
            seg = self.result(state, a)
            custo = self.path_cost(custo, state, a, seg)
            state = seg
        self.display(state)
        print('Custo:', custo)
        print('Goal?', self.goal_test(state))
        return (state, custo)

    # _________________________________________MAPA____________________________________________________
    def line(self, x, y, dx, dy, length):
        """Uma linha de células de comprimento 'length' começando em (x, y) na direcção (dx, dy)."""
        return {(x + i * dx, y + i * dy) for i in range(length)}

    def quadro(self, x, y, length):
        """Uma moldura quadrada de células de comprimento 'length' começando no topo esquerdo (x, y)."""
        return self.line(x, y, 0, 1, length) | self.line(x + length - 1, y, 0, 1, length) | self.line(x, y, 1, 0,
                                                                                                      length) | self.line(
            x, y + length - 1, 1, 0, length)

    def display(self, state: PacmanEstado):
        """Representação gráfica através de caracteres de determinado estado do Pacman"""
        grid = ''
        for y in range(0, self.dim):
            for x in range(0, self.dim):
                if (x, y) in self.obstacles:
                    grid += '= '
                elif (x, y) == state.pacman:
                    grid += '@ '
                elif (x,y) in state.pastilhas:
                    grid += f'{state.pastilhas[(x, y)]} '
                else:
                    grid += '. '
            grid += '\n'

        print(grid)

l = PacmanPastilhas().line(2, 2, 1, 0, 6)  # iniciox, inicioy, horizontal, vertical, tamanho
# print(l)
c = PacmanPastilhas().line(2, 3, 0, 1, 4)
# print(c)
d = PacmanPastilhas().line(6, 3, 0, 1, 3)
fronteira = PacmanPastilhas().quadro(0, 0, 10)
# print(fronteira)
p = PacmanPastilhas(pacman=(1, 1),
                                 goal=1,
                                 pastilhas={(2,1): 'N', (5, 8): 'N', (7, 3): 'C', (4,5): 'D'},
                                 obstacles=fronteira | l | c | d,
                                 dim=10)

from random import randint
e = p.initial
p.display(e)
print(f'Points: {e.points}\n')

custo = 0
for i in range(5):
    actions = p.actions(e)
    e = p.result(e, actions[randint(0, len(actions)-1)])
    custo = p.path_cost(custo, None, None, e)
    p.display(e)
    print(f'Points: {e.points}')
    print(f'Custo: {custo}')
    print(f'Pastilhas: {e.pastilhas}')
    print(f'CellsVisited: {e.cellsVisited}\n')
    print(f'E final? {p.goal_test(e)}')


# start = timeit.default_timer()
# stop = timeit.default_timer() 