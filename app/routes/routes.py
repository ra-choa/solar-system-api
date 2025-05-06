from flask import abort, Blueprint, make_response, request, Response
from app.models.planet import Planet
from ..db import db
from sqlalchemy import cast, String, Integer
from .route_utilities import validate_model

bp = Blueprint("bp", __name__, url_prefix = "/planets")

@bp.post("")
def create_planet():
    request_body = request.get_json()
    try:
        new_planet = Planet.from_dict(request_body)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_planet)
    db.session.commit()

    return new_planet.to_dict(), 201

@bp.get("")
def get_all_planets():
    query = db.select(Planet)

    name_param = request.args.get("name")
    if name_param:
        query = query.where(Planet.name.ilike(f"%{name_param}%"))
    
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Planet.description.ilike(f"%{description_param}%"))
    
    moons_param = request.args.get("moons")
    if moons_param: 
        # Assume that if < or > in moons_param, then it's followed by a number.
        if '<' in moons_param:
            num = int(moons_param[1:])
            query = query.where(Planet.moons < num)
        elif '>' in moons_param:
            num = int(moons_param[1:])
            query = query.where(Planet.moons > num)
        else:
            query = query.filter(Planet.moons == int(moons_param))

    query = query.order_by(Planet.id)
    planets = db.session.scalars(query)

    planets_response = []
    for planet in planets:
        planets_response.append(planet.to_dict())
    return planets_response

@bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_model(planet_id)

    return planet.to_dict()

@bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_model(planet_id)
    request_body = request.get_json()

    planet.title = request_body["name"]
    planet.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_model(planet_id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")