#!/bin/bash
# Lanceur pour AnalystHelper - Interface Graphique
# Exécutez ce script pour lancer l'interface

echo "========================================"
echo "  AnalystHelper - Interface Graphique"
echo "========================================"
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ ERREUR : Python 3 n'est pas installé"
    echo ""
    echo "Installez Python 3 :"
    echo "  - Mac : brew install python3"
    echo "  - Linux : sudo apt install python3 python3-pip"
    echo ""
    exit 1
fi

echo "✅ Python détecté !"
echo "Lancement de l'interface..."
echo ""

# Lancer l'interface graphique
python3 analyst_helper_gui.py

# Vérifier le code de retour
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Une erreur s'est produite."
    echo "Vérifiez que les dépendances sont installées :"
    echo "   pip3 install -r requirements.txt"
    echo ""
    read -p "Appuyez sur Entrée pour continuer..."
fi
