# Prérequis

Pour exécuter ce projet, vous aurez besoin de Python et de plusieurs de ses bibliothèques. Voici les commandes pour les installer sur un système basé sur Debian comme Ubuntu :

```bash
sudo apt-get install python3-tk
sudo apt-get install python3-networkx
sudo apt-get install python3-matplotlib
```

*Assurez-vous que toutes les dépendances sont correctement installées avant de tenter d'exécuter l'application.*

# Coloriage de graphe et Résolution de Sudoku
Ce projet explore le problème du coloriage de graphes non orientés et développe une application capable de résoudre des grilles de Sudoku à l'aide d'algorithmes de coloriage de graphes. Le coloriage de graphe est le processus d'attribution de couleurs aux sommets d'un graphe de telle sorte que deux sommets adjacents n'aient jamais la même couleur. Le graphe est non réflexif, ce qui signifie qu'aucun sommet n'est connecté à lui-même.

# Objectifs du Projet

Les principaux objectifs de ce projet sont :

- Implémenter trois algorithmes de coloriage de graphes en Python :
	Algorithme glouton.
	Algorithme de Welsh-Powell.
	Algorithme de backtracking.

- Concevoir et mettre en œuvre un algorithme de coloriage adapté à un graphe dynamique, où le nombre de sommets et d'arêtes peut changer au fil du temps.

- Développer une application qui permet à l'utilisateur de colorier un graphe de son choix et de résoudre des grilles de Sudoku en utilisant un algorithme de coloriage.
