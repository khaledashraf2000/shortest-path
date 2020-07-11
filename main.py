from collections import deque


# converts from (row, col) to square position
def pos(row, col, n):
    return (row - 1) * n + col


# initial and final positions
inp = list(map(int, input("").split()))
r = [inp[0], inp[2]]
c = [inp[1], inp[3]]

# initialize min row and col, max row and col
min_row = r[0] if r[0] < r[1] else r[1]
max_row = r[1] if min_row == r[0] else r[0]
min_col = c[0] if c[0] < c[1] else c[1]
max_col = c[1] if min_col == c[0] else c[0]

# scanning n and allowed ranges
n = int(input(""))
allowed = []
for i in range(n):
    data = list(map(int, input("").split()))
    allowed.append([data.copy()[0], data.copy()[1], data.copy()[2]])

    # updating min_row and max_row
    if allowed[i][0] < min_row:
        min_row = allowed[i][0]
    if allowed[i][0] > max_row:
        max_row = allowed[i][0]
    # updating min_col and max_col
    if allowed[i][1] < min_col:
        min_col = allowed[i][1]
    if allowed[i][2] > max_col:
        max_col = allowed[i][2]

# shift to start from 1
ROW_SHIFT = min_row - 1
COL_SHIFT = min_col - 1

ROW = max_row - ROW_SHIFT
COL = max_col - COL_SHIFT
N = COL
START = pos(r[0] - ROW_SHIFT, c[0] - COL_SHIFT, N)
END = pos(r[1] - ROW_SHIFT, c[1] - COL_SHIFT, N)

# my approach was to connect all available squares to themselves to use them
# as a reference for surrounding squares so they connect to them as well,
# then remove self-loops after filling in the matrix

# initialize adjacency matrix
adj_m = [[0 for _ in range(ROW * COL + 1)] for _ in range(ROW * COL + 1)]

# connecting START and END to themselves because any surrounding square is able
# to connect to them
adj_m[START][START] = 1
adj_m[END][END] = 1

# convert allowed from row, col to pos
# i used the same allowed list to save space, now first element in each range
# is the starting square and second element is the ending square, third element
# is negligible.
for i in range(n):
    row = allowed[i][0]
    allowed[i][0] = pos(row - ROW_SHIFT, allowed[i][1] - COL_SHIFT, N)
    allowed[i][1] = pos(row - ROW_SHIFT, allowed[i][2] - COL_SHIFT, N)

# fill in adjacency matrix with ranges of allowed moves
for i in range(n):
    for j in range(allowed[i][0], allowed[i][1] + 1):
        # connect square to itself
        adj_m[j][j] = 1

        L = j - 1
        U = j - N
        UR = j - (N - 1)
        UL = j - (N + 1)

        '''
         UL | U | UR
        --------------
        j-1 | j | j+1
        --------------
         DL | D | DR
        '''

        # connect any allowed square (including start and final position) around it to itself
        # only look at squares in upper row and left columns
        # because of iteration nature

        # connect to left
        if j % COL != 1:  # not on left column
            if adj_m[L][L] == 1:
                adj_m[L][j] = 1
                adj_m[j][L] = 1

        # not the top row
        if j > COL:
            # connect to upper square
            if adj_m[U][U] == 1:
                adj_m[U][j] = 1
                adj_m[j][U] = 1

            # not on right column
            if j % COL != 0:
                # connect to upper right square
                if adj_m[UR][UR] == 1:
                    adj_m[UR][j] = 1
                    adj_m[j][UR] = 1

            # not on left column
            if j % COL != 1:
                # connect upper left square
                if adj_m[UL][UL] == 1:
                    adj_m[UL][j] = 1
                    adj_m[j][UL] = 1

# remove self loops
for i in range(ROW * COL + 1):
    adj_m[i][i] = 0
'''
for i in range(1, ROW * COL + 1):
    for j in range(1, ROW * COL + 1):
        print(f"{adj_m[i][j]} ", end='')
    print(" ")
'''

# bfs
q = deque()
visited = [False for _ in range(1, ROW * COL + 2)]
dist = [float('inf') for _ in range(1, ROW * COL + 2)]
pred = [-1 for _ in range(1, ROW * COL + 2)]
connected = False

q.append(START)
visited[START] = True
dist[START] = 0

# while queue isn't empty
while q:
    curr = q.popleft()
    for sq in range(1, ROW * COL + 1):
        if adj_m[curr][sq] == 1 and not visited[sq]:
            q.append(sq)
            visited[sq] = True
            dist[sq] = dist[curr] + 1
            pred[sq] = curr

            if sq == END:
                connected = True
                break

if connected:
    print(dist[END])
else:
    print('-1')
