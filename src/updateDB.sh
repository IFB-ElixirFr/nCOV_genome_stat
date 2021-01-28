find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

python manage.py makemigrations
python manage.py migrate
python manage.py load_regions
python manage.py load_vaccins_regions
python manage.py load_countries
python manage.py load_vaccins_hospitIncidReg