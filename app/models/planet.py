from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Planet:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    moon: Mapped[int]

    # def __init__(self, id, name, description, moon):
    #     self.id = id
    #     self.name = name
    #     self.description = description
    #     self.moon = moon

# planets = [
#     Planet(1, "Mercury", "Smallest. Mainly rock.", None),
#     Planet(2, "Venus", "Second from the sun. Mainly rock.", None),
#     Planet(3, "Earth", "Human life. Mainly rock.", 1),
#     Planet(4, "Mars", "What came first: Mars or Martian?. Mainly rock.", 2),
#     Planet(5, "Jupiter", "Largest. Mainly gas or ice.", 95),
#     Planet(6, "Saturn", "Rings made from particles of ice, dust, and rock. Mainly gas or ice.", 146),
#     Planet(7, "Uranus", "Mainly gas or ice.", 27),
#     Planet(8, "Neptune", "The Blue Planet. Mainly gas or ice.", 14),
#     Planet(9, "Pluto", "A dwarf planet under", 14)
# ]

# https://science.nasa.gov/solar-system/planets/

