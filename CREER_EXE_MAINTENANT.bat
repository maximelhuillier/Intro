@echo off
REM ============================================
REM Script pour créer AnalystHelper.exe
REM Double-cliquez sur ce fichier !
REM ============================================

echo.
echo ========================================
echo   Creation d'AnalystHelper.exe
echo ========================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR : Python n'est pas installe
    echo Installez Python depuis https://python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Python detecte !
echo.

REM Vérifier si PyInstaller est installé
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [2/4] Installation de PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERREUR : Impossible d'installer PyInstaller
        pause
        exit /b 1
    )
) else (
    echo [2/4] PyInstaller deja installe
)
echo.

REM Vérifier les dépendances
echo [3/4] Verification des dependances...
pip install -r requirements.txt >nul 2>&1
echo.

REM Créer l'exe
echo [4/4] Creation de l'executable...
echo Cela peut prendre 3-5 minutes, patientez...
echo.

pyinstaller --onefile --windowed --name=AnalystHelper --clean analyst_helper_gui.py

if errorlevel 1 (
    echo.
    echo ERREUR : La creation a echoue
    echo Consultez les messages ci-dessus
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SUCCES !
echo ========================================
echo.
echo L'executable a ete cree dans :
echo   %CD%\dist\AnalystHelper.exe
echo.
echo Vous pouvez maintenant :
echo 1. Tester l'exe : ouvrir dist\AnalystHelper.exe
echo 2. Distribuer ce fichier a vos collegues
echo.
echo Vos collegues n'auront PAS besoin de Python !
echo.

REM Proposer d'ouvrir le dossier
set /p OPEN="Ouvrir le dossier dist ? (o/n) : "
if /i "%OPEN%"=="o" (
    explorer dist
)

echo.
pause
