#!/bin/bash

# Arrêter l'exécution en cas d'erreur
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@42.fr
DJANGO_SUPERUSER_PASSWORD=trans

set -e

# Attendre que la base de données soit prête (facultatif)
# Remplacer 'postgres' et '5432' par vos propres valeurs de HOST et PORT si elles sont différentes
echo "Attente de la base de données..."
while !</dev/tcp/postgres/5432; do
  sleep 1
done

# Exécuter les migrations Django
echo "Application des migrations Django..."
python3.11 manage.py makemigrations
python3.11 manage.py migrate
python3.11 manage.py shell < /app/Docker/create_superuser.py


# Démarrer Gunicorn
echo "Démarrage de Gunicorn..."
exec gunicorn transcendence.wsgi:application --bind 0.0.0.0:8001