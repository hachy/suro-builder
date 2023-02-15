import sys
import random

size, s, t = 5, 0, 24

args = sys.argv
if len(args) == 2:
    size = int(args[1])
    t = size * size - 1
elif len(args) == 3:
    size = int(args[1])
    s = args[2]
    t = size * size - 1
elif len(args) == 4:
    size = int(args[1])
    s, t = args[2], args[3]


num_max_1 = 6
num_max_2 = 9
if size < num_max_1:
    num_max_1 = size
if size < num_max_2:
    num_max_2 = size

board = [[0] * size for _ in range(size)]
for i in range(size):
    for j in range(size):
        num = random.randrange(0, num_max_1)
        if num == 1:
            num = random.randrange(1, num_max_2)
        board[i][j] = num

print(size)
print(s, t)
for i in range(size):
    print(*board[i])
