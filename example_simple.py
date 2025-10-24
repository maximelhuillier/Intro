#!/usr/bin/env python3
"""
Exemple simple d'utilisation d'AnalystHelper
Pour les utilisateurs qui veulent un script rapide à personnaliser
"""

from analyst_helper import FolderScanner, HTMLReporter

# ============================================
# CONFIGURATION - Modifiez ces valeurs
# ============================================

# Dossier à analyser
TARGET_FOLDER = "."  # Dossier actuel, ou spécifiez un chemin : "/chemin/vers/dossier"

# Fichier de sortie pour le rapport
OUTPUT_REPORT = "mon_rapport.html"

# Dossiers à exclure du scan
EXCLUDE_FOLDERS = [
    "node_modules",
    ".git",
    "__pycache__",
    "venv",
    "analyst_output"
]

# ============================================
# EXÉCUTION
# ============================================

def main():
    print("🔍 AnalystHelper - Exemple Simple\n")

    # 1. Scanner le dossier
    print(f"📁 Scan du dossier : {TARGET_FOLDER}")
    scanner = FolderScanner(TARGET_FOLDER)
    files = scanner.scan(exclude_folders=EXCLUDE_FOLDERS)

    # 2. Afficher les statistiques
    print(f"\n✅ Scan terminé :")
    print(f"   - {scanner.stats['total_files']} fichiers trouvés")
    print(f"   - {scanner.stats['total_size_mb']:.2f} MB")

    # Afficher la répartition par type
    print("\n📊 Répartition par type :")
    for file_type, count in scanner.stats['by_type'].items():
        print(f"   - {file_type}: {count}")

    # 3. Générer le rapport HTML
    print(f"\n📄 Génération du rapport : {OUTPUT_REPORT}")
    reporter = HTMLReporter(OUTPUT_REPORT)
    reporter.generate_report(
        files=files,
        stats=scanner.stats,
        title="Mon Rapport d'Analyse"
    )

    print(f"\n✅ Terminé ! Ouvrez {OUTPUT_REPORT} dans votre navigateur\n")


if __name__ == "__main__":
    main()
