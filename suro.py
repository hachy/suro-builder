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


class SmallBoard:
    def __init__(self, origin_bd, i, j, d, start, target):
        self.start = start
        self.target = target
        b_i = 0 if i - d <= 0 else i - d
        b_j = 0 if j - d <= 0 else j - d
        e_i = row - 1 if i + d >= row else i + d
        e_j = col - 1 if j + d >= col else j + d
        self.bd, self.s_i, self.s_j, self.t_i, self.t_j = self.small_board(
            b_i, b_j, e_i, e_j, origin_bd
        )
        self.h, self.w = e_i - b_i + 1, e_j - b_j + 1

    def small_board(self, b_i, b_j, e_i, e_j, origin_bd):
        s_bd = []
        s_i, s_j, t_i, t_j = 0, 0, 0, 0
        for i in range(row):
            if i >= b_i and i <= e_i:
                s_bd.append([])
            for j in range(col):
                if i >= b_i and i <= e_i and j >= b_j and j <= e_j:
                    s_bd[i - b_i].append(origin_bd[i][j])
                s_idx = i * col + j
                if s_idx == self.start:
                    s_i, s_j = i - b_i, j - b_j
                if s_idx == self.target:
                    t_i, t_j = i - b_i, j - b_j
        return s_bd, s_i, s_j, t_i, t_j


def dfs(s_bd, i, j, t_i, t_j, h, w, visited, depth, val):
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    visited[i][j] = (True, depth)
    for k in range(4):
        r = dx[k] + i
        c = dy[k] + j
        if r < 0 or r >= h or c < 0 or c >= w or s_bd[r][c] == 0:
            continue
        if visited[r][c][0]:
            continue
        if r == t_i and c == t_j and visited[i][j][1] + 1 != val:
            continue
        dfs(s_bd, r, c, t_i, t_j, h, w, visited, depth + 1, val)


def maze(s, val):
    visited = [[(False, 0)] * s.w for _ in range(s.h)]
    dfs(s.bd, s.s_i, s.s_j, s.t_i, s.t_j, s.h, s.w, visited, 0, val)
    goal = visited[s.t_i][s.t_j]
    res = False
    if goal[0] and goal[1] == val:
        res = True
    return res


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
            if val == 0:
                continue
            for i2 in range(row):
                for j2 in range(col):
                    idx2 = i2 * col + j2
                    d = dist[i2][j2]
                    if idx == idx2:
                        continue
                    if d == -1:
                        continue
                    if d == val:
                        G[idx].append(idx2)
                    if d == val - 2:
                        sbd = SmallBoard(bd, i, j, d, idx, idx2)
                        if maze(sbd, val):
                            G[idx].append(idx2)
    return G


def bfs(s, graph, tmp_bd, seen, prev):
    t_bd = copy.deepcopy(tmp_bd)
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

        # update graph
        tmp_bd[v // row][v % col] = 0
        graph = create_graph(tmp_bd)
        # reset
        tmp_bd = t_bd
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
            bfs(start, tmp_graph, tmp_bd, seen, prev)

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
            print("cost:", cost - 1)
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
