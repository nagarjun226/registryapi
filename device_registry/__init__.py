# import markdown to convert to html
import markdown

# import flask, a lightweight web framework
from flask import Flask, g

# flask_restful's parser
from flask_restful import Resource, Api, reqparse

# import shelve for object persistence
import shelve

import os
from datetime import datetime

# Create an instance of Flask App
app = Flask(__name__)

# Create the API
api = Api(app)

# Create a connection from flask to the db we will use. We are using shelve
# for object persistence here
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = shelve.open("devices.db")
    return db

# Tear down the db when the app shuts down
@app.teardown_appcontext
def teardown_db(excetion):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    """Display Documentation"""

    # Open README.md
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
        # Read the content of the file
        content = markdown_file.read()

        # Covert to HTML
        return markdown.markdown(content)

# Using flask REstful to write APIs. 
# Create a class for each endpoint
# Create a function for each method

class DeviceList(Resource):
    def get(self):
        # `GET /devices`
        shelf = get_db() # Fetch the DB
        keys = list(shelf.keys())

        devices = []

        for key in keys:
            devices.append(shelf[key])
        
        return {'message': 'Success', 'data': devices}, 200

    def post(self):
        parser = reqparse.RequestParser()

        # Sanity check for arguments
        parser.add_argument('device_id', required=False)
        parser.add_argument('device_name', required=True)
        parser.add_argument('device_type', required=False)
        parser.add_argument('controller_gateway', required=True)
        
        # Parse arguments into an object
        args = parser.parse_args()

        now = datetime.now()
        if args['device_id'] is None:
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            args['device_id'] = str(hash(args['device_name']+date_time))
        
        shelf = get_db()
        shelf[args['device_id']] = args

        return {'message': 'Device Registered', 'data': args}, 201

class Device(Resource):
    def get(self, device_id):
        shelf = get_db()

        # if key does not exist in the store
        if not (device_id in shelf):
            return {'message': 'Device not found', 'data': {}}, 404
        
        return {'message': 'Device found', 'data': shelf[device_id]}, 200

    def delete(self, device_id):
        shelf = get_db()

        # if key does not exist in the store
        if not (device_id in shelf):
            return {'message': 'Device not found', 'data': {}}, 404
        
        del shelf[device_id]

        return '', 204

# Adding end points
api.add_resource(DeviceList, '/devices') 
api.add_resource(Device, '/devices/<string:device_id>') 