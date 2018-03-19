rm db.sqlite3
rm -rf */migrations/*
python3 manage.py makemigrations gestionUsuarios
python3 manage.py makemigrations gestionAplicaciones
python3 manage.py makemigrations asignacionHistorias


python3 manage.py migrate  gestionUsuarios
python3 manage.py migrate  gestionAplicaciones
python3 manage.py migrate  asignacionHistorias
python3 manage.py migrate 