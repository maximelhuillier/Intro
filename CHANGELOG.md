# 📝 Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.0.0] - 2024-10-24

### 🎉 Version Initiale

#### ✨ Ajouté
- **Scanner d'arborescence** (`core/scanner.py`)
  - Scan récursif de dossiers avec métadonnées complètes
  - Export JSON et CSV
  - Génération d'arborescence textuelle
  - Statistiques détaillées (taille, types, extensions)
  - Support de profondeur maximale configurable

- **Extracteur de pièces jointes** (`core/extractor.py`)
  - Support des fichiers .msg (Outlook) et .eml (standard)
  - Extraction récursive des emails imbriqués
  - Filtrage automatique des images intégrées
  - Renommage intelligent des fichiers
  - Gestion des conflits de noms

- **Classificateur de fichiers** (`core/classifier.py`)
  - Classification automatique par type de fichier
  - 3 catégories par défaut : Dossier technique, Correspondance, Autres
  - Catégories personnalisables
  - Option de préservation de structure
  - Rapports de classification détaillés

- **Générateur de rapports HTML** (`core/reporter.py`)
  - Rapports HTML interactifs modernes
  - 4 graphiques dynamiques (Chart.js) :
    - Répartition par type (donut)
    - Top extensions (barres)
    - Top 10 fichiers par taille (barres horizontales)
    - Distribution temporelle (ligne)
  - Tableau triable et filtrable
  - Recherche en temps réel
  - Export CSV intégré
  - Design responsive et moderne
  - Animations et interactions

- **Scripts d'exemple**
  - `demo.py` : Démonstration interactive complète
  - `example_simple.py` : Exemple minimal à personnaliser
  - `test_analyst_helper.py` : Suite de tests unitaires

- **Documentation**
  - `README_ANALYST_HELPER.md` : Documentation complète
  - `QUICKSTART.md` : Guide de démarrage rapide
  - `STRUCTURE.md` : Structure du projet
  - Commentaires de code détaillés

- **Configuration**
  - `requirements.txt` : Dépendances minimales
  - `setup.py` : Installation comme package
  - `.gitignore` : Fichiers à ignorer
  - `LICENSE` : Licence MIT

#### 🎯 Fonctionnalités Clés
- ✅ 100% Python pur (pas de dépendances lourdes)
- ✅ Multi-plateforme (Windows, Mac, Linux)
- ✅ Traitement local (sécurité et confidentialité)
- ✅ Rapports standalone (partageable sans dépendances)
- ✅ Performance optimisée
- ✅ Gestion d'erreurs robuste

#### 📊 Statistiques
- 5 modules principaux
- 3 scripts d'exemple
- 4 fichiers de documentation
- ~1500 lignes de code
- 5/5 tests passés

---

## [Futur] - Roadmap

### 🔮 Prévu pour v1.1.0
- [ ] Support des archives .pst (Outlook)
- [ ] Détection de doublons par hash MD5/SHA256
- [ ] Interface graphique (GUI) avec Tkinter ou PyQt
- [ ] Export Excel natif (sans passer par CSV)

### 🔮 Prévu pour v1.2.0
- [ ] OCR sur PDF scannés
- [ ] Analyse de contenu avec NLP
- [ ] Comparaison de deux dossiers
- [ ] Détection de fichiers sensibles

### 🔮 Prévu pour v2.0.0
- [ ] Application web (Flask/FastAPI + React)
- [ ] Base de données pour historique
- [ ] Planification de tâches (cron)
- [ ] API REST

---

## Types de Changements

- `✨ Ajouté` : Nouvelles fonctionnalités
- `🔧 Modifié` : Changements de fonctionnalités existantes
- `🗑️ Déprécié` : Fonctionnalités qui seront supprimées
- `🔥 Supprimé` : Fonctionnalités supprimées
- `🐛 Corrigé` : Corrections de bugs
- `🔒 Sécurité` : Corrections de vulnérabilités

---

[1.0.0]: https://github.com/votre-username/analyst-helper/releases/tag/v1.0.0
