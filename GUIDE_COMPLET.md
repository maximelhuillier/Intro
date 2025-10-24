# 📚 Guide Complet - AnalystHelper

## 🎯 Vue d'Ensemble

**AnalystHelper** est votre alternative moderne aux macros Excel VBA pour l'analyse de dossiers.

### ✅ Ce que fait AnalystHelper

| Fonctionnalité | Description | Équivalent VBA |
|----------------|-------------|----------------|
| 🗂️ Scanner | Parcourt récursivement les dossiers | ✅ Oui |
| 📊 Classifier | Organise les fichiers par type | ✅ Oui |
| 📎 Extraire | Extrait les PJ des emails (.msg, .eml) | ✅ Oui (seulement .msg) |
| 📈 Rapporter | Génère des rapports HTML interactifs | ⚠️ Limité (Excel statique) |
| 🔍 Analyser | Graphiques et statistiques | ⚠️ Limité |
| 💾 Exporter | CSV, JSON, HTML | ⚠️ Partiel |

### ⚡ Avantages vs VBA

```
VBA Excel                          AnalystHelper Python
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Excel + Outlook requis    →    🐍 Python uniquement
💻 Windows seulement          →    🌍 Multi-plateforme
🐌 Lent sur gros volumes      →    ⚡ Rapide et optimisé
📊 Tableau Excel statique     →    🎨 HTML interactif
🔧 Difficile à maintenir      →    ✨ Code moderne structuré
❌ Pas de graphiques          →    📈 4 graphiques dynamiques
```

---

## 🚀 Installation & Premier Lancement

### Étape 1 : Vérifier Python

```bash
python --version
```

✅ Attendu : `Python 3.7.x` ou supérieur
❌ Si non installé : [Télécharger Python](https://www.python.org/downloads/)

### Étape 2 : Installer les dépendances

```bash
cd /chemin/vers/analyst-helper
pip install -r requirements.txt
```

**Note :** Une seule dépendance (`extract-msg` pour les .msg)

### Étape 3 : Tester l'installation

```bash
python test_analyst_helper.py
```

Résultat attendu :
```
✅ PASS - Imports
✅ PASS - Scanner
✅ PASS - Classificateur
✅ PASS - Reporter
✅ PASS - Extracteur
🎉 Tous les tests sont passés !
```

---

## 📖 Modes d'Utilisation

### 🟢 Mode 1 : Exemple Simple (Recommandé pour débuter)

**Fichier :** `example_simple.py`
**Niveau :** Débutant
**Temps :** 2 minutes

```bash
python example_simple.py
```

**Personnalisation :**
```python
# Éditez example_simple.py
TARGET_FOLDER = "/mon/dossier"        # Votre dossier
OUTPUT_REPORT = "mon_rapport.html"    # Nom du rapport
```

**Résultat :** Génère `mon_rapport.html` avec :
- Statistiques
- Graphiques
- Liste des fichiers

---

### 🟡 Mode 2 : Démonstration Interactive

**Fichier :** `demo.py`
**Niveau :** Intermédiaire
**Temps :** 5-10 minutes

```bash
python demo.py
```

**Étapes interactives :**
1. Choix du dossier à analyser
2. Scan et affichage de l'arborescence
3. Classification des fichiers (optionnel)
4. Extraction des pièces jointes (optionnel)
5. Génération du rapport HTML

**Résultat :** Dossier `analyst_output/` avec :
```
analyst_output/
├── rapport_analyse.html      # Rapport principal
├── fichiers.csv              # Export CSV
├── fichiers.json             # Export JSON
├── fichiers_classés/         # Fichiers organisés
│   ├── Dossier technique/
│   ├── Correspondance/
│   └── Autres fichiers/
└── pièces_jointes/           # PJ extraites
```

---

### 🔵 Mode 3 : Utilisation Programmatique

**Niveau :** Avancé
**Pour :** Intégration dans vos scripts

#### Exemple 1 : Scanner Basique

```python
from analyst_helper import FolderScanner, HTMLReporter

# Scanner
scanner = FolderScanner("/chemin/dossier")
files = scanner.scan()

# Rapport
reporter = HTMLReporter("rapport.html")
reporter.generate_report(files=files, title="Mon Analyse")

print(f"✅ {len(files)} fichiers analysés")
```

#### Exemple 2 : Workflow Complet

```python
from analyst_helper import (
    FolderScanner,
    FileClassifier,
    AttachmentExtractor,
    HTMLReporter
)

# 1. Scanner
scanner = FolderScanner("/projet")
files = scanner.scan(exclude_folders=['.git', 'node_modules'])

# 2. Classifier
classifier = FileClassifier("/sortie")
classifier.classify_all(files, copy=True)

# 3. Extraire les PJ
extractor = AttachmentExtractor("/sortie/pj")
emails = [f.path for f in files if f.is_email]
attachments = extractor.extract_all(emails)

# 4. Rapport
reporter = HTMLReporter("rapport_final.html")
reporter.generate_report(
    files=files,
    attachments=attachments,
    title="Analyse Complète"
)
```

---

## 📊 Comprendre le Rapport HTML

### 📈 Section 1 : Cartes de Statistiques

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ 📁          │  │ 💾          │  │ 📧          │  │ 📎          │
│   1,234     │  │  567.8 MB   │  │     42      │  │    156      │
│  Fichiers   │  │   Taille    │  │   Emails    │  │  Pièces PJ  │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
```

### 📈 Section 2 : Graphiques Interactifs

**1. Répartition par type (Donut)**
- Dossier technique : 45%
- Correspondance : 30%
- Autres fichiers : 25%

**2. Top extensions (Barres)**
- .pdf : 234 fichiers
- .docx : 156 fichiers
- .xlsx : 98 fichiers

**3. Top 10 fichiers par taille (Barres horizontales)**
- projet_final.zip : 45.2 MB
- presentation.pptx : 23.1 MB
- ...

**4. Distribution temporelle (Ligne)**
- Fichiers créés/modifiés par mois

### 📋 Section 3 : Tableau Interactif

**Fonctionnalités :**
- ✅ **Recherche** en temps réel
- ✅ **Tri** par colonne (clic sur en-tête)
- ✅ **Filtre** par type
- ✅ **Export CSV** intégré
- ✅ **Liens** vers les fichiers (clic pour ouvrir)

**Colonnes :**
| Type | Nom | Extension | Taille | Modifié | Dossier |
|------|-----|-----------|--------|---------|---------|

---

## 🎨 Personnalisation Avancée

### Catégories Personnalisées

```python
categories = {
    "📐 Plans CAO": ['.dwg', '.dxf', '.rvt'],
    "📄 Documents": ['.pdf', '.doc', '.docx'],
    "📊 Tableurs": ['.xls', '.xlsx', '.csv'],
    "📧 Emails": ['.msg', '.eml'],
    "🗜️ Archives": ['.zip', '.rar', '.7z'],
    "🖼️ Images": ['.jpg', '.png', '.pdf'],
    "💼 Autres": []
}

classifier = FileClassifier("/sortie", categories=categories)
```

### Exclusions de Dossiers

```python
exclude = [
    # Dossiers système
    'System Volume Information',
    '$RECYCLE.BIN',

    # Dossiers développement
    'node_modules',
    '__pycache__',
    '.git',
    'venv',

    # Dossiers temporaires
    'temp',
    'tmp',
    'cache',

    # Dossiers de sortie
    'analyst_output',
]

scanner = FolderScanner("/racine")
files = scanner.scan(exclude_folders=exclude)
```

### Profondeur Maximale

```python
# Limiter la profondeur de scan
scanner = FolderScanner("/racine", max_depth=5)
```

---

## 🔧 Cas d'Usage Réels

### 📂 Cas 1 : Audit de Projet

**Besoin :** Inventorier tous les fichiers d'un projet
**Solution :**

```python
scanner = FolderScanner("/projet")
files = scanner.scan()

# Export pour Excel
scanner.export_to_csv("inventaire_projet.csv")

# Rapport pour l'équipe
reporter = HTMLReporter("inventaire.html")
reporter.generate_report(files=files, title="Inventaire Projet X")
```

### 📧 Cas 2 : Traitement d'Emails

**Besoin :** Extraire toutes les PJ d'un dossier d'emails
**Solution :**

```python
# Scanner les emails
scanner = FolderScanner("/emails")
files = scanner.scan()
emails = [f.path for f in files if f.is_email]

# Extraire les PJ
extractor = AttachmentExtractor("/pj_extraites")
attachments = extractor.extract_all(emails)

print(f"✅ {len(attachments)} pièces jointes extraites")
```

### 🗂️ Cas 3 : Migration de Données

**Besoin :** Réorganiser des fichiers avant archivage
**Solution :**

```python
# Scanner
scanner = FolderScanner("/source")
files = scanner.scan()

# Classifier et copier
classifier = FileClassifier("/archive")
classifier.classify_all(files, copy=True, preserve_structure=False)

# Rapport de migration
print(classifier.get_report())
```

### 📊 Cas 4 : Analyse d'Occupation Disque

**Besoin :** Identifier les gros fichiers
**Solution :**

```python
scanner = FolderScanner("/donnees")
files = scanner.scan()

# Trier par taille
files_sorted = sorted(files, key=lambda f: f.size_mb, reverse=True)

# Top 20
print("🏆 Top 20 des plus gros fichiers :")
for i, f in enumerate(files_sorted[:20], 1):
    print(f"{i:2}. {f.name:50} {f.size_mb:8.2f} MB")
```

---

## 🐛 Résolution de Problèmes

### ❌ Erreur : "Module 'extract-msg' not found"

**Cause :** Dépendance manquante
**Solution :**
```bash
pip install extract-msg
```

### ❌ Erreur : "Permission denied"

**Cause :** Pas les droits d'accès
**Solution :**

**Sur Linux/Mac :**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Sur Windows :**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### ❌ Les liens ne fonctionnent pas dans le rapport

**Cause :** Restrictions du navigateur pour `file://`
**Solution :**
- ✅ Utilisez **Firefox** (recommandé)
- ⚠️ Chrome nécessite des paramètres spéciaux
- ✅ Edge fonctionne généralement

### ❌ Scan trop lent

**Cause :** Trop de fichiers ou dossiers système
**Solution :**
```python
# Exclure les gros dossiers inutiles
scanner.scan(exclude_folders=[
    'node_modules',      # Énorme
    '.git',              # Inutile
    'System Volume Info' # Système
])
```

---

## 📚 Documentation Complémentaire

| Fichier | Contenu | Quand le lire |
|---------|---------|---------------|
| `README_ANALYST_HELPER.md` | Documentation complète | Pour tout savoir |
| `QUICKSTART.md` | Démarrage rapide | Pour commencer vite |
| `STRUCTURE.md` | Architecture du projet | Pour les développeurs |
| `CHANGELOG.md` | Historique des versions | Pour suivre l'évolution |
| Ce fichier | Guide complet | Pour une vue d'ensemble |

---

## 🎓 Conseils Pro

### 💡 Performance

1. **Exclure les dossiers inutiles** : Gagne 50-90% du temps
2. **Limiter la profondeur** : Si vous connaissez la structure
3. **Traiter par lots** : Pour très gros volumes (>100k fichiers)

### 💡 Sécurité

1. **Traitement local** : Rien n'est envoyé en ligne
2. **Copie, pas déplacement** : Fichiers originaux préservés
3. **Logs d'erreurs** : Activez pour debug

### 💡 Partage

1. **Rapport HTML standalone** : Peut être partagé sans dépendances
2. **Export CSV** : Pour Excel ou bases de données
3. **Export JSON** : Pour intégration avec d'autres outils

---

## 🚀 Prochaines Étapes

1. ✅ Installer : `pip install -r requirements.txt`
2. ✅ Tester : `python test_analyst_helper.py`
3. ✅ Essayer : `python example_simple.py`
4. ✅ Explorer : Lire `QUICKSTART.md`
5. ✅ Utiliser : Adapter à vos besoins

---

## 💬 Support

- 🐛 **Bug ?** → Créer une issue GitHub
- 💡 **Idée ?** → Proposer une fonctionnalité
- ❓ **Question ?** → Consulter la documentation

---

**Fait avec ❤️ pour gagner du temps et simplifier l'analyse de dossiers**

🎉 Bon usage d'AnalystHelper !
