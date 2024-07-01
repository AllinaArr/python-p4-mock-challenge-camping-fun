#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/campers', methods=['GET', 'POST'])
def all_campers():
    campers = Camper.query.all()
    
    return [c.to_dict(rules=['-signups']) for c in campers], 200

@app.route('/campers/<int:id>', methods=['GET', 'PATCH'])
def campers_by_id(id):
    camper = Camper.query.filter(Camper.id == id).first()
    if not camper:
            return {'error':'Camper not found'}, 404
        
    if request.method == 'GET':
        return camper.to_dict(), 200
    elif request.method == 'PATCH':
        data = request.get_json()
        
        try:
            if 'name' in data:
                camper.name = data['name']
            if 'age' in data:
                camper.age = data['age']
        except ValueError:
            return {'error':["validation error"]}, 400
            
        db.session.add(camper)
        db.session.commit()
        
        return camper.to_dict(rules=['-signups']), 202

if __name__ == '__main__':
    app.run(port=5555, debug=True)
