Description de l’architecture

L’application est structurée en deux parties principales :

- **app/** : contient le code source de l’application
  - `main.py` : point d’entrée
  - `gui.py` : interface graphique Tkinter
  - `wigor_api.py` : communication avec l’API
  - `models.py` : classe `Course`
  - `config.py` : constantes globales

- **tests/** : contient les tests unitaires
  - `test_models.py` : tests de la classe `Course`
  - `test_api.py` : tests simulés de l’API
  - `test_gui.py` : tests simulés de l’interface

---

## 3. Fonctionnement de l’application

- L’utilisateur saisit ses identifiants ou un cookie.
- L’application se connecte à l’API WigorServices.
- Les cours sont récupérés et affichés dans une table.
- L’interface est construite avec Tkinter.
- Les erreurs réseau ou d’authentification sont gérées proprement.
- Un mode “mock” est prévu si l’API est inaccessible.

---

## 4. Couverture des tests

Commande utilisée :

```bash
pytest --cov=app --cov-report=term-missing
