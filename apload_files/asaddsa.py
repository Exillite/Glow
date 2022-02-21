def dfs(v):
    visited.append(v)

    for i in range(n):
        if graph[v][i] == 1 and i not in visited:
            dfs(i)


n, s = map(int, input().split())
graph = [list(map(int, input().split())) for x in range(n)]

visited = []
dfs(s)

print(len(visited))
