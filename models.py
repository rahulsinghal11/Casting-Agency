import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime
from flask_migrate import Migrate
from dotenv import load_dotenv
import json


load_dotenv()

if os.getenv('ENV') == 'test':
    database_path = os.getenv('TEST_DATABASE_URL')
else:
    database_path = os.getenv('DATABASE_URL')


db = SQLAlchemy()

'''
setup_db(app)
    binds flask app and SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Movies
a persistent movie entity, extends the base SQLAlchemy Model
'''


class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True, nullable=False)
    release_date = Column(DateTime(), nullable=False)

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    '''
    insert()
        inserts a new movie into the database
        the movie must have a unique title, a unique id or null id
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a movie from the database
        the movie must exist in the database
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a movie in the database
        the movie must exist in the database
    '''
    def update(self):
        db.session.commit()


'''
Actors
a persistent movie entity, extends the base SQLAlchemy Model
'''


class Actors(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=False)
    name = Column(String(80), unique=True, nullable=False)
    gender = Column(String, nullable=False)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age
        }

    '''
    insert()
        inserts a new actor into the database
        the actor must have a unique name, a unique id or null id
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes an actor from the database
        the actor must exist in the database
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates an actor details in the database
        the actor must exist in the database
    '''

    def update(self):
        db.session.commit()
