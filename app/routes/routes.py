from flask import abort, Blueprint, make_response, request, Response
from app.models.planet import Planet
from ..db import db
from sqlalchemy import cast, String

planets_bp = Blueprint("planets_bp", __name__, url_prefix = "/planets")

@planets_bp.post("")
def create_planet():
    request_body = request.get_json()
    name = request_body["name"]
    description = request_body["description"]
    moons = request_body["moons"]

    new_planet = Planet(name=name, description=description, moons=moons)
    db.session.add(new_planet)
    db.session.commit()

    response = {
        "id": new_planet.id,
        "name": new_planet.name,
        "description": new_planet.description,
        "moons": new_planet.moons,
    }
    return response, 201

@planets_bp.get("")
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
        # Can try adding in more filters another time (<, >, etc.)
        query = query.where(cast(Planet.moons, String).like(f"%{moons_param}%")) # check this later

    query = query.order_by(Planet.id)
    planets = db.session.scalars(query)

    planets_response = []
    for planet in planets:
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "moons": planet.moons,
            }
        )
    return planets_response

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        response = {"message": f"planet id {planet_id} invalid"}
        abort(make_response(response , 400))
    
    query = db.select(Planet).where(Planet.id == planet_id)
    planet = db.session.scalar(query)

    if not planet:
        response = {"message": f"planet id {planet_id} not found"}
        abort(make_response(response, 404))
    return planet

@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)

    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "moons": planet.moons,
    }
