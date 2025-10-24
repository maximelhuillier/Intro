#!/bin/bash
# ============================================
# Script pour créer AnalystHelper.exe
# Exécutez : ./creer_exe_maintenant.sh
# ============================================

echo ""
echo "========================================"
echo "  Création d'AnalystHelper.exe"
echo "========================================"
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ ERREUR : Python n'est pas installé"
    echo "Installez Python depuis https://python.org/downloads/"
    exit 1
fi

echo "✅ [1/4] Python détecté !"
echo ""

# Vérifier si PyInstaller est installé
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo "📦 [2/4] Installation de PyInstaller..."
    pip3 install pyinstaller
    if [ $? -ne 0 ]; then
        echo "❌ ERREUR : Impossible d'installer PyInstaller"
        exit 1
    fi
else
    echo "✅ [2/4] PyInstaller déjà installé"
fi
echo ""

# Vérifier les dépendances
echo "📦 [3/4] Vérification des dépendances..."
pip3 install -r requirements.txt > /dev/null 2>&1
echo ""

# Créer l'exe
echo "🔨 [4/4] Création de l'exécutable..."
echo "Cela peut prendre 3-5 minutes, patientez..."
echo ""

pyinstaller --onefile --windowed --name=AnalystHelper --clean analyst_helper_gui.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ ERREUR : La création a échoué"
    echo "Consultez les messages ci-dessus"
    exit 1
fi

echo ""
echo "========================================"
echo "  ✅ SUCCÈS !"
echo "========================================"
echo ""
echo "L'exécutable a été créé dans :"
echo "  $(pwd)/dist/AnalystHelper.exe"
echo ""
echo "Note : Sur Mac/Linux, le fichier s'appelle 'AnalystHelper' (sans .exe)"
echo ""
echo "Vous pouvez maintenant :"
echo "1. Tester : ./dist/AnalystHelper (Mac/Linux)"
echo "2. Distribuer ce fichier à vos collègues"
echo ""
echo "Vos collègues n'auront PAS besoin de Python !"
echo ""

# Proposer d'ouvrir le dossier
read -p "Ouvrir le dossier dist ? (o/n) : " OPEN
if [ "$OPEN" = "o" ] || [ "$OPEN" = "O" ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open dist
    else
        xdg-open dist 2>/dev/null || nautilus dist 2>/dev/null || echo "Ouvrez manuellement : $(pwd)/dist"
    fi
fi

echo ""
