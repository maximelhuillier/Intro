# 📁 Structure du Projet AnalystHelper

```
analyst-helper/
│
├── 📄 README.md                    # README GitHub principal
├── 📄 README_ANALYST_HELPER.md     # Documentation complète de l'outil
├── 📄 QUICKSTART.md                # Guide de démarrage rapide
├── 📄 STRUCTURE.md                 # Ce fichier (structure du projet)
├── 📄 LICENSE                      # Licence MIT
├── 📄 requirements.txt             # Dépendances Python
├── 📄 setup.py                     # Script d'installation
├── 📄 .gitignore                   # Fichiers à ignorer par Git
│
├── 🐍 demo.py                      # Script de démonstration interactif
├── 🐍 example_simple.py            # Exemple simple d'utilisation
├── 🐍 test_analyst_helper.py       # Tests unitaires
│
└── 📦 analyst_helper/              # Package principal
    ├── __init__.py                 # Point d'entrée du package
    │
    ├── 📂 core/                    # Modules principaux
    │   ├── __init__.py
    │   ├── scanner.py              # Scanner d'arborescence
    │   ├── extractor.py            # Extracteur de pièces jointes
    │   ├── classifier.py           # Classificateur de fichiers
    │   └── reporter.py             # Générateur de rapports HTML
    │
    └── 📂 utils/                   # Utilitaires
        └── __init__.py
```

## 📋 Description des Fichiers

### 📖 Documentation

| Fichier | Description |
|---------|-------------|
| `README_ANALYST_HELPER.md` | Documentation complète : fonctionnalités, installation, exemples |
| `QUICKSTART.md` | Guide pour démarrer en 5 minutes |
| `STRUCTURE.md` | Ce fichier - vue d'ensemble du projet |

### 🚀 Scripts Exécutables

| Fichier | Usage | Niveau |
|---------|-------|--------|
| `example_simple.py` | Exemple basique à personnaliser | 🟢 Débutant |
| `demo.py` | Démonstration interactive complète | 🟡 Intermédiaire |
| `test_analyst_helper.py` | Tests unitaires | 🟡 Intermédiaire |

### 📦 Package Python

#### `analyst_helper/__init__.py`
Point d'entrée du package, expose les classes principales :
- `FolderScanner`
- `AttachmentExtractor`
- `FileClassifier`
- `HTMLReporter`

#### `analyst_helper/core/scanner.py`
**Scanner d'arborescence de dossiers**
- Scanne récursivement les dossiers
- Collecte les métadonnées (taille, date, type)
- Calcule les statistiques
- Exporte en JSON/CSV
- Génère une vue arborescente

**Classes principales :**
- `FileInfo` : Informations sur un fichier
- `FolderScanner` : Scanner principal

#### `analyst_helper/core/extractor.py`
**Extracteur de pièces jointes**
- Supporte .msg (Outlook) et .eml (standard)
- Gère les emails imbriqués (récursif)
- Ignore les images intégrées
- Renommage intelligent des fichiers

**Classes principales :**
- `AttachmentInfo` : Informations sur une PJ
- `AttachmentExtractor` : Extracteur principal

#### `analyst_helper/core/classifier.py`
**Classificateur de fichiers**
- Classe les fichiers par catégories
- Copie dans des dossiers organisés
- Préserve ou aplatit la structure
- Génère des rapports de classification

**Classes principales :**
- `FileClassifier` : Classificateur principal

**Catégories par défaut :**
- Dossier technique : `.pdf`, `.dwg`, `.doc`, `.xls`, etc.
- Correspondance : `.msg`, `.eml`
- Autres fichiers : tout le reste

#### `analyst_helper/core/reporter.py`
**Générateur de rapports HTML**
- Rapports HTML interactifs
- Graphiques dynamiques (Chart.js)
- Tableaux triables/filtrables
- Export CSV intégré
- Design moderne et responsive

**Classes principales :**
- `HTMLReporter` : Générateur de rapports

**Fonctionnalités du rapport :**
- 📊 Cartes de statistiques
- 📈 4 graphiques interactifs
- 📋 Tableau avec recherche et filtres
- 📥 Export CSV
- 🎨 Design moderne avec animations

## 🔄 Flux de Travail Typique

```
1. Scanner
   └─> FolderScanner.scan()
       └─> Liste de FileInfo

2. Classifier (optionnel)
   └─> FileClassifier.classify_all()
       └─> Fichiers organisés par catégorie

3. Extraire (si emails)
   └─> AttachmentExtractor.extract_all()
       └─> Liste de AttachmentInfo

4. Rapporter
   └─> HTMLReporter.generate_report()
       └─> Rapport HTML interactif
```

## 📊 Formats de Sortie

| Format | Générateur | Usage |
|--------|-----------|-------|
| HTML | `HTMLReporter` | Visualisation interactive avec graphiques |
| CSV | `FolderScanner.export_to_csv()` | Import dans Excel, bases de données |
| JSON | `FolderScanner.export_to_json()` | Intégration avec d'autres outils |

## 🎯 Points d'Entrée

### Pour les utilisateurs finaux
```bash
python example_simple.py    # Le plus simple
python demo.py              # Complet et interactif
```

### Pour les développeurs
```python
from analyst_helper import FolderScanner, HTMLReporter

scanner = FolderScanner("/path")
files = scanner.scan()

reporter = HTMLReporter("output.html")
reporter.generate_report(files=files)
```

### Installation comme package
```bash
pip install -e .            # Installation en mode développement
analyst-helper              # Commande CLI (si configurée)
```

## 🧪 Tests

```bash
python test_analyst_helper.py
```

Tests effectués :
1. ✅ Import des modules
2. ✅ Scanner de dossiers
3. ✅ Classificateur
4. ✅ Générateur de rapports
5. ✅ Extracteur de PJ

## 📦 Dépendances

### Obligatoires
- Python 3.7+
- `extract-msg>=0.45.0` (pour fichiers .msg Outlook)

### Optionnelles
- Aucune ! Les graphiques utilisent Chart.js côté client

## 🚀 Prochaines Étapes

1. **Installation** : `pip install -r requirements.txt`
2. **Test** : `python test_analyst_helper.py`
3. **Essai** : `python example_simple.py`
4. **Lecture** : `QUICKSTART.md` et `README_ANALYST_HELPER.md`

## 💡 Architecture

- **Modulaire** : Chaque fonctionnalité est un module indépendant
- **Extensible** : Facile d'ajouter de nouvelles catégories, formats
- **Testable** : Modules séparés facilement testables
- **Simple** : API claire et intuitive

---

Pour plus d'informations, consultez `README_ANALYST_HELPER.md` 📖
