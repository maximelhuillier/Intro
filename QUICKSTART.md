# 🚀 Démarrage Rapide - AnalystHelper

Guide pour commencer en 5 minutes !

## 📋 Installation

### 1. Vérifier Python

```bash
python --version
# Devrait afficher Python 3.7 ou supérieur
```

Si Python n'est pas installé, téléchargez-le depuis [python.org](https://www.python.org/downloads/)

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

**Note:** Une seule dépendance nécessaire pour l'extraction d'emails (.msg)

## ⚡ Utilisation Ultra-Rapide

### Option 1 : Exemple Simple (Recommandé pour débuter)

```bash
python example_simple.py
```

Ce script va :
- ✅ Scanner le dossier actuel
- ✅ Générer un rapport HTML interactif (`mon_rapport.html`)
- ✅ Vous montrer les statistiques

**Personnaliser** : Éditez `example_simple.py` et modifiez les lignes :

```python
TARGET_FOLDER = "/chemin/vers/mon/dossier"  # Votre dossier
OUTPUT_REPORT = "mon_rapport_personnalisé.html"  # Nom du rapport
```

### Option 2 : Mode Démo Interactif

```bash
python demo.py
```

Ce script interactif vous guide à travers :
1. Scanner un dossier
2. Classifier les fichiers
3. Extraire les pièces jointes
4. Générer le rapport HTML

## 📊 Voir le Rapport

Ouvrez le fichier `.html` généré dans votre navigateur :

- **Windows** : Double-clic sur le fichier
- **Mac** : Double-clic ou `open mon_rapport.html`
- **Linux** : `xdg-open mon_rapport.html` ou Firefox/Chrome

Le rapport contient :
- 📈 Graphiques interactifs
- 📋 Tableau triable/filtrable
- 📥 Export CSV intégré
- 🔍 Recherche en temps réel

## 🎯 Cas d'Usage Typiques

### Analyser un dossier projet

```python
from analyst_helper import FolderScanner, HTMLReporter

scanner = FolderScanner("/chemin/vers/projet")
files = scanner.scan()

reporter = HTMLReporter("rapport_projet.html")
reporter.generate_report(files=files, title="Analyse Projet X")
```

### Classifier et organiser des fichiers

```python
from analyst_helper import FolderScanner, FileClassifier

scanner = FolderScanner("/chemin/source")
files = scanner.scan()

classifier = FileClassifier("/chemin/destination")
classifier.classify_all(files, copy=True)
```

### Extraire des pièces jointes d'emails

```python
from analyst_helper import FolderScanner, AttachmentExtractor

scanner = FolderScanner("/dossier/avec/emails")
files = scanner.scan()

extractor = AttachmentExtractor("/dossier/pj")
emails = [f.path for f in files if f.is_email]
attachments = extractor.extract_all(emails)
```

## 🔧 Personnalisation

### Changer les catégories de classification

```python
categories = {
    "Plans": ['.dwg', '.dxf'],
    "Documents": ['.pdf', '.doc', '.docx'],
    "Tableurs": ['.xls', '.xlsx'],
    "Emails": ['.msg', '.eml'],
    "Autres": []
}

classifier = FileClassifier("/sortie", categories=categories)
```

### Exclure certains dossiers

```python
scanner = FolderScanner("/racine")
files = scanner.scan(exclude_folders=[
    'node_modules',
    '.git',
    'temp',
    '__pycache__'
])
```

## 🆘 Problèmes Courants

### "Module 'extract-msg' not found"

```bash
pip install extract-msg
```

### Les liens ne fonctionnent pas dans le rapport

Utilisez Firefox ou configurez Chrome pour autoriser les liens `file://`

### Erreur de permissions

Sur Linux/Mac :

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Sur Windows :

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 📖 Documentation Complète

Pour plus d'informations, consultez :
- `README_ANALYST_HELPER.md` - Documentation complète
- `demo.py` - Exemple interactif complet
- `test_analyst_helper.py` - Tests unitaires

## 💡 Conseils Pro

1. **Performances** : Excluez les dossiers inutiles (`.git`, `node_modules`) pour accélérer le scan
2. **Rapport** : Le rapport HTML est standalone, vous pouvez le partager sans dépendances
3. **Export** : Utilisez le bouton "Export CSV" dans le rapport pour Excel
4. **Sécurité** : Vos données restent locales, rien n'est envoyé en ligne

## 🎉 C'est tout !

Vous êtes prêt à utiliser AnalystHelper. Bon analyse ! 📊
