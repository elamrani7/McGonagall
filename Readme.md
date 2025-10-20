Voici mon architecture de projet actuelle :

DEFIS13/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── gui.py
│   ├── index.py
│   ├── main.py
│   ├── models.py
│   └── wigor_api.py
│
├── build/
│   ├── main/
│   └── McGonagallPlanner.exe
│
├── dist/
│   └── McGonagallPlanner.exe
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_gui.py
│   └── test_models.py
│
├── main.spec
├── html.html
└── .coverage

Je veux que tu génères pour chaque fichier le code adapté selon les rôles suivants :

### 🔹 app/wigor_api.py
- Contient une classe `WigorClient` qui se connecte à l’API wigorservices.
- Utilise `requests` avec un header `Cookie` passé en paramètre.
- Fournit une méthode `get_schedule()` qui renvoie la réponse JSON formatée.
- Gère les erreurs (401, 404, 500) avec des exceptions personnalisées.

### 🔹 app/models.py
- Définit une dataclass `ScheduleItem` avec les champs : `date`, `start_time`, `end_time`, `subject`, `room`, `teacher`.
- Fournit une fonction `parse_schedule(json_data)` pour transformer la réponse API en liste de `ScheduleItem`.

### 🔹 app/gui.py
- Utilise `tkinter` ou `PySide6` pour créer une fenêtre "McGonagall Planner".
- La fenêtre contient :
  - une zone pour coller les cookies,
  - un bouton "Charger emploi du temps" → appelle `WigorClient.get_schedule()`,
  - une table affichant les cours (date, heure, matière, salle, prof),
  - une zone de logs/erreurs.
- Le code doit être bien organisé (classe `MainWindow`) et testable.

### 🔹 app/main.py
- Point d’entrée du programme.
- Instancie la fenêtre depuis `gui.py`.
- Charge les cookies si présents (optionnel).
- Lance l’application avec `if __name__ == "__main__":`.

### 🔹 app/config.py
- Contient les constantes (URL de l’API, paramètres).
- Exemple : `BASE_URL = "https://api.wigorservices.net/schedule"`

### 🔹 app/index.py
- Peut servir à des fonctions utilitaires : formatage, logs, regroupement par jour.

### 🔹 tests/test_api.py
- Mock `requests.get` pour tester les cas : succès (200), erreur 401, erreur 500.
- Vérifie que `get_schedule()` renvoie bien la liste d’objets `ScheduleItem`.

### 🔹 tests/test_models.py
- Teste `parse_schedule()` avec un JSON correct, un JSON incomplet, et un JSON vide.

### 🔹 tests/test_gui.py
- Teste que l’interface se crée sans erreur.
- Mock `WigorClient.get_schedule()` pour vérifier que le tableau se met à jour.

### 🔹 build/main.spec
- Fichier PyInstaller pour générer un exécutable Windows (`McGonagallPlanner.exe`).
- OneFile, avec icône et nom du programme.

### ✅ Contraintes générales :
- Respecte PEP8.
- Fournis docstrings dans chaque module.
- Fournis logs (`logging`).
- Écris des tests Pytest avec coverage > 80%.
- Prépare le code à être packagé avec PyInstaller.
- N’utilise pas de données réelles de connexion.
- Tout doit fonctionner avec Python 3.11+.
