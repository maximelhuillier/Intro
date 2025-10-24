@echo off
REM Lanceur pour AnalystHelper - Interface Graphique
REM Double-cliquez sur ce fichier pour lancer l'interface

echo ========================================
echo    AnalystHelper - Interface Graphique
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR : Python n'est pas installe ou n'est pas dans le PATH
    echo.
    echo Telechargez Python depuis : https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python detecte !
echo Lancement de l'interface...
echo.

REM Lancer l'interface graphique
python analyst_helper_gui.py

REM Si erreur
if errorlevel 1 (
    echo.
    echo Une erreur s'est produite.
    echo Verifiez que les dependances sont installees :
    echo    pip install -r requirements.txt
    echo.
    pause
)
