from flask import abort, Blueprint, make_response, request, Response
from app.models.moon import Moon
from ..db import db
from sqlalchemy import cast, String, Integer
from .route_utilities import validate_model

bp = Blueprint("moons_bp", __name__, url_prefix = "/moons")

@bp.post("")
def create_moon():
    request_body = request.get_json()

    try:
        new_moon = Moon.from_dict(request_body)
        
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
    
    db.session.add(new_moon)
    db.session.commit()

    return make_response(new_moon.to_dict(), 201)

@bp.get("")
def get_all_moons():
    query = db.select(Moon)

    # name_param = request.args.get("name")
    # if name_param:
    #     query = query.where(Moon.name.ilike(f"%{name_param}%"))

    moons = db.session.scalars(query.order_by(Moon.id))
    # Use list comprehension syntax to create the list `authors_response`
    moons_response = [moon.to_dict() for moon in moons]

    return moons_response