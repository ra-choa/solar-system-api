from flask import abort, Blueprint, make_response
from app.models.planet import Planet

planets_bp = Blueprint("planets_bp", __name__, url_prefix = "/planets")
