from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
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

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

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


# class Planet_Favorite(db.Model):
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('user.id'))
#     user = relationship(User)
#     planet_id = Column(Integer, ForeignKey('planet.id'))
#     planet = relationship(Planet)


# class Character(db.Model):
#     __tablename__ = 'character'
#     id = db.Column(Integer, primary_key=True)
#     name = db.Column(String(250), nullable=False)

# class Character_Favorite(db.Model):
#     __tablename__ = 'character_favorite'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = db.Column(Integer, primary_key=True)
#     user_id = db.Column(Integer, ForeignKey('user.id'))
#     user = relationship(User)
#     character_id = Column(Integer, ForeignKey('character.id'))
#     character = relationship(Character)

#     def to_dict(self):
#         return {}
