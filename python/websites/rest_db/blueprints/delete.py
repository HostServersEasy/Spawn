from flask import Blueprint
from data import db, cursor

bp = Blueprint(
    name="delete",
    import_name=__name__
)

__all__ = ['bp']

# content

@bp.route('/delete/<record>/<id>', methods=['DELETE'])
@bp.route('/delete/<record>/<id>/',methods=['DELETE'])
def delete(record, id):
    query    = f"""DELETE FROM {record} WHERE id={id}"""
    response = {'message': 'Deleted record successfully.'}
    
    try:
        db.execute(query)
        db.commit()
    except: response = {'message': 'Error deleting record.'}
    
    return response