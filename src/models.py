from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorite_planets = db.relationship('Planet_Favorite', back_populates="owner")
    favorite_people = db.relationship('FavoritePerson', back_populates='owner')
    # is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    favorite = db.relationship('Planet_Favorite', back_populates='planet')

    def __init__(self, name):
        self.name = name

    @classmethod
    def create(cls, name):
        new_planet = cls(name)
        db.session.add(new_planet)
        try:
            db.session.commit()
            return new_planet
        except Exception as error:
            print(error.args)
            return None

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            print(error.args)
            return False

    def update(self, name):
        self.name = name
        try:
            db.session.commit()
            return True
        except Exception as error:
            print(error.args)
            return False

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    favorite = db.relationship('FavoritePerson', back_populates='person')

    def __init__(self, name):
        self.name = name
    
    @classmethod
    def create(cls, name):
        new_person = cls(name)
        db.session.add(new_person)
        try:
            db.session.commit()
            return new_person
        except Exception as error:
            print(error.args)
            return None

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            print(error.args)
            return False

    def update(self, name):
        self.name = name
        try:
            db.session.commit()
            return True
        except Exception as error:
            print(error.args)
            return False


class Planet_Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', back_populates='favorite_planets')
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship('Planet', back_populates='favorite')

    def serialize(self):
        return {
            "id": self.id,
            "owner": self.owner.serialize(),
            "planet": self.planet.serialize()
        }

class FavoritePerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', back_populates='favorite_people')
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', back_populates='favorite')

    def serialize(self):
        return {
            "id": self.id,
            "owner": self.owner.serialize(),
            "person": self.person.serialize()
        }