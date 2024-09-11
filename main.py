from TextDBParser import TextDBParser
from EXCErrors import ExcErrors
from IODB import IOdb

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
    TextDB  = TextDBParser("TextDB")
    SPSfehl = ExcErrors("SPS_fehl")
    NCRfehl = ExcErrors("NCR_fehl")
    MMIfehl = ExcErrors("MMI_fehl")
    DIO_db     = IOdb("DIO")

    # Register parsers with the app
    app = create_app([TextDB, SPSfehl, NCRfehl, MMIfehl, DIO_db])
    app.run(debug=True)
