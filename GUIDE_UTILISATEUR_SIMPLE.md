# 📖 Guide Utilisateur Simple - AnalystHelper

## 👥 Pour vos Collègues qui ne Connaissent pas Python

Ce guide explique comment utiliser **AnalystHelper** avec l'interface graphique, **sans connaître Python**.

---

## 🎯 Vous avez 3 Options

### 🟢 Option 1 : Interface Graphique (RECOMMANDÉE)

**Avantages :** Facile, aucune commande à taper
**Prérequis :** Python doit être installé

[👉 Cliquez ici](#option-1-interface-graphique)

---

### 🟡 Option 2 : Exécutable Windows (.exe)

**Avantages :** Pas besoin de Python, double-clic et c'est parti
**Limitation :** Windows uniquement

[👉 Cliquez ici](#option-2-exécutable-windows-exe)

---

### 🔵 Option 3 : Lanceurs Automatiques

**Avantages :** Un seul clic, automatique
**Prérequis :** Python doit être installé

[👉 Cliquez ici](#option-3-lanceurs-automatiques)

---

# Option 1 : Interface Graphique

## 📋 Prérequis (À faire UNE SEULE FOIS)

### Étape 1 : Installer Python

**Windows :**
1. Télécharger Python : https://www.python.org/downloads/
2. **IMPORTANT** : Cocher "Add Python to PATH" pendant l'installation
3. Cliquer sur "Install Now"

**Mac :**
```bash
# Ouvrir Terminal et taper :
brew install python3
```

**Linux :**
```bash
# Ouvrir Terminal et taper :
sudo apt install python3 python3-pip
```

### Étape 2 : Installer les Dépendances

**Windows :**
1. Ouvrir l'Invite de commandes (cmd)
2. Naviguer vers le dossier AnalystHelper
3. Taper :
```bash
pip install -r requirements.txt
```

**Mac/Linux :**
```bash
pip3 install -r requirements.txt
```

---

## 🚀 Utilisation (Chaque Fois)

### Lancer l'Interface

**Windows :**
1. Double-cliquer sur `LANCER_INTERFACE.bat`

**Ou manuellement :**
```bash
python analyst_helper_gui.py
```

**Mac/Linux :**
```bash
./lancer_interface.sh
```

**Ou manuellement :**
```bash
python3 analyst_helper_gui.py
```

---

## 📸 Utilisation de l'Interface

### Fenêtre Principale

```
┌─────────────────────────────────────────────────────┐
│         📊 AnalystHelper                            │
│     Analysez vos dossiers en quelques clics         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📁 Dossier à analyser                              │
│  [C:\Mon\Dossier\Projet    ]  [📂 Parcourir]       │
│                                                     │
│  ⚙️ Options                                         │
│  ☑ Classifier les fichiers par type                │
│  ☑ Extraire les pièces jointes des emails          │
│  🚫 Dossiers à exclure : .git, node_modules         │
│                                                     │
│  💾 Dossier de sortie                               │
│  [C:\Users\Nom\AnalystHelper_Output]  [📂 Changer] │
│                                                     │
│          [🚀 Lancer l'Analyse]                      │
│                                                     │
│  📊 Progression                                      │
│  [████████░░░░░░░░░░░░░░░░░░]                       │
│  Scan en cours...                                   │
│                                                     │
│  [📄 Ouvrir le Rapport HTML] [📂 Ouvrir le Dossier]│
└─────────────────────────────────────────────────────┘
```

### Étapes d'Utilisation

#### 1️⃣ Sélectionner le Dossier
- Cliquer sur **📂 Parcourir**
- Choisir le dossier à analyser
- Cliquer sur **Sélectionner**

#### 2️⃣ Configurer les Options

**Options disponibles :**

- ☑ **Classifier les fichiers** : Organise les fichiers en 3 catégories
  - Dossier technique (PDF, DWG, DOC, XLS)
  - Correspondance (MSG, EML)
  - Autres fichiers

- ☑ **Extraire les pièces jointes** : Extrait les PJ des emails
  - Supporte .msg (Outlook) et .eml
  - Gère les emails imbriqués

- **Dossiers à exclure** : Ajoutez les dossiers à ignorer
  - Par défaut : `.git, node_modules, __pycache__, temp`
  - Ajoutez d'autres dossiers séparés par des virgules

#### 3️⃣ Choisir le Dossier de Sortie (Optionnel)

Par défaut : `C:\Users\VotreNom\AnalystHelper_Output`

Pour changer :
- Cliquer sur **📂 Changer**
- Sélectionner un autre dossier

#### 4️⃣ Lancer l'Analyse

- Cliquer sur **🚀 Lancer l'Analyse**
- Une fenêtre de confirmation apparaît
- Cliquer sur **Oui**

#### 5️⃣ Suivre la Progression

La fenêtre de progression affiche :
- `ÉTAPE 1/4 : SCAN DU DOSSIER`
- `ÉTAPE 2/4 : CLASSIFICATION DES FICHIERS`
- `ÉTAPE 3/4 : EXTRACTION DES PIÈCES JOINTES`
- `ÉTAPE 4/4 : GÉNÉRATION DU RAPPORT HTML`

#### 6️⃣ Consulter les Résultats

Quand l'analyse est terminée :
- Cliquer sur **📄 Ouvrir le Rapport HTML**
- Le rapport s'ouvre dans votre navigateur

**Ou :**
- Cliquer sur **📂 Ouvrir le Dossier**
- Explorer les fichiers générés

---

## 📂 Résultats Générés

Dans le dossier de sortie, vous trouverez :

```
AnalystHelper_Output/
├── rapport_analyse.html      ⭐ Rapport principal (OUVRIR CE FICHIER)
├── fichiers.csv              📊 Liste des fichiers (Excel)
├── fichiers.json             📄 Données brutes (JSON)
│
├── fichiers_classés/         📁 Fichiers organisés
│   ├── Dossier technique/
│   ├── Correspondance/
│   └── Autres fichiers/
│
└── pièces_jointes/           📎 PJ extraites des emails
```

---

## 🎨 Utilisation du Rapport HTML

### Ouvrir le Rapport

1. Double-cliquer sur `rapport_analyse.html`
2. Le rapport s'ouvre dans votre navigateur par défaut

### Fonctionnalités du Rapport

#### 📊 Statistiques
En haut du rapport :
- 📁 Nombre de fichiers
- 💾 Taille totale
- 📧 Nombre d'emails
- 📎 Pièces jointes

#### 📈 Graphiques Interactifs
- **Donut** : Répartition par type
- **Barres** : Top extensions
- **Taille** : Plus gros fichiers
- **Temps** : Distribution par mois

*Survolez les graphiques pour voir les détails*

#### 📋 Tableau de Fichiers

**Recherche :**
- Tapez dans la barre de recherche
- Les résultats s'affichent instantanément

**Tri :**
- Cliquez sur les en-têtes de colonnes
- Exemple : Cliquer sur "Taille" pour trier par taille

**Filtrage :**
- Utilisez le menu déroulant "Type"
- Filtrer par : Dossier technique, Correspondance, Autres

**Export CSV :**
- Cliquez sur **📥 Exporter CSV**
- Ouvrez le fichier dans Excel

---

# Option 2 : Exécutable Windows (.exe)

## 🏗️ Créer l'Exécutable (À faire UNE FOIS)

### Pour la Personne qui Crée l'Exe

1. Ouvrir l'Invite de commandes
2. Naviguer vers le dossier AnalystHelper
3. Taper :
```bash
python build_exe.py
```

4. Attendre la création (2-5 minutes)
5. L'exécutable sera dans : `dist/AnalystHelper.exe`

---

## 📤 Distribuer l'Exécutable

### Pour Distribuer à vos Collègues

1. Copier le fichier `dist/AnalystHelper.exe`
2. Envoyer par email ou mettre sur un serveur partagé

**Vos collègues n'auront PAS besoin de Python !**

---

## 🚀 Utiliser l'Exécutable

### Pour vos Collègues

1. Double-cliquer sur `AnalystHelper.exe`
2. L'interface graphique s'ouvre
3. Suivre les mêmes étapes que l'Option 1

**C'est tout ! Aucune installation nécessaire.**

---

# Option 3 : Lanceurs Automatiques

## 🚀 Windows

Double-cliquer sur : `LANCER_INTERFACE.bat`

## 🚀 Mac/Linux

Dans le Terminal :
```bash
./lancer_interface.sh
```

---

## ❓ Questions Fréquentes

### "Python n'est pas reconnu comme commande"

**Solution :** Python n'est pas dans le PATH
1. Réinstallez Python
2. **Cochez** "Add Python to PATH"

### "ModuleNotFoundError: No module named 'analyst_helper'"

**Solution :** Les dépendances ne sont pas installées
```bash
pip install -r requirements.txt
```

### "Permission denied" (Mac/Linux)

**Solution :** Rendre le script exécutable
```bash
chmod +x lancer_interface.sh
```

### "extract-msg not found"

**Solution :** Module manquant pour les .msg
```bash
pip install extract-msg
```

### Le rapport ne s'ouvre pas automatiquement

**Solution :**
1. Aller dans le dossier de sortie
2. Double-cliquer sur `rapport_analyse.html`

### Les liens dans le rapport ne fonctionnent pas

**Solution :**
- Utilisez **Firefox** (recommandé)
- Ou configurez Chrome pour autoriser `file://`

---

## 📧 Support

### Problème avec l'Interface ?

1. Vérifier que Python est installé
2. Vérifier que les dépendances sont installées
3. Consulter les messages d'erreur dans la fenêtre

### Erreur lors de l'Analyse ?

Consultez la fenêtre de progression :
- Les messages en rouge indiquent les erreurs
- Les messages en vert indiquent les succès

---

## 💡 Conseils d'Utilisation

### ✅ Bonnes Pratiques

1. **Exclure les dossiers inutiles**
   - Ajoutez `.git, node_modules, temp` pour accélérer

2. **Vérifier le dossier de sortie**
   - Utilisez un dossier dédié (pas le Bureau)

3. **Fermer les fichiers**
   - Fermez Excel/Outlook avant l'analyse

4. **Sauvegarder le rapport**
   - Le rapport HTML peut être partagé sans dépendances

### ⚠️ À Éviter

1. ❌ Ne pas analyser des disques système entiers (C:\)
2. ❌ Ne pas fermer l'interface pendant l'analyse
3. ❌ Ne pas analyser des dossiers réseau lents

---

## 🎓 Tutoriel Vidéo (Si Disponible)

*À créer : Enregistrez une vidéo de 3 minutes montrant :*
1. Lancer l'interface
2. Sélectionner un dossier
3. Cliquer sur "Lancer l'Analyse"
4. Ouvrir le rapport

---

## 📝 Checklist de Démarrage

Pour vos collègues, imprimez cette checklist :

```
☐ 1. Python est installé (avec PATH)
☐ 2. Dépendances installées (pip install -r requirements.txt)
☐ 3. Double-clic sur LANCER_INTERFACE.bat (Windows)
☐ 4. Sélectionner le dossier à analyser
☐ 5. Configurer les options
☐ 6. Cliquer sur "Lancer l'Analyse"
☐ 7. Attendre la fin (barre de progression)
☐ 8. Cliquer sur "Ouvrir le Rapport HTML"
☐ 9. Consulter les statistiques et graphiques
☐ 10. Exporter en CSV si besoin
```

---

## 🎉 Résumé pour vos Collègues

### En 3 Phrases

1. **Double-cliquez** sur `LANCER_INTERFACE.bat` (Windows) ou `AnalystHelper.exe`
2. **Sélectionnez** le dossier à analyser et cliquez sur "Lancer l'Analyse"
3. **Ouvrez** le rapport HTML généré pour voir les résultats

**C'est tout ! Pas besoin de connaître Python 😊**

---

**💬 Besoin d'aide ? Demandez à la personne qui a configuré AnalystHelper !**
