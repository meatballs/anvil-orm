import anvil.tables as tables
from anvil.tables import app_tables
import anvil.server

from . import model

__version__ = "0.1.0"


def get_sequence_value(sequence_id):
    row = app_tables.sequence.get(id=sequence_id) or app_tables.sequence.add_row(
        id=sequence_id, next=1
    )
    result = row["next"]
    row["next"] += 1
    return result


def get_row(class_name, id):
    table = getattr(app_tables, class_name.lower())
    return table.get(id=id)


@anvil.server.callable
def get_object(class_name, id):
    cls = getattr(model, class_name)
    return cls._from_row(get_row(class_name, id))


@anvil.server.callable
def list_objects(class_name, **filter_args):
    cls = getattr(model, class_name)
    table = getattr(app_tables, class_name.lower())
    rows = table.search(**filter_args)
    return [cls._from_row(row) for row in rows]


@anvil.server.callable
def save_object(instance):
    table_name = type(instance).__name__.lower()
    table = getattr(app_tables, table_name)

    attributes = {
        name: getattr(instance, name)
        for name, attribute in instance._attributes.items()
    }
    relationships = {
        name: get_row(relationship.cls.__name__, getattr(instance, name).id)
        for name, relationship in instance._relationships.items()
    }

    if instance.id is None:
        with tables.Transaction():
            id = get_sequence_value(table_name)
            table.add_row(id=id, **attributes, **relationships)
    else:
        row = table.get(id=instance.id)
        row.update(**attributes, **relationships)
