import numpy as np


# Удаляет вершину из графа
def RemoveNode(graph, node):
    for current in graph[node]:
        graph[current].remove(node)
    graph[node].clear()


# Красит вершину со степенью не меньше sqrt(n) и ее соседей,
# а потом удаляет покрашенные вершины из графа
def ColorAndRemove(graph, node, color_offset, colors):
    colors[node] = color_offset
    color_offset += 1

    for current in graph[node]:
        is_allowed = True

        for neighbour in graph[current]:
            if neighbour == current:
                continue

            if colors[neighbour] == color_offset:
                is_allowed = False
                break

        if is_allowed:
            colors[current] = color_offset
        else:
            colors[current] = color_offset + 1

    color_offset += 2

    neighbours = graph[node].copy()
    for current in neighbours:
        RemoveNode(graph, current)
    return color_offset


# Красит оставшуюся часть графа.
# Степени вершин в ней меньше, чем sqrt(n)
def ColorRemainder(graph, color_offset, colors):
    for current in range(len(graph)):
        if colors[current] == -1:
            used = set()
            for neighbour in graph[current]:
                used.add(colors[neighbour])

            color = color_offset
            while color in used:
                color += 1

            colors[current] = color


# Красит граф в O(sqrt(n)) цветов
def ColorGraph(graph):
    node_count = len(graph)
    boundary = np.sqrt(node_count)
    color_offset = 0
    colors = [-1 for i in range(node_count)]

    for node in range(node_count):
        if len(graph[node]) >= boundary:
            color_offset = ColorAndRemove(graph, node, color_offset, colors)

    ColorRemainder(graph, color_offset, colors)
    return colors


# Выводит цвет каждой вершины после раскраски
def PrintColors(colors):
    used = set()
    for i in range(len(colors)):
        used.add(colors[i])
        print('Node {}'.format(i + 1) + ', Color: {}'.format(colors[i]))

    print('\nTotal colors used: {}'.format(len(used)))


# Считывает строку и извлекает из нее пару чисел
def ScanPair(file):
    first, second = file.readline().split()
    first = int(first)
    second = int(second)
    return first, second


def main():
    input_file = open('input', 'r')
    node_count, edge_count = ScanPair(input_file)

    graph = [[] for i in range(node_count)]
    for i in range(edge_count):
        a, b = ScanPair(input_file)
        a -= 1
        b -= 1

        graph[a].append(b)
        graph[b].append(a)

    colors = ColorGraph(graph)
    PrintColors(colors)


main()
