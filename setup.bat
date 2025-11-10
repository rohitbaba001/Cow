@echo off
echo ========================================
echo Dairy Farm Management System Setup
echo ========================================
echo.

echo Creating virtual environment...
python -m venv venv
echo.

echo Activating virtual environment...
call venv\Scripts\activate
echo.

echo Installing required packages...
pip install -r requirements.txt
echo.

echo Creating migrations...
python manage.py makemigrations
echo.

echo Running migrations...
python manage.py migrate
echo.

echo Creating media directories...
if not exist "media" mkdir media
if not exist "media\cows" mkdir media\cows
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Create a superuser: python manage.py createsuperuser
echo 2. Run the server: python manage.py runserver
echo 3. Open browser: http://127.0.0.1:8000/
echo.
echo Press any key to create superuser now...
pause > nul

python manage.py createsuperuser
echo.

echo ========================================
echo All done! Starting development server...
echo ========================================
python manage.py runserver
