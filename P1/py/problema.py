from estado import PacmanEstado


from searchPlus import *
from typing import Tuple, List

class PacmanPastilhas(Problem):
    def __init__(self, pacman=(1, 1), goal=1, gums={}, obstacles={}, dim=10):
        super().__init__(PacmanEstado(pacman, gums), goal)
        self.dim = dim
        self.obstacles = obstacles
        self.directions = {"N": (0, -1), "W": (-1, 0), "E": (1, 0), "S": (0, 1)}

    def actions(self, state: PacmanEstado) -> List[str]:
        """
        Retorna as ações que podem ser executadas num dado estado.
        """
        def valid(x: int, y: int) -> bool:
            return (x, y) not in self.obstacles\
                    and x >= 0 and y >= 0\
                    and x <= self.dim and y <= self.dim

        x, y = state.pacman 
        return [act for act in self.directions
                if valid(x + self.directions[act][0], y + self.directions[act][1])]

    def result(self, state: PacmanEstado, action: str) -> PacmanEstado:
        """
        Retorna o estado que resulta de executar uma dada ação num 
        dado estado.

        pre: action in self.actions(state)
        """
        x, y = state.pacman
        dx, dy = self.directions[action]

        new_state = state.copy()
        new_state.visitCell((x+dx, y+dy))

        return new_state

    def goal_test(self, state: PacmanEstado) -> bool:
        """
        Retorna se o estado é o objetivo.
        """
        return state.points >= self.goal

    def path_cost(self, c: int, state1: PacmanEstado, action: str, state2: PacmanEstado) -> int:
        """
        Retorna o custo de uma solução que chega ao state2 através
        do state1, assumindo custo acumulado c de state1.

        pre: state2 == self.result(state1, action)
        """
        return c + state2.cellsVisited[state2.pacman]
        
    def exec(self, state: PacmanEstado, actions: List[str]) -> Tuple[PacmanEstado, int]:
        """
        Tuplo com o estado atual do Pacman e o respetivo custo acumulado até esta posição
        """
        custo = 0
        for a in actions:
            seg = self.result(state, a)
            custo = self.path_cost(custo, state, a, seg)
            state = seg
        self.display(state)
        print('Custo:', custo)
        print('Goal?', self.goal_test(state))
        return (state, custo)

    def display(self, state: PacmanEstado):
        """
        Constrói o mapa 2D da representação de um estado
        """
        grid = ''
        for y in range(self.dim + 1):
            for x in range(self.dim + 1):
                if (x, y) in self.obstacles:
                    grid += '= '
                elif (x, y) == state.pacman:
                    grid += '@ '
                elif (x,y) in state.gums:
                    grid += f'{state.gums[(x, y)]} '
                else:
                    grid += '. '
            grid += '\n'

        print(grid, end='')

    def display_trace(self, actions: List[str]):
        """
        Constrói o mapa 2D da representação de um estado mostrando o caminho percorrido
        """
        path = set()
        st = self.initial
        for a in actions[:-1]:
            st = self.result(st,a)
            path.add(st.pacman)
            
        """ print the state please"""
        output=""
        for y in range(self.dim + 1):
            for x in range(self.dim + 1):
                if (x, y) in self.obstacles:
                    output += '= '
                elif (x, y) == self.initial.pacman:
                    output += '@ '
                elif (x, y) in path:
                    output += '+ '
                elif (x,y) in self.initial.gums:
                    output += f'{self.initial.gums[(x, y)]} '
                else:
                    output += '. '
            output += "\n"
        print(output, end='')
