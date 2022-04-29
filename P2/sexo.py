# código de aplicação dos algoritmos
from csp import *
from typing import Dict, List
from math import sqrt

# Implemente uma função que permita visualizar o puzzle Futoshiki, antes e depois de resolvido. Compare com a solução obtida pelo seu algoritmo.
# No caso de não implementar esta função, inclua um screenshot do problema e da sua solução.
# Implemente uma função que permita visualizar o quadrado latino, antes e depois de resolvido.
from typing import Dict
from math import sqrt

def visualize_futoshiki(vs: Dict[str, int], maiores: Dict[str, str]):
    def get_x_y(n: int, var: int):
        return var % n, var // n

    n = int(sqrt(len(vs)))
    to_list = sorted(vs.items(), key=lambda x: int(x[0]))

    to_write = [[''] * n for _ in range((n*2) - 1)]
    for i, (var, v) in enumerate(to_list):
        var_int = int(var)
        x, y = get_x_y(n, var_int)

        char_to_write = str(v)

        maiores_que = maiores.get(var, None)
        if maiores_que is not None:
            for maior in maiores_que:
                xM, yM = get_x_y(n, int(maior))

                if y == yM:
                    # Sinal horizontal
                    if xM > x:
                        char_to_write += ' >'
                    elif xM < x:
                        char_to_write = f'< {char_to_write}'
                elif yM > y:
                    # Sinal vertical
                    to_write[y * 2 + 1][x] = 'v'
                else:
                    to_write[y * 2 - 1][x] = '^'


        to_write[y * 2][x] = char_to_write

    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in to_write]))

def diff_lin_col(n: int, X: str, a: int, Y: str, b: int):  # X Y -> Vars ; a b-> Doms #
    # Ver se X e Y estão na mesma linha
    X = int(X)
    Y = int(Y)

    linhaX = X//n
    linhaY = Y//n
    # Ver se X e Y estão na mesma coluna
    colunaX = X % n
    colunaY = Y % n

    if linhaX == linhaY or colunaX == colunaY:
        return a != b
    else:
        return True

def maior(x: int, y: int) -> bool:
    return x > y

def menor(x: int, y: int) -> bool:
    return x < y
        
def futoshiki(n: int = 3, quadrados_preenchidos: Dict[str, int] = None, maiores: Dict[str, List[str]] = None) -> CSP:
    """
    Pode receber parametros ou não.
    Deve devolver um CSP, à semelhança dos guiões das aulas PL.
    Comente o código.
    """
    # 0 1 2 .
    # 3 4 5 .
    # 6 7 8 .
    # . . .
    # As variáveis são os índices do quadrado latino.
    variaveis = [str(x) for x in range(n*n)]  # [0,...,8] Indices

    # O domínio são os valores [1, ..., n] para cada variável.
    dom = [x for x in range(1, n+1)]  # [1,...,9] Valores

    dominios = {}
    for v in variaveis:
        dominios[v] = dom  # A colocar na lista os valores
        # TODO copiar lista?
    if quadrados_preenchidos:
        for (k, v) in quadrados_preenchidos.items():
            dominios[k] = [v]  # {Indice: val,Indice: val}
            # ex: {4: [3]} -> dominios[4] = [3]

    # Os vizinhos são os índices da mesma linha e da mesma coluna que a variável
    vizinhos = {v: [] for v in variaveis}  # {1: [], ..., 9: []}

    # Para cada coluna
    for col in range(n):
        # Para cada linha
        for lin in range(col, n*n, n):
            # Linhas
            vizinhos[str(lin)].extend([lin+x for x in range(1, n-col)])
            # Colunas
            vizinhos[str(lin)].extend([x for x in range(lin+n, n*n, n)])

    # Traduzir de dicionário para o formato do parse_neighbors
    vizinhos = '; '.join(
        map(lambda k: f'{k}: {" ".join(map(str, vizinhos[k]))}', vizinhos))
    vizinhos = parse_neighbors(vizinhos)

    def restricoes(X, a, Y, b):
        maior = None
        menor = None
        #print(list(maiores.keys()))
        #print(list(maiores.values()))
       # print(X in list(maiores.keys()))
       # print(type(X))

        if X in list(maiores.keys()):
            print("a")
            if Y in maiores[X]:
                print("b")
                maior = int(a)
                menor = int(b)
        if Y in list(maiores.keys()):
            if X in maiores[Y]:
                maior = int(b)
                menor = int(a)
        if maior != None and menor != None and maior<=menor:
            return False

        return diff_lin_col(n, str(X), str(a), str(Y), str(b))

    return CSP(variaveis, dominios, vizinhos, restricoes)

n = 4
maiores = {'1': ['0'], '13':['9'], '7':['3']}

p = futoshiki(n, maiores=maiores)
r = backtracking_search(p)
print(r)
visualize_futoshiki(r, maiores=maiores)
