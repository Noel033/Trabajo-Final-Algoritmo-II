import networkx as nx
import matplotlib.pyplot as plt

tareas = [
    "Escribir guion",
    "Hacer storyboard",
    "Crear fondos",
    "Crear Sonidos",
    "Crear lógica de APUS",
    "Crear lógica de Illas",
    "Integrar",
    "Publicar"
]

#Crear digrafo
G = nx.DiGraph()

#Agregar nodos al grafo
G.add_nodes_from(tareas)

G.add_edge("Escribir guion", "Hacer storyboard")
G.add_edge("Hacer storyboard", "Crear fondos")
G.add_edge("Cresr fondos", "Crear Sonidos")
G.add_edge("Crear Sonidos", "Crear lógica de APUS")
G.add_edge("Crear lógica de APUS", "Crear lógica de Illas")
G.add_edge("Crear lógica de Illas", "Integrar")
G.add_edge("Integrar", "Publicar")

# Ordenación topológica
orden = list(nx.topological_sort(G))

# Imprimir
print("Orden e tareas: ")
for i, tarea in enumerate(orden, 1):
    print(f"{i}.{tarea}")

# Determinar posición para la visualización
pos = nx.spring_layout(G)

plt.figure(figsize = (10, 6))
plt.title("Dependencias del Proyecto: Videojuego")

nx.draw(G, pos, with_labels = True, node_color="lightcoral", node_size=2000, font_size=10, font_weight="bold", arrowsize = 20)

#mostrar el grafo
plt.show()
