import ast
import os
import random
from _ast import FunctionDef, Assign, Call, Name, ClassDef, For, If
from typing import Any
from PIL import Image, ImageDraw, ImageFont
import settings as s
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class kanisaVisitor(ast.NodeVisitor):
    def __init__(self):
        self.tree_name = None
        self.current_tree = None
        self.graphed_tree_image = Image.new("RGBA", (641, 1005), s.ANTIQUE_WHITE)
        self.tree_draw = ImageDraw.Draw(self.graphed_tree_image)
        self.curr_func_pos = [5, 5]
        self.func_rect_size = [190, 80]
        self.func_rect_list = []
        self.G = nx.grid_graph(dim=(8, 3))
        # self.G = nx.DiGraph()
        self.functions = set()
        self.variables = set()
        # self.current_function = None
        # self.current_method = None
        self.font = ImageFont.truetype(f'{os.getcwd()}/assets/Fonts/Akt-Medium.ttf', 16)
        self.var_to_func = {}
        self.class_info = {}

    def visit_ClassDef(self, node: ClassDef) -> Any:
        class_name = node.name
        self.class_info['name'] = class_name
        self.class_info['methods'] = []
        self.class_info['variables'] = []
        self.class_info['for_loops'] = []
        self.class_info['if_statements'] = []
        self.class_info['calls'] = []
        self.class_info['attributes'] = []

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                self.class_info['methods'].append(item.name)
            elif isinstance(item, ast.Assign):
                targets = [t.id for t in item.targets if isinstance(t, ast.Name)]
                self.class_info['attributes'].extend(targets)
        # self.G.add_node(class_name)
        # self.current_scope = class_name
        self.generic_visit(node)
        # self.current_scope = None

    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        self.current_method = node.name
        self.generic_visit(node)
        del self.current_method

    # def visit_Call(self, node: Call) -> Any:
    #     if isinstance(node.func, ast.Name) and self.current_scope:
    #         called_func = node.func.id
    #         self.functions.add(called_func)
    #         self.G.add_node(called_func)
    #         self.G.add_edge(self.current_scope, called_func)
    #     elif isinstance(node.func, ast.Attribute) and self.current_scope:
    #         called_func = f"{node.func.value}.{node.func.attr}"
    #         self.functions.add(called_func)
    #         self.G.add_node(called_func)
    #         self.G.add_edge(self.current_scope, called_func)
    #     self.generic_visit(node)

    def visit_Name(self, node: Name) -> Any:
        if isinstance(node.ctx, ast.Load) and node.id not in ['print', 'len']:
            self.class_info['calls'].append(node.id)
        self.generic_visit(node)

    def visit_Assign(self, node: Assign) -> Any:
        if hasattr(self, 'current_method'):
            targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            self.class_info['variables'].extend(targets)
        self.generic_visit(node)

    def visit_For(self, node: For) -> Any:
        self.class_info['for_loops'].append(f"for_{len(self.class_info['for_loops'])}")
        self.generic_visit(node)

    def visit_If(self, node: If) -> Any:
        self.class_info['if_statements'].append(f"if_{len(self.class_info['if_statements'])}")
        self.generic_visit(node)

    # def visit_c

    def parse_new_tree(self, file_code):
        self.current_tree = ast.parse(file_code)

    def visit_it(self):
        if self.current_tree:
            self.visit(self.current_tree)
        self.graphed_tree_image.save(f"{self.tree_name}_graphted.png")
        print("Exiting the visitor area....")


def draw_shell_graph(file_path):
    class_info = parse_python_file(file_path)
    G = build_graph(class_info)
    class_name = class_info['name']

    shells = [[class_name]]
    outer_nodes = [n for n in G.nodes() if n != class_name]
    shells.append(outer_nodes)
    pos = nx.shell_layout(G, shells)

    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightgreen', node_shape='o', font_size=10,
            font_weight='bold', edge_color='gray', arrows=True)
    plt.title(f"Shell graph for {class_name} class")
    plt.show()


def draw_hexagon_graph(file_path):
    class_info = parse_python_file(file_path)
    G = build_graph(class_info)
    class_name = class_info['name']

    pos = {class_name: (0, 0)}
    angles = np.linspace(0, 2 * np.pi, 7)[:-1]
    radius = 2.5
    neighbors = list(G.neighbors(class_name))
    num_neighbors = len(neighbors)
    ring = 1
    placed = 0
    categories = {
        'variables': class_info['variables'],
        'methods': class_info['methods'],
        'for_loops': class_info['for_loops'],
        'if_statements': class_info['if_statements'],
        'calls': class_info['calls'],
        'attributes': class_info['attributes']
    }

    for idx, (cat, items) in enumerate(categories.items()):
        print(f"==CATEGORY: {cat}==")
        angle = angles[idx]
        base_pos = (radius * np.cos(angle), radius * np.sin(angle))
        outward_dir = (np.cos(angle), np.sin(angle))
        # direction = (radius * np.cos(angle), radius * np.sin(angle))
        for i, item in enumerate(items):
            print(f"{i}: {item}")
            # offset = (i * 0.5 * np.cos(angle + np.pi / 2), i * 0.5 * np.sin(angle + np.pi / 2))
            pos[item] = (base_pos[0] + i * 1.5 * outward_dir[0],
                         base_pos[1] + i * 1.5 * outward_dir[1])

    # for node in neighbors:
    #     if placed < 6:
    #         angle = angles[placed]
    #         pos[node] = (radius * np.cos(angle), radius * np.sin(angle))
    #     else:
    #         ring_angle = angles[placed % 6]
    #         pos[node] = (
    #             radius * ring * np.cos(ring_angle),
    #             radius * ring * np.sin(ring_angle)
    #         )
    #         if placed % 6 == 0:
    #             ring += 1
    #     placed += 1
    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='lightblue', node_shape='h',
            font_size=10, font_weight='bold', edge_color='gray', arrows=True)
    plt.title(f"Hexagonal Grid of Class: {class_name}")
    plt.show()


def draw_circular_graph(file_path):
    class_info = parse_python_file(file_path)
    G = build_graph(class_info)
    class_name = class_info['name']

    pos = nx.circular_layout(G)

    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightcoral', node_shape='o', font_size=10,
            font_weight='bold', edge_color='gray', arrows=True)


def parse_python_file(file_path):
    with open(file_path, "r", encoding="utf8") as file:
        tree = ast.parse(file.read())
    visitor = kanisaVisitor()
    visitor.visit(tree)
    return visitor.class_info


def build_graph(class_info):
    class_name = class_info['name']
    G = nx.DiGraph()
    G.add_node(class_name)

    categories = {
        'variables': class_info['variables'],
        'methods': class_info['methods'],
        'for_loops': class_info['for_loops'],
        'if_statements': class_info['if_statements'],
        'calls': class_info['calls'],
        'attributes': class_info['attributes']
    }
    for cat, items in categories.items():
        for item in items:
            G.add_node(item)
            G.add_edge(class_name, item)
    return G


def color_and_draw_graph(graph, functions, variables, pos, extra=None):
    node_colors = []
    for node in graph.nodes():
        if node in functions:
            node_colors.append('lightblue')
        elif node in variables:
            node_colors.append('lightgreen')
        else:
            node_colors.append('lightgray')

    nx.draw(graph, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=1500,
            font_size=10,
            arrows=True,
            edge_color='gray')
    plt.title("GRAPHTED")
    plt.show()
