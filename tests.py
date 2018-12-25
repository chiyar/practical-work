import pytest
import scipy.stats as sps
from main import color_graph
import numpy as np


# Проверяет, правильным ли образом покрашен граф,
# и не превосходит ли число использованных цветов 4*sqrt(n),
# как было заявлено в алгоритме
def coloring_is_valid(graph, colors):
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if colors[i] == colors[graph[i][j]]:
                return False

    used = set()
    for i in range(len(graph)):
        used.add(colors[i])

    print('Colors used: ', len(used), "Count of vertices: ", len(graph))
    return len(used) <= 4 * np.sqrt(len(graph))


# Генерирует случайный граф с заданной вероятностью
# появления ребра и с заданными размерами трех компонент
def generate_random_graph(components_sizes, probability):
    graph = [[] for i in range(np.sum(components_sizes))]
    for i in range(components_sizes[0]):
        for j in range(components_sizes[1]):
            first = i
            second = j + components_sizes[0]
            if sps.bernoulli.rvs(probability):
                graph[first].append(second)
                graph[second].append(first)

    for i in range(components_sizes[1]):
        for j in range(components_sizes[2]):
            first = i + components_sizes[0]
            second = j + components_sizes[0] + components_sizes[1]
            if sps.bernoulli.rvs(probability):
                graph[first].append(second)
                graph[second].append(first)

    for i in range(components_sizes[2]):
        for j in range(components_sizes[0]):
            first = i + components_sizes[0] + components_sizes[1]
            second = j
            if sps.bernoulli.rvs(probability):
                graph[first].append(second)
                graph[second].append(first)

    return graph


# Генерирует все возможные наборы ребер между
# двумя заданными компонентами
def generate_all_edge_sets_between_2_components(first_component, second_component):
    edges_count = len(first_component) * len(second_component)
    edge_sets = []
    for bit_mask in range(1, 2 ** edges_count):
        edges = []
        current_edge = [0, 0]
        for i in range(edges_count):
            if (2 ** i) & bit_mask != 0:
                edges.append([first_component[current_edge[0]], second_component[current_edge[1]]])
                current_edge[1] += 1
                if current_edge[1] == len(second_component):
                    current_edge[0] += 1
                    current_edge[1] = 0
        edge_sets.append(edges)
    return edge_sets


# Строит граф по заданным ребрам
def build_graph_by_edges(edges, vertices_count):
    graph = [[] for i in range(vertices_count)]
    for ind in range(3):
        for edge in edges[ind]:
            graph[edge[0]].append(edge[1])
            graph[edge[1]].append(edge[0])
    return graph


# Генерирует все 3-раскрашиваемые графы с заданным количеством вершин,
# в которых между каждыми двумя компонентами (из трех) есть ребро
def generate_all_3_coloring_graphs_with_fixed_vertices_count(vertices_count):
    graphs = []
    for i in range(1, vertices_count + 1):
        for j in range(i + 1):
            if i + j > vertices_count:
                continue
            if vertices_count - i - j > j:
                continue

            # Делим вершины на 3 компоненты
            components = [[], [], []]
            for vertex_ind in range(i):
                components[0].append(vertex_ind)
            for vertex_ind in range(i, i + j):
                components[1].append(vertex_ind)
            for vertex_ind in range(i + j, vertices_count):
                components[2].append(vertex_ind)

            # Генерируем все возможные наборы ребер между каждыми двумя компонентами
            edge_sets = []
            edge_sets.append(generate_all_edge_sets_between_2_components(components[0], components[1]))
            edge_sets.append(generate_all_edge_sets_between_2_components(components[1], components[2]))
            edge_sets.append(generate_all_edge_sets_between_2_components(components[2], components[0]))
            for edges01 in edge_sets[0]:
                for edges12 in edge_sets[1]:
                    for edges20 in edge_sets[2]:
                        graphs.append(build_graph_by_edges([edges01, edges12, edges20], vertices_count))
    return graphs


class Test3Coloring:

    @pytest.mark.parametrize("probability", [0., 0.01, 0.1, 0.5, 0.75, 0.95, 1.])
    def test_random_3_coloring_graph_coloring(self, probability):
        graph_variants = [[0, 1, 0], [10, 3, 0], [10, 10, 10], [20, 30, 10], [100, 1, 1], [1000, 100, 100]]
        for components_sizes in graph_variants:
            graph = generate_random_graph(components_sizes, probability)
            if probability == 1.:
                print(graph)
            colors = color_graph(graph)
            assert(coloring_is_valid(graph, colors))

    # def test_all_3_coloring_graphs_coloring(self):
    #     for vertices_count in range(1, 8):
    #         graphs = generate_all_3_coloring_graphs_with_fixed_vertices_count(vertices_count)
    #         for graph in graphs:
    #             colors = color_graph(graph)
    #             assert (coloring_is_valid(graph, colors))

