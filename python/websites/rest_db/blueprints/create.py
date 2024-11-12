from flask import Blueprint, request
from data import create_table, tables, table, by_id

bp = Blueprint(
    name="create",
    import_name=__name__
)

__all__ = ['bp']

# content

@bp.route('/create/<record>', methods=['PUT'])
@bp.route('/create/<record>/', methods=['PUT'])
def create(record):
    cols = request.headers.get('cols').split('(')[1].split(')')[0].split(',')
    if cols[-1] == '':
        create_table(str(record), cols[:-1])
    else:
        create_table(str(record), cols)
    return "[]"

@bp.route('/records')
@bp.route('/records/')
def records():
    return str(tables())

@bp.route('/records/<record>')
@bp.route('/records/<record>/')
def recordsrecsel(record):
    return str(table(record))

@bp.route('/records/<record>/<id>')
@bp.route('/records/<record>/<id>/')
def recordsrecselid(record, id):
    return str(by_id(table(record), id))