# se definiu uma classe para representar os estados, inclua aqui o código Python correspondente
from __future__ import annotations  # Para poder usar o tipo PacmanEstado nos métodos antes da classe estar definida
from typing import Tuple


class PacmanEstado:
    def __init__(self, pacman=(1, 1), gums=None, cellsVisited=None, points=0, moves=0):
        self.pacman = pacman
        self.points = points
        self.moves = moves

        if gums is None:
            gums = {}

        self.gums = gums

        if cellsVisited is None:
            self.cellsVisited = {pacman: 1}
        else:
            self.cellsVisited = cellsVisited
        """ cellsVisited
            Key: (x,y) of visited cell
            Value: How many times it was visited
        """

    def __lt__(self, other: PacmanEstado) -> bool:
        """Compara a quantidade de pontos de self e other"""
        return isinstance(other, PacmanEstado) and self.points < other.points

    def __eq__(self, other: PacmanEstado) -> bool:
        """Compara se self é igual a other"""
        return isinstance(other, PacmanEstado) \
               and self.pacman == other.pacman \
               and self.points == other.points \
               and tuple(self.gums) == tuple(other.gums) \
               and tuple(self.cellsVisited.items()) == tuple(other.cellsVisited.items())

    def __hash__(self) -> int:
        """"Hash do estado"""
        return hash((self.pacman, self.points, tuple(self.gums), tuple(self.cellsVisited.items())))

    def copy(self) -> PacmanEstado:
        """Efetua uma cópia do estado"""
        return PacmanEstado(self.pacman, self.gums.copy(), self.cellsVisited.copy(), self.points, self.moves)

    def visitCell(self, cell: Tuple[int, int]):
        """Visita a célula e come a pastilha, se existir"""
        self.pacman = cell
        self.moves += 1

        if cell not in self.cellsVisited:
            self.cellsVisited[cell] = 0

        self.cellsVisited[cell] += 1

        if cell in self.gums:
            self.eatGum(cell)

    def eatGum(self, gum: Tuple[int, int]):
        """"Come a pastilha e altera a pontuação"""
        if self.gums[gum] == 'N':
            self.points += 1
        elif self.gums[gum] == 'D':
            self.points += max(0, 5 - self.moves)
        elif self.gums[gum] == 'C':
            self.points += self.moves

        del self.gums[gum]
