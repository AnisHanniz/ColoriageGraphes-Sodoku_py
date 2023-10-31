
##Algorithme Glouton
import networkx as nx
import itertools
def greedy_coloring(graph):
    colors = {}
    for node in graph.nodes():
        used_colors = set(colors.get(neighbor, None) for neighbor in graph.neighbors(node))
        for color in range(len(graph.nodes())):
            if color not in used_colors:
                colors[node] = color
                break
    return colors

# Exemple d'utilisation :
G = nx.Graph()
G.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)])
greedy_colors = greedy_coloring(G)
print("Couleurs attribuées par l'algorithme glouton :", greedy_colors)

##Welsh_Powell
import networkx as nx
import itertools
def welsh_powell_coloring(graph):
    nodes = sorted(graph.nodes(), key=lambda node: -len(list(graph.neighbors(node))))
    colors = {}
    for node in nodes:
        used_colors = set(colors.get(neighbor, None) for neighbor in graph.neighbors(node))
        for color in range(len(graph.nodes())):
            if color not in used_colors:
                colors[node] = color
                break
    return colors

# Exemple d'utilisation :
G = nx.Graph()
G.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)])
welsh_powell_colors = welsh_powell_coloring(G)
print("Couleurs attribuées par l'algorithme de Welsh-Powell :", welsh_powell_colors)


##Backtracking
import networkx as nx
import itertools
def is_valid_coloring(graph, coloring):
    for node in graph.nodes():
        for neighbor in graph.neighbors(node):
            if coloring[node] == coloring[neighbor]:
                return False
    return True

def backtrack_coloring(graph):
    colors = {}
    nodes = list(graph.nodes())
    for color_order in itertools.permutations(range(len(graph.nodes()))):
        coloring = {nodes[i]: color_order[i] for i in range(len(nodes))}
        if is_valid_coloring(graph, coloring):
            return coloring

# Exemple d'utilisation :
G = nx.Graph()
G.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)])
backtrack_colors = backtrack_coloring(G)
print("Couleurs attribuées par l'algorithme de Backtracking :", backtrack_colors)

##Welsh-Powell Dynamique


import networkx as nx

def welsh_powell_coloring_dynamic(graph):
    def welsh_powell_coloring(graph):
        nodes = sorted(graph.nodes(), key=lambda node: -len(list(graph.neighbors(node))))
        colors = {}
        for node in nodes:
            used_colors = set(colors.get(neighbor, None) for neighbor in graph.neighbors(node))
            for color in range(len(graph.nodes())):
                if color not in used_colors:
                    colors[node] = color
                    break
        return colors

    coloring = welsh_powell_coloring(graph)

    def update_coloring(event):
        nonlocal coloring
        if event['action'] == 'add_node':
            graph.add_node(event['node'])
        elif event['action'] == 'remove_node':
            graph.remove_node(event['node'])
        elif event['action'] == 'add_edge':
            graph.add_edge(event['node1'], event['node2'])
        elif event['action'] == 'remove_edge':
            graph.remove_edge(event['node1'], event['node2'])
        coloring = welsh_powell_coloring(graph)

    return update_coloring

# Exemple d'utilisation :
G = nx.Graph()
G.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)])

update_coloring = welsh_powell_coloring_dynamic(G)
print("Couleurs attribuées par l'algorithme de Welsh-Powell :", update_coloring)

# Modifiez le graphe en ajoutant ou supprimant des nœuds ou des arêtes
update_coloring({'action': 'add_node', 'node': 5})
update_coloring({'action': 'add_edge', 'node1': 0, 'node2': 5})

print("Nouvelles couleurs après modification du graphe :", update_coloring)


##

import tkinter as tk
from tkinter import messagebox
import networkx as nx
from sudoku_solver import solve_sudoku  # Vous devrez créer un module sudoku_solver pour résoudre Sudoku

# Fonction pour colorier un graphe
def color_graph(graph, algorithm):
    if algorithm == "Glouton":
        colors = greedy_coloring(graph)
    elif algorithm == "Welsh-Powell":
        colors = welsh_powell_coloring(graph)
    elif algorithm == "Backtracking":
        colors = backtrack_coloring(graph)
    return colors

# Fonction pour résoudre Sudoku
def solve_sudoku_puzzle(sudoku_grid):
    return solve_sudoku(sudoku_grid)

# Interface utilisateur
def color_graph_ui():
    algorithm = algorithm_var.get()
    G = nx.Graph()
    # Ajoutez les arêtes du graphe à partir de l'entrée de l'utilisateur

    colors = color_graph(G, algorithm)
    # Affichez le résultat de la coloration sur l'interface

def solve_sudoku_ui():
    sudoku_grid = []
    # Lisez les valeurs du Sudoku à partir de l'interface utilisateur

    solution = solve_sudoku_puzzle(sudoku_grid)
    if solution:
        print("1")
        # Affichez la solution sur l'interface utilisateur
        # Placez le code pour afficher la solution ici
    else:
        messagebox.showerror("Erreur", "La grille Sudoku n'a pas de solution valide.")


# Créez la fenêtre principale
root = tk.Tk()
root.title("Coloration de graphe et résolution de Sudoku")

# Menu déroulant pour choisir l'algorithme de coloration
algorithm_var = tk.StringVar()
algorithm_var.set("Glouton")  # Algorithme par défaut
algorithm_label = tk.Label(root, text="Algorithme de coloration:")
algorithm_label.pack()
algorithm_menu = tk.OptionMenu(root, algorithm_var, "Glouton", "Welsh-Powell", "Backtracking")
algorithm_menu.pack()

# Boutons pour lancer la coloration du graphe et la résolution du Sudoku
color_button = tk.Button(root, text="Colorier le graphe", command=color_graph_ui)
color_button.pack()
sudoku_button = tk.Button(root, text="Résoudre Sudoku", command=solve_sudoku_ui)
sudoku_button.pack()

# Ajoutez d'autres éléments d'interface utilisateur pour entrer le graphe et le Sudoku

root.mainloop()
