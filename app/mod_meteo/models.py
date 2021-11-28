from app import db

class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

class Source(Base):

    sensor_id = db.Column(db.String(32), nullable=False, unique=True)
    name = db.Column(db.String(128))
    country = db.Column(db.String(128), nullable=False)
    country_code = db.Column(db.String(128), nullable=False)
    valid_from = db.Column(db.DateTime, nullable=False)
    observations = db.relationship('Observation', backref='source', lazy=True)

class Observation(Base):

    source_id = db.Column(db.Integer, db.ForeignKey('source.id'), nullable=False)
    wind_from_direction_value = db.Column(db.Float)
    wind_speed_value = db.Column(db.Float)
    air_temperature = db.Column(db.Float)
    reference_time =  db.Column(db.DateTime, nullable=False)