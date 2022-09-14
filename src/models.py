from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    

    people_favorites = db.relationship('People_favorites', backref="user")
    planets_favorites = db.relationship('Planets_favorites', backref="user")

    """def get_people(self):
        return list(map(lambda person: person.to_dict(), self.people))
    
    def get_planets(self):
        return list(map(lambda planet: planet.to_dict(), self.planets))"""
    


    def save(self):
        db.session.add(self)  
        db.session.commit()  

    def update(self):
        db.session.commit()  

    def delete(self):
        db.session.delete(self)  
        db.session.commit()  

    def serialize(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }

class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(200), nullable=False)  
    gender = db.Column(db.String(100))  
    birth_year = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String(100)) 
    eye_color = db.Column(db.String(100)) 
    

    def save(self):
        db.session.add(self)  
        db.session.commit()  

    def update(self):
        db.session.commit()  

    def delete(self):
        db.session.delete(self)  
        db.session.commit()  

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'birth_year': self.birth_year,
            'height': self.height,
            'hair_color': self.hair_color,
            'eye_color': self.eye_color

        }

class People_favorites(db.Model):
    __tablename__ = 'people_favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,  db.ForeignKey('users.id'))  
    people_id = db.Column(db.Integer, db.ForeignKey('people.id')) 
    people = db.relationship('People', backref='people_favorite')

    def save(self):
        db.session.add(self)  
        db.session.commit()  

    def update(self):
        db.session.commit()  

    def delete(self):
        db.session.delete(self)  
        db.session.commit()  

    def serialize(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'people_id': self.people_id
        }

class Planets(db.Model):
    __tablename__ =  'planets'
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(200), nullable=False) 
    climate = db.Column(db.String(100), nullable=False) 
    terrain = db.Column(db.String(100), nullable=False) 
    population  = db.Column(db.String(100), nullable=False)
    gravity  = db.Column(db.String(100), nullable=False)
    orbital_period =  db.Column(db.Integer, nullable=False)


    def save(self):
        db.session.add(self)  
        db.session.commit()  

    def update(self):
        db.session.commit()  

    def delete(self):
        db.session.delete(self)  
        db.session.commit()  

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'climate': self.climate,
            'terrain': self.terrain,
            'population': self.population,
            'gravity': self.gravity,
            'orbital_period': self.orbital_period

        }

class Planets_favorites(db.Model):
    __tablename__ = 'planets_favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planets = db.relationship('Planets', backref='planets_favorite')
    
    def save(self):
        db.session.add(self)  
        db.session.commit()  

    def update(self):
        db.session.commit()  

    def delete(self):
        db.session.delete(self)  
        db.session.commit()  
    
    def serialize(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'planets_id': self.planets_id
        }