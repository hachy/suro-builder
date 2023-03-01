import pprint
import sys
from collections import deque
import itertools
import copy


sys.setrecursionlimit(10**6)

n = int(input())
board = [list(map(int, input().split())) for _ in range(n)]

row = len(board)
col = len(board)
N = row * col


def show_grid_idx(r, c):
    print("-- grid index --")
    grid = [[0] * c for _ in range(r)]
    for i in range(r):
        for j in range(c):
            grid[i][j] = i * c + j
    pprint.pprint(grid)
    print("--------------------")


def create_graph(bd):
    G = [[] for i in range(N)]
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    for i in range(row):
        for j in range(col):
            idx = i * col + j
            dist = [[-1] * col for _ in range(row)]
            deq = deque()
            dist[i][j] = 0
            deq.append((i, j))
            while deq:
                x, y = deq.popleft()
                for k in range(4):
                    r = dx[k] + x
                    c = dy[k] + y
                    if r < 0 or r >= row or c < 0 or c >= col or bd[r][c] == 0:
                        continue
                    if dist[r][c] != -1:
                        continue
                    dist[r][c] = dist[x][y] + 1
                    deq.append((r, c))
            val = bd[i][j]
            for i2 in range(row):
                for j2 in range(col):
                    idx2 = i2 * col + j2
                    d = dist[i2][j2]
                    if idx == idx2:
                        continue
                    if d == -1:
                        continue
                    if d == val or d == val - 2:
                        G[idx].append(idx2)
    return G


def bfs(s, graph, seen, prev):
    deq = deque()
    seen[s] = True
    deq.append(s)
    while deq:
        v = deq.popleft()
        for v2 in graph[v]:
            if seen[v2]:
                continue
            seen[v2] = True
            prev[v2] = v
            deq.append(v2)
    return


def solve(s, tlist, graph):
    psize = len(tlist)
    perms = itertools.permutations(tlist, psize)
    for perm in perms:
        start = s
        tmp_graph = graph
        tmp_bd = copy.deepcopy(board)
        for v in perm:
            seen = [False] * N
            prev = [-1] * N
            bfs(start, tmp_graph, seen, prev)

            if not seen[v]:
                print("No")
                break

            now = v
            res = []
            while now != -1:
                res.append(now)
                now = prev[now]
            res.reverse()
            cost = len(res)
            print("cost:", cost)
            print(*res)

            # update graph
            start = v
            for i in range(cost):
                if i == cost - 1:
                    continue
                tr = res[i] // row
                tc = res[i] % col
                tmp_bd[tr][tc] = 0
            tmp_graph = create_graph(tmp_bd)
        print("--------------------")


show_grid_idx(row, col)

S, T = 0, [24]
g = create_graph(board)
pprint.pprint(board)
print("--------------------")
print("S:", S, "T:", T)
print("--------------------")
solve(S, T, g)
