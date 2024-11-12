from flask import Blueprint
from data import db, cursor

bp = Blueprint(
    name="read",
    import_name=__name__
)

__all__ = ['bp']

# content

@bp.route('/read/<record>/<id>', methods=['GET'])
@bp.route('/read/<record>/<id>/',methods=['GET'])
def read(record, id):
    query    = f"""SELECT * FROM {record} WHERE id={id}"""
    response = {'message': 'Read record successfully.', 'data': ''}
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        response['data'] = rows
    except: response = {'message': 'Error reading record.'}
    
    return response