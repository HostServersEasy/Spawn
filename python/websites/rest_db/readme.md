# REST in CRUD API

This API contains of four endpoints/methods for writing, reading, creating tables and deleting. It also includes a fully functional login and register implementation that uses BCrypt to convert strings into hashes.

This API encrypts the email address and password of the user, and then stores it in session data and the SQLite3 database.

- `/`: Shows this Markdown file in a formatted HTML document.
- `/delete/<record>/<id>` - [ `DELETE` ]: Deletes an item from a record.
- `/write/<record>/<id>` - [ `POST`, `PUT` ]: Writes an (existing) item to a record.
- `/create/<record>` - [ `PUT` ]: Creates a new record, which items will be inserted into.
- `/read/<record>/<id>` - [ `GET`, `POST` ]: Read an item under a record by its ID.
  
- `/login` - [ `GET`, `POST` ]: A page which demonstrates how the methods work.
- `/register` - [ `GET`, `POST` ]: A page which demonstrates how the methods work.
  
- `/records` - [ `GET` ]: Grabs a list of all valid records/tables and returns their name in a list (`[]`).
- `/records/<record>` - [ `GET` ]: Grabs list of tuples in a record/table. (basically returns the selected record/table's contents)
- `/records/<record>/<id>` - [ `GET` ]: Grabs a tuple inside a list of tuples inside a record/table. (basically returns the specific tuple object with the correct ID in a record)

The code for the pure login implementation and methods are in the file: `blueprints/root.py`
The code for just the API implementation or database methods are in the other blueprint files: `create.py`, `delete.py`, `read.py`, `write.py`.
There is **no authorization in these examples** so it should **not be used in a production environment**.

[Log in](/login) or [Register](/register) for the demo.
Once logged in, your information will appear below here.

<style>
    a {
        color: #000;
    }
    p,h1,li {
        font-family: system-ui, arial, helvetica;
    }
    code {
        font-family: monospace;
    }
</style>