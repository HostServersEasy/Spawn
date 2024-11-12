from flask import Blueprint, request
from data import db, cursor, write_to_table, create_table

bp = Blueprint(
    name="write",
    import_name=__name__
)

__all__ = ['bp']

# content

@bp.route('/write/<record>/<id>', methods=['PUT', 'POST'])
@bp.route('/write/<record>/<id>/',methods=['PUT', 'POST'])
def write(record, id):
    response = {'message': 'Written record successfully.', 'data': ''}
    data = request.headers.get('data').split('(')[1].split(')')[0].split(',')
    cols = request.headers.get('cols').split('(')[1].split(')')[0].split(',')
    
    if not data or not cols:
        return "Invalid request headers."
    
    if cols[-1] == '':
        print("Yes: columns last element ends with a comma")
        print(cols)
        create_table(record, cols[:-1]) # just try and create a table just in case to prevent errors
        # excludes the last object of list.
    else:
        print("No: columns last element doesn't end with a comma")
        print(cols)
        create_table(record, cols) # the normal object
    
    if data[-1] == '':
        write_to_table(record, [
            (id, *data[:-1]) # read all values from request data, excluding last object of list.
        ])
    else:
        write_to_table(record, [
            (id, *data) # read all values from request data
        ])
    
    #try:
        #db.execute(query)
        #rows = cursor.fetchall()
        #response['data'] = rows
    #except: response = {'message': 'Error writing record.'}
    
    return response