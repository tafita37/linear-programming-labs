from pulp import LpMaximize , LpProblem , LpVariable, LpInteger
# 1. Dé finir le mod èle d’ optimisation avec un objectif de maximisation
model = LpProblem ( name =" exemple - plne ", sense = LpMaximize )
# 2. Dé finir les variables de dé cision : x et y ( enti ères , non n é gatives )
x1 = LpVariable ( name ="x1", lowBound =0 , cat = LpInteger )
x2 = LpVariable ( name ="x2", lowBound =0 , cat = LpInteger )
x3 = LpVariable ( name ="x3", lowBound =0 , cat = LpInteger )
x4 = LpVariable ( name ="x4", lowBound =0 , cat = LpInteger )
# 3. Dé finir la fonction objectif
model += 40 * x1 + 30 * x2 + 20 * x3 + 10 * x4, " Fonction_objectif "
# 4. Ajouter les contraintes
model += ( 6 * x1 + 4 * x2 + 3 * x3 + 2 * x4 <= 10 , " Contrainte_1 ")
# 5. Ré soudre le probl ème avec le solveur par dé faut ( CBC)
model . solve ()
# 6. Afficher les ré sultats
print ( f"Statut : { model . status }")
print (f"x1 = {x1.value()}, x2 = {x2.value()}, x3 = {x3.value()}, x4 = {x4.value()}")
print (f"Valeur optimale de Z = { model.objective.value()}")