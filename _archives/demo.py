#!/usr/bin/env python3
"""
Script de démonstration pour AnalystHelper
Montre comment scanner, classifier, extraire et générer des rapports
"""

import os
import sys
from pathlib import Path
from analyst_helper import FolderScanner, FileClassifier, AttachmentExtractor, HTMLReporter


def print_banner():
    """Affiche la bannière de bienvenue"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║              📊 AnalystHelper - Demo v1.0               ║
    ║                                                          ║
    ║    Outil d'aide à l'analyse de dossiers et documents    ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def get_folder_choice():
    """Demande à l'utilisateur de choisir un dossier"""
    print("\n📁 Choisissez le mode d'analyse :")
    print("  1. Analyser le dossier actuel")
    print("  2. Analyser un autre dossier")
    print("  3. Mode démo (créer des fichiers de test)")

    choice = input("\nVotre choix (1-3) : ").strip()

    if choice == "1":
        return os.getcwd()
    elif choice == "2":
        folder = input("Chemin du dossier à analyser : ").strip()
        if os.path.isdir(folder):
            return folder
        else:
            print("❌ Dossier invalide, utilisation du dossier actuel")
            return os.getcwd()
    elif choice == "3":
        return create_demo_files()
    else:
        print("❌ Choix invalide, utilisation du dossier actuel")
        return os.getcwd()


def create_demo_files():
    """Crée des fichiers de démonstration"""
    print("\n🎨 Création de fichiers de démonstration...")

    demo_dir = Path.cwd() / "demo_analyst_helper"
    demo_dir.mkdir(exist_ok=True)

    # Créer quelques fichiers de test
    files_to_create = [
        ("demo_dir/documents/rapport_2024.pdf", b"%PDF-1.4 Demo PDF"),
        ("demo_dir/documents/presentation.pptx", b"PK Demo PPTX"),
        ("demo_dir/plans/plan_A.dwg", b"AutoCAD Demo"),
        ("demo_dir/tableaux/budget.xlsx", b"PK Demo XLSX"),
        ("demo_dir/divers/notes.txt", b"Notes de demo"),
        ("demo_dir/images/photo.jpg", b"\xFF\xD8\xFF Demo JPG"),
    ]

    for filepath, content in files_to_create:
        full_path = demo_dir / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'wb') as f:
            f.write(content)

    print(f"✅ Fichiers de démonstration créés dans : {demo_dir}")
    return str(demo_dir)


def main():
    """Fonction principale"""
    print_banner()

    # Étape 1 : Choix du dossier
    target_folder = get_folder_choice()
    print(f"\n🎯 Dossier cible : {target_folder}")

    # Créer le dossier de sortie
    output_dir = Path(target_folder) / "analyst_output"
    output_dir.mkdir(exist_ok=True)
    print(f"📂 Dossier de sortie : {output_dir}")

    # Étape 2 : Scanner le dossier
    print("\n" + "="*60)
    print("ÉTAPE 1/4 : SCAN DE L'ARBORESCENCE")
    print("="*60)

    scanner = FolderScanner(target_folder)
    files = scanner.scan(exclude_folders=['analyst_output', 'node_modules', '.git'])

    # Afficher les statistiques
    print(f"\n📊 Statistiques :")
    print(f"   - Fichiers trouvés : {scanner.stats['total_files']}")
    print(f"   - Taille totale : {scanner.stats['total_size_mb']:.2f} MB")
    print(f"   - Emails : {scanner.stats['total_emails']}")
    print(f"   - Dossiers : {scanner.stats['total_folders']}")

    if scanner.stats['total_files'] == 0:
        print("\n⚠️  Aucun fichier trouvé. Fin du programme.")
        return

    # Afficher l'arborescence (max 3 niveaux)
    print("\n🌳 Arborescence (aperçu) :")
    print(scanner.get_tree_structure(max_depth=2))

    # Exporter en JSON et CSV
    scanner.export_to_json(str(output_dir / "fichiers.json"))
    scanner.export_to_csv(str(output_dir / "fichiers.csv"))

    # Étape 3 : Classification
    print("\n" + "="*60)
    print("ÉTAPE 2/4 : CLASSIFICATION DES FICHIERS")
    print("="*60)

    response = input("\nVoulez-vous copier et classifier les fichiers ? (o/N) : ").strip().lower()
    if response == 'o':
        classifier = FileClassifier(str(output_dir / "fichiers_classés"))
        classifier.classify_all(files, copy=True, preserve_structure=False)
        print("\n" + classifier.get_report())
    else:
        print("⏭️  Classification ignorée")

    # Étape 4 : Extraction des pièces jointes
    print("\n" + "="*60)
    print("ÉTAPE 3/4 : EXTRACTION DES PIÈCES JOINTES")
    print("="*60)

    attachments = []
    if scanner.stats['total_emails'] > 0:
        print(f"\n📧 {scanner.stats['total_emails']} email(s) détecté(s)")
        response = input("Voulez-vous extraire les pièces jointes ? (o/N) : ").strip().lower()

        if response == 'o':
            extractor = AttachmentExtractor(str(output_dir / "pièces_jointes"))
            email_files = [f.path for f in files if f.is_email]

            try:
                attachments = extractor.extract_all(email_files)
            except ImportError:
                print("\n⚠️  Module 'extract-msg' non installé.")
                print("   Installez-le avec : pip install extract-msg")
                print("   Extraction des pièces jointes ignorée.")
        else:
            print("⏭️  Extraction ignorée")
    else:
        print("\n📧 Aucun email détecté")

    # Étape 5 : Génération du rapport HTML
    print("\n" + "="*60)
    print("ÉTAPE 4/4 : GÉNÉRATION DU RAPPORT HTML")
    print("="*60)

    reporter = HTMLReporter(str(output_dir / "rapport_analyse.html"))
    reporter.generate_report(
        files=files,
        attachments=attachments,
        stats=scanner.stats,
        title=f"Rapport d'Analyse - {Path(target_folder).name}"
    )

    # Résumé final
    print("\n" + "="*60)
    print("✅ TRAITEMENT TERMINÉ")
    print("="*60)

    print(f"\n📁 Fichiers générés dans : {output_dir}")
    print("\n   📄 fichiers.csv           - Liste des fichiers (CSV)")
    print("   📄 fichiers.json          - Liste des fichiers (JSON)")
    print("   📄 rapport_analyse.html   - Rapport interactif")

    if response == 'o' and scanner.stats['total_emails'] > 0:
        print("   📁 pièces_jointes/        - PJ extraites")

    # Proposer d'ouvrir le rapport
    print("\n" + "="*60)
    response = input("\nVoulez-vous ouvrir le rapport HTML ? (o/N) : ").strip().lower()

    if response == 'o':
        import webbrowser
        report_path = output_dir / "rapport_analyse.html"
        webbrowser.open('file://' + str(report_path.resolve()))
        print("🌐 Rapport ouvert dans le navigateur")

    print("\n👋 Merci d'avoir utilisé AnalystHelper !")
    print("   Pour plus d'infos : voir README_ANALYST_HELPER.md\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
