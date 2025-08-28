from pulp import LpMinimize, LpProblem, LpVariable, LpBinary, lpSum

# 1. Définir le modèle d’optimisation (minimisation du coût)
model = LpProblem(name="assignment_problem", sense=LpMinimize)

# 2. Définir les variables binaires xij
x = [[LpVariable(name=f"x{i+1}{j+1}", cat=LpBinary) for j in range(3)] for i in range(3)]

# 3. Matrice des coûts
costs = [
    [6, 4, 3],  # Ouvrier 1
    [2, 6, 5],  # Ouvrier 2
    [4, 3, 7]   # Ouvrier 3
]

# 4. Définir la fonction objectif
model += lpSum(costs[i][j] * x[i][j] for i in range(3) for j in range(3)), "Total_Cost"

# 5. Ajouter les contraintes
# Chaque ouvrier fait exactement une tâche
for i in range(3):
    model += lpSum(x[i][j] for j in range(3)) == 1, f"Ouvrier_{i+1}_one_task"

# Chaque tâche est attribuée à un seul ouvrier
for j in range(3):
    model += lpSum(x[i][j] for i in range(3)) == 1, f"Tache_{j+1}_one_worker"

# 6. Résoudre le problème
model.solve()

# 7. Afficher les résultats
for i in range(3):
    for j in range(3):
        if x[i][j].value() == 1:
            print(f"Ouvrier {i+1} -> Tâche {j+1}")

print(f"Coût total minimum : {model.objective.value()}")