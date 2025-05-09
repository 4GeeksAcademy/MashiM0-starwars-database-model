from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    people_favorites_associates: Mapped[list['PeopleFavorites']] = relationship(
        back_populates='user', cascade='all, delete-orphan', lazy='joined')
    planet_favorites_associates: Mapped[list['PlanetFavorites']] = relationship(
        back_populates='user', cascade='all, delete-orphan', lazy='joined')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    height: Mapped[int] = mapped_column(Integer)

class Starship(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    size: Mapped[str] = mapped_column(nullable=False)
    seats: Mapped[int] = mapped_column(nullable=False)

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    size: Mapped[str] = mapped_column(nullable=False)

class PeopleFavorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("people.id"))
    character: Mapped['People'] = relationship(
        "People", back_populates="user_favorite_associates")
    user: Mapped['User'] = relationship(
        "User", back_populates="people_favorites_associates")

class PlanetFavorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped['User'] = relationship(
        "User", back_populates="planet_favorites_associates")
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped['Planet'] = relationship(
        "Planet", back_populates="user_favorite_associates")

