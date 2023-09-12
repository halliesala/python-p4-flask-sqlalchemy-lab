#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

# @app.route('/animal')
# def animal():
#     return """
#     <ul> 
#     </ul>
#     """

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    if animal:
        # return f"""
        # <ul>
        #     <li name="Name">{animal.name}</li>
        #     <li name="Species"{animal.species}</li>
        # </ul>
        # """
        return f"""
            <ul>Name: {animal.name}</ul>
            <ul>Species: {animal.species}</ul>
            <ul>Zookeeper: {animal.zookeeper.name}</ul>
            <ul>Enclosure: {animal.enclosure.environment}</ul>
        """
    return "No such animal"

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    if zookeeper:
        return f"""
            <ul>Name: {zookeeper.name}</ul>
            <ul>Birthday: {zookeeper.birthday}</ul>
            {
                "".join([
                    f"<ul>Animal: {animal.name} </ul>"
                    for animal
                    in zookeeper.animals
                ])
            }
        """
    return 'No such zookeeper'

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    if enclosure:
        return f"""
            <ul>Environment: {enclosure.environment}</ul>
            <ul>Open to Visitors: {"True" if enclosure.open_to_visitors else "False"}</ul>
            {
                "".join([
                    f"<ul>Animal: {animal.name} </ul>"
                    for animal
                    in enclosure.animals
                ])
            }
        """
    return ''


if __name__ == '__main__':
    app.run(port=5555, debug=True)
