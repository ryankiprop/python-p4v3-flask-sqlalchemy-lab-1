# server/app.py
#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quakes_data = [quake.to_dict() for quake in quakes]
    
    return jsonify({
        "count": len(quakes_data),
        "quakes": quakes_data
    })

@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.filter_by(id=id).first()
    
    if not earthquake:
        return make_response(jsonify({"message": f"Earthquake {id} not found."}), 404)
    
    return jsonify(earthquake.to_dict())

if __name__ == '__main__':
    app.run(port=5555, debug=True)