from TextDBParser import TextDBParser
from EXCErrors import ExcErrors
from IODB import IOdb
from flask import Flask
from PLCDB import PLCdb
from flasgger import Swagger

def create_app(parsers):
    app = Flask(__name__)
    swagger = Swagger(app)

    # Register routes for each parser
    for parser in parsers:
        parser.create_routes(app)
    return app

#WebApp API Entry: http://localhost:5000/apidocs/

if __name__ == '__main__':
    # Create parser instances
    TextDB  = TextDBParser("TextDB")
    SPSfehl = ExcErrors("SPS_fehl")
    NCRfehl = ExcErrors("NCR_fehl")
    MMIfehl = ExcErrors("MMI_fehl")
    DIO_db  = IOdb("Text_DIO")
    PlcDB   = PLCdb("PlcDB")

    # Register parsers with the app
    app = create_app([TextDB, SPSfehl, NCRfehl, MMIfehl, DIO_db, PlcDB])
    app.run(debug=True)
