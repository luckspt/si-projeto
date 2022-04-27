# código de aplicação dos algoritmos
from csp import *
from typing import Dict

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
        
def futoshiki(n: int = 3, quadrados_preenchidos: Dict[str, int] = None) -> CSP:
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

    maiores = {1:0,2:5,6:3}

    def restricoes(X, a, Y, b):
        for i in maiores:
            if len(dominios[i]) == 1 and len(dominios[maiores[i]]) == 1:
                if maiores[i] >= i:
                    return False
                else:
                    pass

        return diff_lin_col(n, X, a, Y, b)

    return CSP(variaveis, dominios, vizinhos, restricoes)