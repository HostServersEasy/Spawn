import sqlite3, os, random, encryption

db = sqlite3.connect('lite.db', check_same_thread=False)
cursor = db.cursor()

columns_preset = ['firstname TEXT NOT NULL', 'lastname TEXT NOT NULL', 'email TEXT NOT NULL UNIQUE', 'password TEXT NOT NULL UNIQUE']

def create_table(table_name, cols=columns_preset):
    clf = str()
    for index, i in enumerate(cols): 
        clf += f"{i}"
        if not index == (len(cols) - 1):
            clf += ",\n"
    
    print(clf)
    db.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY,
        {clf}
    );
    ''')
    db.commit()
    
def delete_table(table_name):
    db.execute(f'DROP TABLE IF EXISTS {table_name}')
    db.commit()
    
def write_to_table(table_name, vals:list[tuple]):
    qs = str()
    for index, item in enumerate(vals):
        qs += f"{item}"
        if not index == (len(vals) - 1):
            qs += ", "
    
    print(f"QSVALS: {qs.split('(')[1].split(')')[0]}")
    try:
        db.execute(f'INSERT INTO {table_name} VALUES({qs.split("(")[1].split(")")[0]})')
        db.commit()
    except sqlite3.IntegrityError as e:
        return e
    
def tables():
    table = []
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table_name in tables:
        table.append(table_name)
    return table

def table(record):
    """
    Read from a table inside SQLite3 database.
    """
    try:
        cursor.execute(f"SELECT * FROM {record}")
        tab = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"Error: invalid table: {record}")
        return None
    return tab
    
def create_user(
    email:str,
    password:str,
    firstName:str,
    lastName:str
):
    uid = random.randint(0,100000000)
    
    # write the user to the users table
    
    create_table('users', columns_preset) # just try and create the table first
    write_to_table('users', 
        [(str(uid), str(firstName), str(lastName), str(encryption.hash(email)), str(encryption.hash(password)))]
    )

    return uid

def remove_user(
    uid:str
):
    query = f"DELETE FROM users WHERE id={uid}"
    try:
        db.execute(query)
        db.commit()
    except Exception as e:
        print(e.with_traceback())
        return False
    
    return True
    
def get_users():
    create_table('users', columns_preset)
    cursor.execute(f"SELECT * FROM users")
    rows = cursor.fetchall()
    return rows

def user(tuplwe,email):
    for user in tuplwe:
        print(user)
        if encryption.check_hash(str(email).encode("UTF-8"), str(user[3]).encode("UTF-8")):
            return user
    
    return None

def by_id(tuplwe, id):
    for obj in tuplwe:
        if str(obj[0]) == str(id):
            return obj
    return None