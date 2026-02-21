# Comparaison de Métaheuristiques pour le Problème du Voyageur de Commerce (TSP)

Université Hassan II de Casablanca – ENSET Mohammedia  
Master : SDIA (Sciences des Données et Intelligence Artificielle)  
Module : Optimisation & Métaheuristiques  
Encadrant : Prof. MESTARI  

👥 Réalisé par :  
Mustapha Aarab  
Ilyass Moussnaoui  
Aya Agrigah  

---

## 📝 Description du projet

Ce projet a pour objectif de comparer plusieurs métaheuristiques appliquées au Problème du Voyageur de Commerce (TSP) à partir d’instances de la bibliothèque TSPLIB.

L’étude vise à analyser les performances des algorithmes selon plusieurs critères :

- Qualité des solutions (coût du tour)
- Temps d’exécution
- Intensité de recherche (voisins testés)
- Capacité d’exploration (mouvements acceptés)

Chaque configuration est évaluée à partir de 30 exécutions indépendantes afin d’obtenir des résultats statistiquement significatifs.

---

## 🧠 Métaheuristiques implémentées

Les algorithmes suivants ont été développés :

🏔️ Hill Climbing (Best Improvement)  
🔁 Hill Climbing (First Improvement)  
🔄 Multi-Start Hill Climbing  
🔥 Recuit Simulé (Simulated Annealing)  
🚀 Recherche Tabou (Tabu Search)  

Chaque méthode est testée avec deux structures de voisinage :

- Swap (échange de deux villes)
- 2-opt (inversion de segment)

---

## 📂 Structure du projet


project/
├── algo.py # Implémentation des métaheuristiques
├── exemple.py # Script principal d’expérimentation
├── data/ # Instances TSPLIB
│ ├── ulysses22.tsp
│ ├── eil51.tsp
│ └── st70.tsp
└── resultat/ # Résultats et graphiques générés


---

## 📊 Protocole expérimental

- 3 instances TSPLIB (22, 51 et 70 villes)
- 30 exécutions indépendantes par algorithme
- Budget d’évaluation fixe
- Mesures collectées :
  - Meilleur coût
  - Moyenne et écart-type
  - Temps d’exécution
  - Nombre de voisins testés
  - Nombre de mouvements acceptés

---

## 📈 Résultats générés

Après exécution, le dossier `resultat/` contient :

- `tsp_benchmark_results.csv` — Ensemble des résultats expérimentaux
- `chapter1_cost_*.png` — Comparaison des coûts par instance
- `chapter2_time_*.png` — Comparaison des temps d’exécution
- `chapter3_tested_*.png` — Comparaison des voisins testés
- `chapter4_explored_*.png` — Comparaison des mouvements acceptés

---

## ⚙️ Installation

Cloner le dépôt :

```bash
git clone <lien-du-depot>
cd project

Installer les dépendances :

pip install -r requirements.txt
▶️ Exécution

Lancer les expériences avec :

python exemple.py

Les résultats et graphiques seront automatiquement générés dans le dossier resultat/.
🎯 Résumé des conclusions

Le voisinage 2-opt surpasse systématiquement le swap.

La Recherche Tabou (2-opt) offre les meilleures performances globales.

Le Multi-Start HC constitue un bon compromis qualité/temps.

Le HC Best est plus sensible aux optima locaux.

L’impact de la taille de l’instance devient significatif sur les grandes instances.
