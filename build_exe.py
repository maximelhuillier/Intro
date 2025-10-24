#!/usr/bin/env python3
"""
Script pour créer un exécutable Windows (.exe) d'AnalystHelper
Utilise PyInstaller pour créer un fichier .exe standalone
"""

import os
import sys
import subprocess
from pathlib import Path


def check_pyinstaller():
    """Vérifie si PyInstaller est installé"""
    try:
        import PyInstaller
        print("✅ PyInstaller est installé")
        return True
    except ImportError:
        print("❌ PyInstaller n'est pas installé")
        print("\n📦 Installation de PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installé avec succès")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'installation : {e}")
            print("\nInstallez manuellement avec : pip install pyinstaller")
            return False


def create_exe():
    """Crée l'exécutable avec PyInstaller"""
    print("\n🔨 Création de l'exécutable...\n")

    # Paramètres PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                          # Un seul fichier exe
        "--windowed",                         # Pas de console (interface graphique)
        "--name=AnalystHelper",               # Nom de l'exe
        "--icon=NONE",                        # Pas d'icône (ou spécifier un .ico)
        "--clean",                            # Nettoyer avant de build
        "--add-data=analyst_helper;analyst_helper",  # Inclure le package
        "analyst_helper_gui.py"               # Script principal
    ]

    # Sur Windows, le séparateur est différent
    if sys.platform == 'win32':
        cmd[6] = "--add-data=analyst_helper;analyst_helper"
    else:
        cmd[6] = "--add-data=analyst_helper:analyst_helper"

    try:
        result = subprocess.run(cmd, check=True)

        print("\n" + "=" * 60)
        print("✅ EXÉCUTABLE CRÉÉ AVEC SUCCÈS")
        print("=" * 60)
        print("\n📂 L'exécutable se trouve dans : dist/AnalystHelper.exe")
        print("\n💡 Vous pouvez distribuer ce fichier .exe à vos collègues.")
        print("   Ils n'auront pas besoin de Python installé !")
        print("\n📝 Instructions pour vos collègues :")
        print("   1. Double-cliquer sur AnalystHelper.exe")
        print("   2. Sélectionner le dossier à analyser")
        print("   3. Cliquer sur 'Lancer l'Analyse'")
        print("   4. Ouvrir le rapport HTML généré")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors de la création : {e}")
        return False
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        return False

    return True


def main():
    """Fonction principale"""
    print("=" * 60)
    print("🏗️  CRÉATION D'UN EXÉCUTABLE WINDOWS (.exe)")
    print("=" * 60)
    print("\nCet outil va créer un fichier .exe que vos collègues")
    print("pourront utiliser SANS avoir Python installé !")

    # Vérifier PyInstaller
    if not check_pyinstaller():
        return

    # Vérifier que le fichier GUI existe
    if not Path("analyst_helper_gui.py").exists():
        print("\n❌ Fichier analyst_helper_gui.py introuvable")
        return

    # Créer l'exe
    if create_exe():
        print("\n✅ Terminé !")
    else:
        print("\n❌ Échec de la création")


if __name__ == "__main__":
    main()
