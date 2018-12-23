import pytest
import scipy.stats as sps
from main import color_graph
import sys


# Проверяет, правильным ли образом покрашены вершины
def coloring_is_valid(graph, colors):
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if colors[i] == colors[graph[i][j]]:
                return False
    return True


# Генерирует случайный граф с заданной вероятностью появления ребра
# и с заданным количеством вершин
def generate_random_graph(vertices_count, probability = 0.5):
    graph = [[] for i in range(vertices_count)]
    for i in range(vertices_count):
        for j in range(i):
            flag = sps.bernoulli.rvs(probability)
            if flag:
                graph[i].append(j)
                graph[j].append(i)
    return graph


# Генерирует все графы с заданным количеством вершин
def generate_all_graphs_with_fixed_vertices_count(vertices_count):
    graphs = []
    max_edges_count = (vertices_count - 1) * vertices_count // 2
    for bit_mask in range(1, 2 ** max_edges_count):
        graph = [[] for i in range(vertices_count)]

        current_edge = [0, 1]
        for i in range(max_edges_count):
            if (2 ** i) & bit_mask != 0:
                graph[current_edge[0]].append(current_edge[1])
                graph[current_edge[1]].append(current_edge[0])

            current_edge[1] += 1
            if current_edge[1] == vertices_count:
                current_edge[0] += 1
                current_edge[1] = current_edge[0] + 1

        graphs.append(graph)

    return graphs


class Test3Coloring:

    @pytest.mark.parametrize("probability", [0., 0.01, 0.1, 0.5, 0.75, 0.95, 1.])
    def test_random_graph_coloring(self, probability):
        for vertices_count in range(100, 110):
            graph = generate_random_graph(vertices_count, probability)
            colors = color_graph(graph)
            assert(coloring_is_valid(graph, colors))

    def test_all_graphs_coloring(self):
        for vertices_count in range(1, 7):
            graphs = generate_all_graphs_with_fixed_vertices_count(vertices_count)
            for graph in graphs:
                colors = color_graph(graph)
                assert (coloring_is_valid(graph, colors))

