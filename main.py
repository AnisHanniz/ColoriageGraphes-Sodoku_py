import tkinter as tk
from tkinter import messagebox, filedialog,simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from sudoku_solver import solve_sudoku_board
from graphe_coloration import (
    greedy_coloring,
    welsh_powell_coloring,
    backtrack_coloring,
    welsh_powell_coloring_dynamic
)

# Variables Globales
G = nx.Graph()
dynamic_coloring_func = None

def update_vertex_buttons():
    global add_vertex_button, remove_vertex_button, root, G, dynamic_coloring_func , refresh_graph_button
    if algorithm_var.get() == "WP-Dynamique":
        add_vertex_button.pack()
        remove_vertex_button.pack()
        refresh_graph_button.pack()
        root.geometry("450x250")
        if not dynamic_coloring_func:
            _, dynamic_coloring_func = welsh_powell_coloring_dynamic(G)
            colors = dynamic_coloring_func({'action': 'initial'})
            draw_graph2(G, colors)
    else:
        add_vertex_button.pack_forget()
        remove_vertex_button.pack_forget()
        refresh_graph_button.pack_forget()
        root.geometry("400x150")
        dynamic_coloring_func = None

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_cord = int((screen_width / 2) - (width / 2))
    y_cord = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x_cord}+{y_cord}")

def draw_graph(graph, colors=None):
    pos = nx.spring_layout(graph)
    default_color = 'gray'
    node_colors = [colors.get(node, default_color) for node in graph.nodes()] if colors else default_color
    plt.figure()
    nx.draw(graph, pos, with_labels=True, font_weight='bold', node_color=node_colors)
    plt.title("Coloration du graphe")
    plt.show()
    
# Conserver les références pour la figure et les axes
fig, ax = None, None

def draw_graph2(graph, colors=None):
    global fig, ax
    pos = nx.spring_layout(graph) 
    default_color = 'gray'
    node_colors = [colors.get(node, default_color) for node in graph.nodes()] if colors else default_color

    if fig is None:
        plt.ion() # Activer le mode interactif pour mettre à jour le plot
        fig, ax = plt.subplots()
    else:
        ax.clear()   # Effacer le dessin précédent

    nx.draw(graph, pos, ax=ax, with_labels=True, font_weight='bold', node_color=node_colors)
    plt.title("Coloration du graphe Dynamique")
    fig.canvas.draw()  # Mettre à jour la figure
    plt.pause(0.001)   # Pause pour assurer la mise à jour de la figure




def add_vertex():
    global G, dynamic_coloring_func
    new_node = simpledialog.askinteger("Input", "Entrez un sommet à ajouter:", parent=root)
    if new_node is None:
        messagebox.showinfo("Information", "Entrée vide.")
        return
    if new_node in G.nodes():
        messagebox.showinfo("Information", "Sommet existe déjà.")
        return

    G.add_node(new_node)
    
    connected_nodes = simpledialog.askstring("Input", "EVers:", parent=root)
    if connected_nodes:
        connected_nodes = [int(n.strip()) for n in connected_nodes.split(' ') if n.strip().isdigit()]
        for node in connected_nodes:
            if node in G.nodes():
                G.add_edge(new_node, node)
            else:
                messagebox.showinfo("Information", f"Sommet {node} N'éxiste pas, ajout non effectué.")

    if dynamic_coloring_func:
        colors = dynamic_coloring_func({'action': 'add_node', 'node': new_node})
        draw_graph2(G, colors)
    else:
        draw_graph2(G, None)

def remove_vertex():
    global G, dynamic_coloring_func
    
    def get_node_to_remove():
        while True:
            node = simpledialog.askinteger("Input", "Entrez un sommet à supprimer:", parent=root)
            if node is None:
                messagebox.showinfo("Information", "Pas d'entrée.")
                return None  # L'utilisateur a annulé l'entrée
            if node in G.nodes():
                return node
            messagebox.showinfo("Information", "Sommet entré non existant.")

    node_to_remove = get_node_to_remove()
    if node_to_remove is None: 
        return

    try:
        if dynamic_coloring_func:
            colors = dynamic_coloring_func({'action': 'remove_node', 'node': node_to_remove})
        else:
            colors = None
        G.remove_node(node_to_remove)
        draw_graph2(G, colors)
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue: {e}")
    else:
        root.update_idletasks()
        root.update()


def refresh_graph():
    global G, dynamic_coloring_func
    if dynamic_coloring_func:
        colors = dynamic_coloring_func({'action': 'refresh'})
    else:
        colors = None
    draw_graph2(G, colors)
        
def color_graph(graph, algorithm):
    global G, dynamic_coloring_func 
    colors = None
    if algorithm == "Glouton":
        colors = greedy_coloring(graph)
    elif algorithm == "Welsh-Powell":
        colors, _ = welsh_powell_coloring(graph)
    elif algorithm == "WP-Dynamique":
        colors, dynamic_coloring_func = welsh_powell_coloring_dynamic(G)
        colors = dynamic_coloring_func({'action': 'initial'})
    elif algorithm == "Backtracking":
        colors = backtrack_coloring(graph)
    
    sorted_colors = {node: colors[node] for node in sorted(colors.keys())}
    return sorted_colors

def color_graph_ui(algorithm):
    edge_input = tk.Toplevel(root)
    edge_input.title("Entrez les arêtes du graphe")
    center_window(edge_input, 300, 120)
    tk.Label(edge_input, text="Entrez les arêtes du graphe").pack()
    tk.Label(edge_input, text="Exemple: 0 1 1 2 2 3").pack()
    edges_entry = tk.Entry(edge_input)
    edges_entry.pack()

    update_vertex_buttons()
    def get_edges():
        edges_str = edges_entry.get()
        edges_list = edges_str.split()
        edges = [int(noeud) for noeud in edges_list]

        if len(edges) % 2 == 0:
            edge_tuples = [(edges[i], edges[i + 1]) for i in range(0, len(edges), 2)]
            G = nx.Graph()
            G.add_edges_from(edge_tuples)
            colors = color_graph(G, algorithm)
            edge_input.destroy()
            draw_graph(G, colors)
        else:
            messagebox.showerror("Erreur", "Nombre impair de nœuds. Assurez-vous d'avoir des paires de nœuds pour former des arêtes.")

    tk.Button(edge_input, text="Valider", command=get_edges).pack()

def sudoku_ui():
    def solve():
        sudoku_board = []
        for i in range(9):
            row = []
            for j in range(9):
                value = entries[i][j].get()
                if value.isdigit() and 0 <= int(value) <= 9: 
                    row.append(int(value))
                elif value == '':  
                    row.append(0)
                else:
                    messagebox.showerror("Erreur", "Les valeurs doivent être des chiffres entre 1 et 9 ou laissées vides.")
                    return  
            sudoku_board.append(row)

        solved, solution = solve_sudoku_board(sudoku_board)
        if solved:
            for i in range(9):
                for j in range(9):
                    entries[i][j].delete(0, tk.END)
                    entries[i][j].insert(0, str(solution[i][j]))
            messagebox.showinfo("Sudoku Résolu", "La grille de Sudoku a été résolue avec succès!")
        else:
            messagebox.showerror("Erreur", "La grille de Sudoku ne peut pas être résolue.")

    def import_sudoku():
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for i, line in enumerate(lines[:9]):
                    for j, value in enumerate(line.strip()):
                        if value.isdigit() and 0 <= int(value) <= 9:
                            entries[i][j].delete(0, tk.END)
                            entries[i][j].insert(0, value)
                        else:
                            messagebox.showerror("Erreur", "Le fichier ne contient pas une grille Sudoku valide.")

    def clear_entries():
        for i in range(9):
            for j in range(9):
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, "0")

    sudoku_entry_window = tk.Toplevel(root)
    sudoku_entry_window.title("Entrer les valeurs du Sudoku")
    center_window(sudoku_entry_window, 350, 370)
    
    tk.Label(sudoku_entry_window, text="Entrez les valeurs du Sudoku (0 pour les cases vides)").grid(row=0, columnspan=9)

    entries = []
    for i in range(9):
        row = []
        for j in range(9):
            entry = tk.Entry(sudoku_entry_window, width=2)
            entry.grid(row=i+1, column=j)
            entry.insert(0, "0")
            row.append(entry)
        entries.append(row)
    
    clear_button = tk.Button(sudoku_entry_window, text="Effacer", command=clear_entries)
    clear_button.grid(row=10, columnspan=9)


    
    
    solve_button = tk.Button(sudoku_entry_window, text="Résoudre", command=solve)
    solve_button.grid(row=12, columnspan=9)

    import_button = tk.Button(sudoku_entry_window, text="Importer Sudoku (fichier .txt)", command=import_sudoku)
    import_button.grid(row=13, columnspan=9)

    tk.Label(sudoku_entry_window, text="Algorithme utilisé : Backtracking").grid(row='14', columnspan=9)
        

# Fenêtre principale de l'application
root = tk.Tk()
root.title("Coloration de graphe et résolution de Sudoku")
root_instructions = tk.Label(root, text="Choisissez un algorithme et lancez l'action désirée.")
root_instructions.pack()
center_window(root, 400, 150)

algorithm_var = tk.StringVar(value="Glouton")
algorithm_var.set("Glouton")
algorithm_label = tk.Label(root, text="Algorithme de coloration:")
algorithm_label.pack()

algorithm_menu = tk.OptionMenu(root, algorithm_var, "Glouton", "Welsh-Powell", "Backtracking", "WP-Dynamique", command=lambda _: update_vertex_buttons())
algorithm_menu.pack()

color_button = tk.Button(root, text="Colorier un graphe", command=lambda: color_graph_ui(algorithm_var.get()))
color_button.pack()

sudoku_button = tk.Button(root, text="Résoudre une grille de Sudoku", command=sudoku_ui)
sudoku_button.pack()

add_vertex_button = tk.Button(root, text="+ Sommet", command=add_vertex)
remove_vertex_button = tk.Button(root, text="- Sommet", command=remove_vertex)
refresh_graph_button = tk.Button(root, text="Rafraichir", command=refresh_graph)
update_vertex_buttons()

root.mainloop()