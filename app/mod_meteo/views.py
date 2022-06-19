from flask import Blueprint, render_template, redirect
from datetime import datetime
from app import db, app
from app.mod_meteo.models import Source, Observation
from app.mod_meteo.utils import request_api

mod_meteo = Blueprint('meteo', __name__)


@mod_meteo.route('/test', methods=['GET', 'POST'])
def test():
    app.logger.error("test")

    endpoint = 'https://frost.met.no/sources/v0.jsonld'
    parameters = {
        'types': 'SensorSystem',
        'elements': 'wind_from_direction',
        'country': 'NO'
    }

    data = request_api(endpoint, parameters)

    for record in data:
        # print(record)
        sensor_data = dict(
            sensor_id=record['id'],
            name=record['name'],
            country=record['country'],
            country_code=record['countryCode'],
            valid_from=datetime.fromisoformat(record['validFrom'][:-1])
        )
        if not Source.query.filter_by(sensor_id=sensor_data['sensor_id']).first():
            app.logger.info('Adding source %s to database', sensor_data['sensor_id'])
            source = Source(**sensor_data)
            db.session.add(source)

    db.session.commit()

    return redirect("/")

@mod_meteo.route("/query", methods=['GET', 'POST'])
def query():
    sources = Source.query.order_by(Source.valid_from).limit(10).all()
    # sources_id = ','.join(src.sensor_id for src in sources)
    #
    # endpoint = 'https://frost.met.no/observations/v0.jsonld'
    # parameters = {
    #     'sources': sources_id,
    #     'elements': 'wind_from_direction, wind_speed, air_temperature',
    #     'referencetime': 'latest'
    # }
    #
    # data = request_api(endpoint, parameters)

    for src in sources:
        endpoint = 'https://frost.met.no/observations/v0.jsonld'
        parameters = {
            'sources': src.sensor_id,
            'elements': 'wind_from_direction, wind_speed, air_temperature',
            'referencetime': 'latest'
        }
        data = request_api(endpoint, parameters)

        if data != None:
            reference_time = datetime.fromisoformat(data[0]['referenceTime'][:-1])
            wind_from_direction = None
            wind_speed = None
            air_temperature = None

            observations = data[0]['observations']

            if len(data) > 1:
                for i in range(1, len(data)):
                    for x in data[i]['observations']:
                        observations.append(x)

            app.logger.info(observations)

            for observation in observations:
                if observation['elementId'] == 'wind_from_direction':
                    wind_from_direction = observation['value']
                    continue
                if observation['elementId'] == 'wind_speed':
                    wind_speed = observation['value']
                    continue
                if observation['elementId'] == 'air_temperature':
                    air_temperature = observation['value']

            app.logger.info("Adding observation to database")

            # app.logger.info(wind_from_direction, wind_speed, air_temperature)
            obs = Observation(source_id=src.id, wind_from_direction_value=wind_from_direction, wind_speed_value=wind_speed,
                            air_temperature=air_temperature, reference_time=reference_time)
            src.observations.append(obs)
            db.session.add(src)
            db.session.add(obs)

    app.logger.info("Commiting to DB")
    db.session.commit()

    return redirect("/")

@mod_meteo.route("/", methods=['GET','POST'])
def index():
    sources = Source.query.order_by(Source.valid_from).limit(10).all()
    # sources = Source.query.limit(10).all()
    observations_data = []
    for src in sources:
        observation = Observation.query.filter_by(source_id=src.id).order_by(Observation.reference_time.desc()).first()
        # if observation is None == False:
        obs = dict(
            sensor_id=src.sensor_id,
            valid_from=src.valid_from,
            wind_direction=observation.wind_from_direction_value if observation.wind_from_direction_value else None,
            wind_speed=observation.wind_speed_value if observation.wind_speed_value else None,
            air_temperature=observation.air_temperature if observation.air_temperature else None,
            reference_time=observation.reference_time
        )
        observations_data.append(obs)

    return render_template("mod_meteo/index.html", observations=observations_data)