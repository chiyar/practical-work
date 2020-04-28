import numpy as np


# Удаляет вершину из графа
def remove_node(graph, node):
    for current in graph[node]:
        graph[current].remove(node)
    graph[node].clear()


# Красит вершину со степенью не меньше sqrt(n) и ее соседей,
# а потом удаляет покрашенные вершины из графа
def color_and_remove(graph, node, color_offset, colors):
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
        remove_node(graph, current)
    return color_offset


# Красит оставшуюся часть графа.
# Степени вершин в ней меньше, чем sqrt(n)
def color_remainder(graph, color_offset, colors):
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
def color_graph(graph):
    node_count = len(graph)
    boundary = np.sqrt(node_count)
    color_offset = 0
    colors = [-1 for i in range(node_count)]

    for node in range(node_count):
        if len(graph[node]) >= boundary:
            color_offset = color_and_remove(graph, node, color_offset, colors)

    color_remainder(graph, color_offset, colors)
    return colors


# Выводит цвет каждой вершины после раскраски
def print_colors(colors):
    used = set()
    for i in range(len(colors)):
        used.add(colors[i])
        print('Node {}'.format(i + 1) + ', Color: {}'.format(colors[i]))

    print('\nTotal colors used: {}'.format(len(used)))


# Считывает строку и извлекает из нее пару чисел
def scan_pair(file):
    first, second = file.readline().split()
    first = int(first)
    second = int(second)
    return first, second


def main():
    input_file = open('input', 'r')
    node_count, edge_count = scan_pair(input_file)

    graph = [[] for i in range(node_count)]
    for i in range(edge_count):
        a, b = scan_pair(input_file)
        a -= 1
        b -= 1

        graph[a].append(b)
        graph[b].append(a)

    colors = color_graph(graph)
    print_colors(colors)


if __name__ == "__main__":
    main()
