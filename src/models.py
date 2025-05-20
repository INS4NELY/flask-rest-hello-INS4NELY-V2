from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            'name': self.name,
            'last_name': self.last_name,
            "email": self.email,
            'is_active': self.is_active
            # do not serialize the password, its a security breac
        }

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'), nullable=False)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey('vehicles.id'), nullable=False)
    user = relationship('User', backref='favorites')
    character = relationship('Character', backref='favorites')
    planet = relationship('Planet', backref='favorites')
    vehicle = relationship('Vehicle', backref='favorites')

    def serialize(self):
        return {
            "id": self.id,
            'user_id': self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id,
        }

class Character(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    birth_year: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    eye_color: Mapped[str] = mapped_column(String(30), unique=False, nullable=False)
    gender: Mapped[str] = mapped_column(String(30), unique=False, nullable=False)
    hair_color: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    height: Mapped[str] = mapped_column(String(30), unique=False, nullable=False)
    mass: Mapped[str] = mapped_column(String(30), unique=False, nullable=False)
    name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    skin_color: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            'birth_year': self.birth_year,
            'eye_color': self.eye_color,
            'gender': self.gender,
            'hair_color': self.hair_color,
            'height': self.height,
            'mass': self.mass,
            'name': self.name,
            'skin_color': self.skin_color
        }


class Planet(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    climate: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    diameter: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    gravity: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    name: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    orbital_period: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    population: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    rotation_period: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    surface_water: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    terrain: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            'climate': self.climate,
            'diameter': self.diameter,
            'gravity': self.gravity,
            'name': self.name,
            'orbital_period': self.orbital_period,
            'population': self.population,
            'rotation_period': self.rotation_period,
            'surface_water': self.surface_water,
            'terrain': self.terrain
        }
      

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id: Mapped[int] = mapped_column(primary_key=True)
    cargo_capacity: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    consumables: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    cost_in_credits: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    crew: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    length: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    max_atmosphering_speed: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    model: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    name: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    passengers: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    vehicle_class: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            'cargo_capacity': self.cargo_capacity,
            'consumables': self.consumables,
            'cost_in_credits': self.cost_in_credits,
            'crew': self.crew,
            'length': self.length,
            'manufacturer': self.manufacturer,
            'max_atmosphering_speed': self.max_atmosphering_speed,
            'model': self.model,
            'name': self.name,
            'passengers': self.passengers,
            'vehicle_class': self.passengers
        }