from TextDBParser import TextDBParser
from SPSFehlerDB import SPSFehlDB

from abc import ABC, abstractmethod
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from

def create_app(parsers):
    app = Flask(__name__)
    swagger = Swagger(app)

    # Register routes for each parser
    for parser in parsers:
        parser.create_routes(app)
    return app

# Example usage
if __name__ == '__main__':
    # Create parser instances
    TextDB = TextDBParser("TextDB")
    SPSfehl= SPSFehlDB("SPS_fehl")


    # Register parsers with the app
    app = create_app([TextDB, SPSfehl])
    app.run(debug=True)
