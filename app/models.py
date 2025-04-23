from app.extensions import db


class Country(db.Model):
    __tablename__ = "country"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cities = db.relationship("City", back_populates="country", cascade="all")

    def __repr__(self):
        return f"<Country(id={self.id}, name={self.name})>"


class TypeBuilding(db.Model):
    __tablename__ = "type_building"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    buildings = db.relationship(
        "Building", back_populates="type_building", cascade="all"
    )

    def __repr__(self):
        return f"<TypeBuilding(id={self.id}, type={self.type})>"


class City(db.Model):
    __tablename__ = "city"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"))
    country = db.relationship("Country", back_populates="cities")
    buildings = db.relationship("Building", back_populates="city", cascade="all")

    def __repr__(self):
        return f"<City(id={self.id}, name={self.name}, country_id={self.country_id})>"


class Building(db.Model):
    __tablename__ = "building"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    type_building_id = db.Column(db.Integer, db.ForeignKey("type_building.id"))
    type_building = db.relationship("TypeBuilding", back_populates="buildings")
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    city = db.relationship("City", back_populates="buildings")
    year = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'{{"id": {self.id}, "title": "{self.title}", "year": {self.year}, "height": {self.height} , "type_building": {self.city}}}"}}'
