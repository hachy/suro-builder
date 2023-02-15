import sys
import random

size = 5

args = sys.argv
if len(args) == 2:
    size = int(args[1])

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
for i in range(size):
    print(*board[i])
