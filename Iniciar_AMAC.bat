@echo off
chcp 65001 > nul
echo =======================================================
echo   🌾 AMAC - Asistente de Monitoreo Agricola Climatico
echo   NASA Space Apps Challenge 2026
echo =======================================================
echo.
echo Abriendo la aplicacion en su navegador web predeterminado...
start "" "%~dp0frontend\index.html"
echo.
echo Verificando servidor Backend Python (opcional)...
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Python detectado. Para iniciar el backend con NASA POWER API en vivo:
    echo      cd backend ^&^& pip install -r requirements.txt ^&^& python app.py
) else (
    echo [INFO] Python no esta en PATH, pero la aplicacion funciona 100% en el navegador con
    echo        modelos integrados, calculos agroclimaticos, mapas y reportes interactivos.
)
echo.
echo Presione cualquier tecla para cerrar esta ventana...
pause > nul
