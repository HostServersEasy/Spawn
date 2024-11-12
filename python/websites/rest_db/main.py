#################
# HostBase 2024 #
#################

# You may not claim this product as your own in publication without modification,
# As said in the GNU General Public License.

# Information:
#   This project is an example template from the HostBase team.
#   We provide you with this resource to help you develop your project.
#   
# Project Description:
#   This project provides you with a RESTful API to manage an SQLite database.
#   The example implementations of this RESTful API is available inside the examples/ folder.
#
#   - The blueprints/root.py file contains an example implementation of a user login.
#   - The blueprints/create.py file contains all the methods for creating a new table in HTTP.
#   - The blueprints/delete.py file contains all the methods for deleting records in HTTP.
#   - The blueprints/read.py file contains all the methods for reading records in HTTP.
#   - The blueprints/write.py file contains all the methods for writing records in HTTP.
#
#   More information and documentation can be found in the readme.md file or by running your project and seeing the root path ( / ) (just a slash). 

import sqlite3, random
from flask import Flask, session

app = Flask(__name__)
app.config["SECRET_KEY"] = str(random.randint(14, 49755))

# blueprints
from blueprints.delete import bp as delb
from blueprints.read import bp as readb
from blueprints.write import bp as writeb
from blueprints.create import bp as createb
from blueprints.root import bp as root

app.register_blueprint(delb)
app.register_blueprint(readb)
app.register_blueprint(writeb)
app.register_blueprint(createb)
app.register_blueprint(root)

# run
app.run(
    host="0.0.0.0",
    port=80
)