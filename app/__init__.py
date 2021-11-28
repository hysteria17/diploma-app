from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from app.mod_meteo.views import mod_meteo as meteo_module

app.register_blueprint(meteo_module)
# db.drop_all()
db.create_all()