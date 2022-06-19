DEBUG = True

# import os
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app2.db')

SQLALCHEMY_DATABASE_URI = 'postgresql://appuser:qwerty@localhost:5432/appdb'
SQLALCHEMY_TRACK_MODIFICATIONS = False
METEO_CLIENT_ID = 'f7fb28d2-6ded-45ae-9575-10aac308301d'

THREADS_PER_PAGE = 2