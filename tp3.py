from pulp import LpMinimize, LpProblem, LpVariable, LpBinary, lpSum

# Villes
cities = ['A', 'B', 'C', 'D', 'E']
n = len(cities)

# 1. Définir le modèle d'optimisation (minimisation du coût)
model = LpProblem(name="tsp_problem", sense=LpMinimize)

# 2. Définir les variables binaires xij
x = [[LpVariable(name=f"x_{cities[i]}_{cities[j]}", cat=LpBinary) for j in range(n)] for i in range(n)]

# 3. Matrice des distances
distances = [
    [0, 12, 10, 19, 8],  # A
    [12, 0, 3, 7, 6],    # B
    [10, 3, 0, 2, 4],    # C
    [19, 7, 2, 0, 3],    # D
    [8, 6, 4, 3, 0]      # E
]

# 4. Définir la fonction objectif (éviter les diagonales i=j)
model += lpSum(distances[i][j] * x[i][j] for i in range(n) for j in range(n) if i != j), "Total_Distance"

# 5. Ajouter les contraintes de base
# Chaque ville a exactement une sortie
for i in range(n):
    model += lpSum(x[i][j] for j in range(n) if i != j) == 1, f"Sortie_{cities[i]}"

# Chaque ville a exactement une entrée
for j in range(n):
    model += lpSum(x[i][j] for i in range(n) if i != j) == 1, f"Entree_{cities[j]}"

# 6. Variables MTZ pour éliminer les sous-tours (CORRIGÉ)
u = [LpVariable(name=f"u_{cities[i]}", lowBound=1, upBound=n-1, cat='Integer') for i in range(1, n)]

# Contraintes MTZ (pour toutes les paires i,j sauf la ville de départ A)
for i in range(1, n):
    for j in range(1, n):
        if i != j:
            model += u[i-1] - u[j-1] + n * x[i][j] <= n - 1, f"MTZ_{cities[i]}_{cities[j]}"

# Contraintes supplémentaires pour lier avec la ville A
for j in range(1, n):
    model += u[j-1] >= 1 + (1 - n) * (1 - x[0][j]) + (n - 3) * x[j][0], f"MTZ_A_{cities[j]}"

# 7. Résoudre le problème
model.solve()

# 8. Afficher le circuit optimal (CORRIGÉ)
print("Statut:", model.status)
if model.status == 1:
    # Reconstruction du tour
    tour = ['A']
    current = 0
    visited = set([0])
    
    while len(visited) < n:
        for j in range(n):
            if j != current and x[current][j].value() == 1 and j not in visited:
                tour.append(cities[j])
                current = j
                visited.add(j)
                break
    
    tour.append('A')  # Retour à A
    print("Circuit optimal :", " -> ".join(tour))
    print("Distance totale :", model.objective.value())
    
    # Afficher les arcs utilisés
    print("\nArcs utilisés:")
    for i in range(n):
        for j in range(n):
            if i != j and x[i][j].value() == 1:
                print(f"{cities[i]} -> {cities[j]} : {distances[i][j]}")
else:
    print("Aucune solution optimale trouvée")