#################
# HostBase 2024 #
#################

# Information:
#   This project is an example template from the HostBase team.
#   We provide you with this resource to help you develop your project.
#   
# Project Description:
#   This project provides you with a really simple starting point for your project.
#   Use Flask to build and create your route tree and start serving your requests!
#   Be creative here and see what you can make.

from flask import(Flask,make_response,Response,abort,after_this_request,send_from_directory,flash,get_flashed_messages,url_for,send_file,jsonify,redirect,request,render_template,render_template_string,session,stream_template,stream_template_string,stream_with_context,get_template_attribute)

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, world! This is exposed to the world-wide internet!"

# run
app.run(
    host="0.0.0.0",
    port=80
)