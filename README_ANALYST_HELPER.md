# 📊 AnalystHelper

> Outil Python moderne pour l'analyse de dossiers, l'extraction de pièces jointes et la génération de rapports interactifs

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 Objectif

**AnalystHelper** est une alternative moderne et indépendante aux macros Excel pour aider les analystes à :

- ✅ **Visualiser** facilement l'arborescence de dossiers
- ✅ **Extraire** automatiquement les pièces jointes des emails (.msg, .eml)
- ✅ **Lister** rapidement tous les documents avec métadonnées
- ✅ **Générer** des rapports HTML interactifs avec graphiques
- ✅ **Classifier** les fichiers par catégories (Dossier technique, Correspondance, Autres)
- ✅ **Exporter** les données en CSV/JSON

## 🚀 Avantages par rapport à Excel/VBA

| Critère | Excel/VBA | AnalystHelper |
|---------|-----------|---------------|
| **Dépendances** | Excel + Outlook requis | Python uniquement |
| **Portabilité** | Windows uniquement | Windows, Mac, Linux |
| **Performance** | Ralentissements sur gros volumes | Optimisé et rapide |
| **Rapports** | Tableau Excel statique | HTML interactif avec graphiques |
| **Maintenance** | Code VBA difficile à maintenir | Python moderne et structuré |
| **Visualisation** | Limitée | Graphiques interactifs (Chart.js) |

## 📦 Installation

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

**Note:** Une seule dépendance nécessaire : `extract-msg` pour les fichiers .msg d'Outlook

## 🎬 Utilisation rapide

### 1️⃣ Scanner un dossier

```python
from analyst_helper import FolderScanner

# Scanner un dossier
scanner = FolderScanner("/chemin/vers/dossier")
files = scanner.scan()

# Afficher l'arborescence
print(scanner.get_tree_structure())

# Exporter les résultats
scanner.export_to_csv("fichiers.csv")
scanner.export_to_json("fichiers.json")
```

### 2️⃣ Classifier les fichiers

```python
from analyst_helper import FileClassifier

# Classifier et organiser les fichiers
classifier = FileClassifier("/chemin/sortie")
classifier.classify_all(files, copy=True)

# Afficher le rapport
print(classifier.get_report())
```

### 3️⃣ Extraire les pièces jointes

```python
from analyst_helper import AttachmentExtractor

# Extraire les PJ des emails
extractor = AttachmentExtractor("/chemin/sortie/Pièces_jointes")

# Liste des emails
emails = [f.path for f in files if f.is_email]

# Extraction
attachments = extractor.extract_all(emails)
```

### 4️⃣ Générer un rapport HTML

```python
from analyst_helper import HTMLReporter

# Créer le rapport
reporter = HTMLReporter("rapport.html")
reporter.generate_report(
    files=files,
    attachments=attachments,
    title="Rapport d'Analyse - Dossier X"
)

# Le fichier rapport.html est généré avec :
# - Statistiques (nombre de fichiers, taille totale, etc.)
# - Graphiques interactifs (répartition par type, taille, date)
# - Tableau triable et filtrable
# - Export CSV intégré
```

## 📁 Structure du projet

```
analyst_helper/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── scanner.py       # Scan d'arborescence
│   ├── extractor.py     # Extraction de PJ
│   ├── classifier.py    # Classification de fichiers
│   └── reporter.py      # Génération de rapports HTML
└── utils/
    └── __init__.py

requirements.txt         # Dépendances Python
README_ANALYST_HELPER.md # Ce fichier
demo.py                  # Script de démonstration
```

## 🎨 Fonctionnalités du rapport HTML

Le rapport HTML généré contient :

### 📊 Statistiques en temps réel
- Nombre total de fichiers
- Taille totale (MB)
- Nombre d'emails
- Nombre de pièces jointes extraites

### 📈 Graphiques interactifs
- **Répartition par type** (Doughnut chart)
- **Top extensions** (Bar chart)
- **Top 10 fichiers par taille** (Horizontal bar)
- **Distribution temporelle** (Line chart)

### 📋 Tableau interactif
- **Tri** par colonne (clic sur en-tête)
- **Filtrage** en temps réel (recherche + type)
- **Export CSV** intégré
- **Liens** vers les fichiers

### 🎯 Navigation
- Interface responsive (mobile-friendly)
- Design moderne avec dégradés
- Animations au survol
- Badge colorés par catégorie

## 🔧 Configuration avancée

### Personnaliser les catégories

```python
categories = {
    "Plans": ['.dwg', '.dxf', '.pdf'],
    "Bureautique": ['.doc', '.docx', '.xls', '.xlsx'],
    "Emails": ['.msg', '.eml'],
    "Archives": ['.zip', '.rar', '.7z'],
    "Autres": []  # Catch-all
}

classifier = FileClassifier("/sortie", categories=categories)
```

### Exclure des dossiers

```python
scanner = FolderScanner("/racine")
files = scanner.scan(exclude_folders=['node_modules', '.git', 'temp'])
```

### Limite de récursion

```python
scanner = FolderScanner("/racine", max_depth=10)
```

## 📝 Exemple complet

Voir le fichier `demo.py` pour un exemple complet d'utilisation.

```bash
python demo.py
```

## 🛠️ Cas d'usage

### Analyse de dossiers projet
- Scanner tous les fichiers d'un projet
- Classifier par type (technique, admin, etc.)
- Générer un rapport pour l'équipe

### Traitement d'emails
- Extraire automatiquement toutes les PJ
- Gérer les emails imbriqués
- Créer une base de documents

### Audit de documents
- Inventorier tous les fichiers
- Identifier les doublons
- Visualiser la distribution

### Migration de données
- Préparer des fichiers pour archivage
- Réorganiser par catégories
- Exporter les métadonnées

## 🔐 Sécurité et confidentialité

- ✅ **Exécution locale** : Aucune donnée n'est envoyée en ligne
- ✅ **Pas de modification** : Les fichiers originaux sont préservés (copie uniquement)
- ✅ **Open source** : Code transparent et auditable
- ✅ **Pas de dépendances suspectes** : Seulement `extract-msg`

## 🐛 Résolution de problèmes

### Erreur "extract-msg not found"

```bash
pip install extract-msg
```

### Erreur de permissions

Sur Linux/Mac, vous devrez peut-être utiliser `sudo` ou un environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Les liens dans le rapport ne fonctionnent pas

Les liens `file:///` fonctionnent mieux dans certains navigateurs. Essayez :
- Firefox (recommandé)
- Chrome (peut nécessiter des paramètres)
- Edge

## 🚀 Roadmap

- [ ] Support des emails .pst (archives Outlook)
- [ ] Détection de doublons (hash)
- [ ] OCR sur les PDF scannés
- [ ] Interface graphique (GUI)
- [ ] Export Excel natif
- [ ] Comparaison de dossiers
- [ ] Analyse de contenu (NLP)

## 📄 Licence

MIT License - Libre d'utilisation et de modification

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📧 Contact

Pour toute question ou suggestion, créez une issue sur GitHub.

---

**Fait avec ❤️ pour les analystes qui veulent gagner du temps**
