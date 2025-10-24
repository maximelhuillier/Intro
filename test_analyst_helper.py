#!/usr/bin/env python3
"""
Tests rapides pour vérifier que AnalystHelper fonctionne
"""

import os
import tempfile
from pathlib import Path


def test_imports():
    """Test 1 : Vérifier que tous les modules peuvent être importés"""
    print("Test 1 : Import des modules...")
    try:
        from analyst_helper import FolderScanner, FileClassifier, HTMLReporter
        print("   ✅ Imports réussis")
        return True
    except ImportError as e:
        print(f"   ❌ Erreur d'import : {e}")
        return False


def test_scanner():
    """Test 2 : Tester le scanner de dossiers"""
    print("\nTest 2 : Scanner de dossiers...")
    try:
        from analyst_helper import FolderScanner

        # Créer un dossier temporaire avec des fichiers
        with tempfile.TemporaryDirectory() as tmpdir:
            # Créer quelques fichiers de test
            (Path(tmpdir) / "test1.pdf").write_text("test")
            (Path(tmpdir) / "test2.txt").write_text("test")

            # Scanner
            scanner = FolderScanner(tmpdir)
            files = scanner.scan()

            if len(files) >= 2:
                print(f"   ✅ Scanner OK - {len(files)} fichiers trouvés")
                return True
            else:
                print(f"   ❌ Scanner : {len(files)} fichiers trouvés (attendu >= 2)")
                return False

    except Exception as e:
        print(f"   ❌ Erreur scanner : {e}")
        return False


def test_classifier():
    """Test 3 : Tester le classificateur"""
    print("\nTest 3 : Classificateur...")
    try:
        from analyst_helper import FolderScanner, FileClassifier

        with tempfile.TemporaryDirectory() as tmpdir:
            # Créer des fichiers
            (Path(tmpdir) / "doc.pdf").write_text("test")
            (Path(tmpdir) / "data.xlsx").write_text("test")

            # Scanner
            scanner = FolderScanner(tmpdir)
            files = scanner.scan()

            # Classifier
            output_dir = Path(tmpdir) / "output"
            classifier = FileClassifier(str(output_dir))
            results = classifier.classify_all(files, copy=True)

            if len(results) >= 2:
                print(f"   ✅ Classificateur OK - {len(results)} fichiers classifiés")
                return True
            else:
                print(f"   ❌ Classificateur : {len(results)} fichiers (attendu >= 2)")
                return False

    except Exception as e:
        print(f"   ❌ Erreur classificateur : {e}")
        return False


def test_reporter():
    """Test 4 : Tester le générateur de rapports"""
    print("\nTest 4 : Générateur de rapports HTML...")
    try:
        from analyst_helper import FolderScanner, HTMLReporter

        with tempfile.TemporaryDirectory() as tmpdir:
            # Créer des fichiers
            (Path(tmpdir) / "test.pdf").write_text("test")

            # Scanner
            scanner = FolderScanner(tmpdir)
            files = scanner.scan()

            # Générer le rapport
            report_path = Path(tmpdir) / "test_report.html"
            reporter = HTMLReporter(str(report_path))
            reporter.generate_report(files=files, title="Test Report")

            if report_path.exists() and report_path.stat().st_size > 1000:
                print(f"   ✅ Rapport HTML OK - {report_path.stat().st_size} bytes")
                return True
            else:
                print("   ❌ Rapport HTML : fichier trop petit ou absent")
                return False

    except Exception as e:
        print(f"   ❌ Erreur rapport : {e}")
        return False


def test_extractor():
    """Test 5 : Tester l'extracteur (optionnel)"""
    print("\nTest 5 : Extracteur de pièces jointes...")
    try:
        from analyst_helper import AttachmentExtractor
        print("   ✅ Module extractor importé")
        print("   ℹ️  Test complet nécessite des fichiers .msg")
        return True
    except ImportError as e:
        print(f"   ⚠️  Module extract-msg non installé : {e}")
        print("      Installation : pip install extract-msg")
        return False


def main():
    """Exécute tous les tests"""
    print("=" * 60)
    print("TESTS ANALYST HELPER")
    print("=" * 60)

    results = []
    results.append(("Imports", test_imports()))
    results.append(("Scanner", test_scanner()))
    results.append(("Classificateur", test_classifier()))
    results.append(("Reporter", test_reporter()))
    results.append(("Extracteur", test_extractor()))

    # Résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ DES TESTS")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")

    print(f"\nRésultat : {passed}/{total} tests réussis")

    if passed == total:
        print("\n🎉 Tous les tests sont passés ! AnalystHelper est prêt.")
    else:
        print("\n⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")

    return passed == total


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
