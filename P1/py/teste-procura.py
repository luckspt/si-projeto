from problema import PacmanPastilhas
def line(x, y, dx, dy, length):
    """Uma linha de células de comprimento 'length' começando em (x, y) na direcção (dx, dy)."""
    return {(x + i * dx, y + i * dy) for i in range(length)}

def quadro(x, y, length):
    """Uma moldura quadrada de células de comprimento 'length' começando no topo esquerdo (x, y)."""
    length += 1 # fix para as coordenadas serem de (0, 0) a (dim, dim)
    return line(x, y, 0, 1, length)\
        | line(x + length - 1, y, 0, 1, length)\
        | line(x, y, 1, 0, length)\
        | line(x, y + length - 1, 1, 0, length)
l = line(2, 2, 1, 0, 6)
c = line(2, 3, 0, 1, 4)
d = line(6, 3, 0, 1, 3)
fronteira = quadro(0, 0, 10)


# código de aplicação dos algoritmos
from searchPlus import *
from timeit import default_timer
from typing import Callable

# Problema -------------------------------------
prob = PacmanPastilhas(
    pacman=(1, 1),
    goal=2,
    gums={(2,1): 'N', (5,8): 'N', (4,3): 'C', (4,5): 'D'},
    obstacles=fronteira | l | c | d,
    dim=10)


est = prob.initial
print('Estado inicial:')
prob.display(est)
print('\n')
# ----------------------------------------------

# Função de teste
def testa(prob: PacmanPastilhas, algo: Callable):
    start = default_timer()

    res = algo(prob)
    if not res:
        print('Sem resultado')
    else:
        sol = res.solution()
        prob.display_trace(sol)
        print(f'Custo: {res.path_cost}')
        print(f'Ações ({len(sol)}): {"-".join(sol)}')

    stop = default_timer()
    print(f'Time: {stop-start}s\n')
# ----------------------------------------------

# Algoritmos de procura
#   Custo Uniforme em Árvore
def best_first_tree_search(problem, f):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = PriorityQueue(min, f)
    frontier.append(node)
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        for child in node.expand(problem):
            frontier.append(child)
    return None

def uniform_cost_tree_search(problem):
    return best_first_tree_search(problem, lambda node: node.path_cost)
#    -------

#    Largura em Grafo
def breadth_first_graph_search(problem):
    """Search the deepest nodes in the search tree first."""
    return graph_search(problem, FIFOQueue())
#    -------

#   Profundidade Iterativa em Grafo
def graph_limited_search(problem, frontier,lim):
    frontier.append(Node(problem.initial))
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        if node.depth < lim:
            frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and
                        child not in frontier)
    return 'cutoff'

def depth_limited_graph_search(problem, depth):
    return graph_limited_search(problem,Stack(),depth)

def iterative_deepening_plus_graph_search(problem):
    for depth in range(sys.maxsize):
        result = depth_limited_graph_search(problem, depth)
        if result != 'cutoff':
            return result
#    -------
# ----------------------------------------------

# Testes
print('BFS Árvore:')
# testa(prob, breadth_first_tree_search)
"""
= = = = = = = = = = = 
= @ + . . . . . . . = 
= + = = = = = = . . = 
= + = . C . = . . . = 
= + = . . . = . . . = 
= + = . D . = . . . = 
= + = . . . . . . . = 
= + + + + + . . . . = 
= . . . . N . . . . = 
= . . . . . . . . . = 
= = = = = = = = = = = 
Custo: 14
Ações (13): E-W-S-S-S-S-S-S-E-E-E-E-S
Time: 0.17257197700382676s

Este é o primeiro caminho a ser encontrado (árvore de nível 13) e tem um custo de 14.
Poderia-se ter usado um caminho mais ótimo (S-S-S-S-S-S-E-E-N-N-N-N-E) que tem o mesmo nível de árvore, 
mas o BFS não leva em consideração os custos das ações, e como a prioridade das ações é Norte, Oeste, Este, Sul, esta 
solução foi descoberta antes da ótima.
"""

print('DFS Árvore:')
print('entra em ciclo infinito...\n')
# testa(prob, depth_first_tree_search)
"""
No DFS em árvore iremos entrar em ciclo infinito porque o dicionário de células visitadas é copiado e incrementado 
na nova célula, portanto, como o dicionário mudou, o estado também será diferente.
"""

print('DFS Progressivo Árvore:')
# testa(prob, iterative_deepening_search)
"""
= = = = = = = = = = = 
= @ + . . . . . . . = 
= + = = = = = = . . = 
= + = . C . = . . . = 
= + = . . . = . . . = 
= + = . D . = . . . = 
= + = . . . . . . . = 
= + + + + + . . . . = 
= . . . . N . . . . = 
= . . . . . . . . . = 
= = = = = = = = = = = 
Custo: 14
Ações (13): E-W-S-S-S-S-S-S-E-E-E-E-S
Time: 0.07676839100167854s


O DFS Progressivo em árvore encontra uma solução apesar de não ser garantidamente ótima.
Procura assim a solução mais próxima da raiz, obtendo a menor quantidade de ações possível.

Tem a mesma solução que o BFS em árvore porque a primeira solução encontra-se ao nível 13, e nesse último nível, 
comporta-se como uma procura em largura.
"""

print('Custo Uniforme Árvore:')
# testa(prob, uniform_cost_tree_search)
"""
= = = = = = = = = = = 
= @ N . . . . . . . = 
= + = = = = = = . . = 
= + = + C . = . . . = 
= + = + . . = . . . = 
= + = + D . = . . . = 
= + = + . . . . . . = 
= + + + . . . . . . = 
= . . . . N . . . . = 
= . . . . . . . . . = 
= = = = = = = = = = = 
Custo: 13
Ações (13): S-S-S-S-S-S-E-E-N-N-N-N-E
Time: 0.047016159995109774s

No custo uniforme em árvore há optimalidade da solução. Neste, são primeiramente expandidos os nós com menor custo, evitando assim
caminhos já percorridos, como podemos observar ao compararmos com os algoritmos anteriores, em que o primeiro passo foi sempre comer
 a pastilha na posição (1,2), voltado em seguida para trás, é mais custoso (14) que comer a pastilha de crescimento (13).
"""

# Grafos
"""
Nas procuras em grafo não se visita estados já visitados (exceto o custo uniforme quando o custo será inferior).
Contudo, um estado deste problema inclui quantas vezes uma célula foi visitada.
Sempre que o pacman muda de posição é criado um novo estado, e quantidade de vezes que a célula foi visitada é incrementada

Portanto, como o dicionário é diferente, haverá uma maior quantidade de estados, ao invés de apenas considerar a posição do pacman no estado.

É importante referir também que para a pesquisa em grafo os estados visitados são guardados num set, e é necessário calcular a hash de cada.
Para esta última parte do cálculo, é necessário processar o dicionário de células visitadas (entre outras coisas), que se torna custoso 
em computação.

Para "simularmos" uma pesquisa em grafo neste problema, embora fosse uma representação incorreta do estado, não deveriamos considerar 
este dicionário.

Como referência, os tempos de execução das pesquisas com o dicionário são, omitindo os casos em que o tempo é idêntico:
BFS Grafo:
Custo: 14
Ações (13): E-W-S-S-S-S-S-S-E-E-E-E-S
Time: 19.181869682004617s

DFS Progressivo Grafo:
Custo: 13
Ações (13): S-S-S-S-S-S-E-E-E-N-N-N-N
Time: 0.14453338000021176s

Custo Uniforme Grafo:
Custo: 13
Ações (13): S-S-S-S-S-S-E-E-N-N-N-N-E
Time: 2.771507126002689s

E sem o dicionário:

BFS Grafo:
Custo: 14
Ações (13): E-W-S-S-S-S-S-S-E-E-E-E-S
Time: 0.0016931040008785203s

DFS Progressivo Grafo:
Custo: 14
Ações (13): E-W-S-S-S-S-S-S-E-E-E-S-E
Time: 0.003614033994381316s

Custo Uniforme Grafo:
Custo: 13
Ações (13): S-S-S-S-S-S-E-E-N-N-N-N-E
Time: 0.004510387996560894s
"""

print('BFS Grafo:')
# testa(prob, breadth_first_graph_search)
"""
= = = = = = = = = = = 
= @ + . . . . . . . = 
= + = = = = = = . . = 
= + = . C . = . . . = 
= + = . . . = . . . = 
= + = . D . = . . . = 
= + = . . . . . . . = 
= + + + + + . . . . = 
= . . . . N . . . . = 
= . . . . . . . . . = 
= = = = = = = = = = = 
Custo: 14
Ações (13): E-W-S-S-S-S-S-S-E-E-E-E-S
Time: 21.853373776997614s

O funcionamento deste algoritmo de pesquisa é idêntico ao BFS em árvore, com a única diferença de não visitar estados já visitados.
Pelas razões supramencionadas, usando a representação correta do estado, este algoritmo é mais lento que a sua vertente em árvore.
"""

print('DFS Grafo:')
print('entra em ciclo infinito...\n')
# testa(prob, depth_first_graph_search)
"""
Esta pesquisa resulta também num ciclo infinito.
"""

print('DFS Progressivo Grafo:')
testa(prob, iterative_deepening_plus_graph_search)
"""
= = = = = = = = = = = 
= @ N . . . . . . . = 
= + = = = = = = . . = 
= + = . C . = . . . = 
= + = . + . = . . . = 
= + = . + . = . . . = 
= + = . + . . . . . = 
= + + + + . . . . . = 
= . . . . N . . . . = 
= . . . . . . . . . = 
= = = = = = = = = = = 
Custo: 13
Ações (13): S-S-S-S-S-S-E-E-E-N-N-N-N
Time: 0.18235782199917594s

Come a pastilha de Desgaste e perde max(0, 5-11) pontos, ficando com 0 pontos. Qdo come a Crescimento ganha 13
porque é que não fez os dois N, e pqq comeu a pastilha D? sus
"""

print('Custo Uniforme Grafo:')
testa(prob, uniform_cost_search)
"""
= = = = = = = = = = = 
= @ N . . . . . . . = 
= + = = = = = = . . = 
= + = + C . = . . . = 
= + = + . . = . . . = 
= + = + D . = . . . = 
= + = + . . . . . . = 
= + + + . . . . . . = 
= . . . . N . . . . = 
= . . . . . . . . . = 
= = = = = = = = = = = 
Custo: 13
Ações (13): S-S-S-S-S-S-E-E-N-N-N-N-E
Time: 4.242591356000048s

O funcionamento deste algoritmo de pesquisa é idêntico ao Custo Uniforme em árvore, com a única diferença de não visitar estados já 
visitados que tenham um custo inferior.
Pelas razões supramencionadas, usando a representação correta do estado, este algoritmo é mais lento que a sua vertente em árvore.
"""