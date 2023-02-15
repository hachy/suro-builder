import pprint
import sys
from collections import deque


sys.setrecursionlimit(10**6)

n = int(input())
S, T = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(n)]
pprint.pprint(board)


row = len(board)
col = len(board)
N = row * col
G = [[] for i in range(N)]


# create graph
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
                if r < 0 or r >= row or c < 0 or c >= col or board[r][c] == 0:
                    continue
                if dist[r][c] != -1:
                    continue
                dist[r][c] = dist[x][y] + 1
                deq.append((r, c))
        val = board[i][j]
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

# pprint.pprint(G)


def bfs(s, G, seen, prev):
    deq = deque()
    seen[s] = True
    deq.append(s)
    while deq:
        v = deq.popleft()
        for v2 in G[v]:
            if seen[v2]:
                continue
            seen[v2] = True
            prev[v2] = v
            deq.append(v2)
    return


seen = [False] * N
prev = [-1] * N
bfs(S, G, seen, prev)

if not seen[T]:
    print("No")
    exit()

now = T
res = []
while now != -1:
    res.append(now)
    now = prev[now]
res.reverse()
print(len(res))
print(*res)
