python3 -m venv venv
pip install django djangorestframework requests beautifulsoup4
 django-admin startproject modascraper .
 python manage.py startapp scraper
 python manage.py makemigrations
 python scraper/scraping.py
