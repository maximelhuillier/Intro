@echo off
REM Lancer DOC EXPLORER - ARGOS
REM Ce fichier lance l'application Python

echo ======================================
echo    DOC EXPLORER - ARGOS
echo    Chargement en cours...
echo ======================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installe ou n'est pas dans le PATH
    echo Veuillez installer Python depuis https://www.python.org/
    pause
    exit /b 1
)

REM Lancer l'application
python "%~dp0doc_explorer.py"

REM Si erreur
if %errorlevel% neq 0 (
    echo.
    echo ERREUR lors du lancement de l'application
    pause
)
