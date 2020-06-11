from collections import deque

N = 10
M = 10

graph = {i: set() for i in range(N)}
for i in range(M):
    for v1, v2 in enumerate(range(1, M)):
        graph[v1].add(v2)
        graph[v2].add(v1)

distances = [None] * N  # array of distances is unknown
start_vertex = 0  # start from root
distances[start_vertex] = 0  # self distance is 0
queue = deque([start_vertex])  # make queue that will be like [0] after E-x: 2 heights number (1,3) queue would be []
# and after step (firing this 2 heights (1,3) queue will contain [1,3]

while queue:
    cur_v = queue.popleft()  #  first element of
    for height_v in graph[cur_v]:  #check all neighbors
        if distances[height_v] is None:  # if we did not check this neighbor distance is None
            distances[height_v] = distances[cur_v] + 1  # calculate distance
            queue.append(height_v)  # add to queue for check its neighbors
print(distances)

