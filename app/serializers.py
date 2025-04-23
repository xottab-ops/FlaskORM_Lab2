from app.models import Country, City, Building, TypeBuilding
from app.extensions import ma, db

class CountrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Country

class CitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = City
        load_instance = True
        sqla_session = db.session
    country = ma.Nested(CountrySchema())

class TypeBuildingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TypeBuilding
        load_instance = True
        sqla_session = db.session
    id = ma.Integer(dump_only=True)

class BuildingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Building
        load_instance = True
        sqla_session = db.session

    type_building = ma.Nested(TypeBuildingSchema())
    city = ma.Nested(CitySchema())

    type_building_id = ma.auto_field()
    city_id = ma.auto_field()

building_cschema = BuildingSchema()
buildings_cschema = BuildingSchema(many=True)
