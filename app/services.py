from app.models import db, Building, TypeBuilding, Country, City
from sqlalchemy.sql import func

from app.serializers import building_cschema


def get_all_buildings():
    query = Building.query
    return query.all()


def get_building_by_id(building_id):
    query = Building.query.filter_by(id=building_id).one_or_none()
    return query


def insert_building(building: dict):
    item = building_cschema.load(building, session=db.session)
    db.session.add(item)
    db.session.commit()
    return Building.query.filter(
        Building.id == db.session.query(func.max(Building.id))
    ).one_or_none()


def update_building_by_id(building_id, update_building):
    building = get_building_by_id(building_id)
    if not building:
        return None

    building = building_cschema.load(
        update_building, instance=building, session=db.session, partial=True
    )

    db.session.commit()

    return get_building_by_id(building_id)


def delete_building_by_id(building_id):
    Building.query.filter(Building.id == building_id).delete()
    db.session.commit()


# def get_grouped_by_type():
#     query = (
#         db.session.query(
#             TypeBuilding.type.label("Тип"),
#             func.max(Building.height).label("Макс. высота"),
#             func.min(Building.height).label("Мин. высота"),
#             func.avg(Building.height).label("Средняя высота")
#         )
#         .join(Building)
#         .group_by(TypeBuilding.type)
#     )
#     return [query.statement.columns.keys(), query.all()]
#
#
# def get_grouped_by_country():
#     query = (
#         db.session.query(
#             Country.name.label("Страна"),
#             func.max(Building.height).label("Макс. высота"),
#             func.min(Building.height).label("Мин. высота"),
#             func.avg(Building.height).label("Средняя высота")
#         )
#         .select_from(Building)
#         .join(City, Building.city_id == City.id)
#         .join(Country, City.country_id == Country.id)
#         .group_by(Country.name)
#     )
#     return [query.statement.columns.keys(), query.all()]
#
#
# def get_grouped_by_year():
#     query = (
#         db.session.query(
#             Building.year.label("Год"),
#             func.max(Building.height).label("Макс. высота"),
#             func.min(Building.height).label("Мин. высота"),
#             func.avg(Building.height).label("Средняя высота")
#         )
#         .group_by(Building.year)
#     )
#     return [query.statement.columns.keys(), query.all()]
#
#
# def get_buildings_in_range(start_year, end_year):
#     query = (
#         db.session.query(
#             Building.title.label("Здание"),
#             TypeBuilding.type.label("Тип"),
#             Country.name.label("Страна"),
#             City.name.label("Город"),
#             Building.year.label("Год"),
#             Building.height.label("Высота")
#         )
#         .join(TypeBuilding)
#         .join(City)
#         .join(Country)
#         .filter(Building.year.between(start_year, end_year))
#     )
#     return [query.statement.columns.keys(), query.all()]
#
