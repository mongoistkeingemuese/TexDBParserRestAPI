from abc import ABC, abstractmethod
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from


class DatabaseParser(ABC):
    def __init__(self, name):
        self.name = name
        self.payload=''
        app=self.create_app()
        app.run(debug=True)

    def execute_method(self, method_name, data):
        # process child class functions dynamicly
        try:
            method = getattr(self, method_name, None)
            if not method:
                raise ValueError(f"Methode '{method_name}' not found")
            
            result = method(**data)
            return jsonify({'status': 'success', 'result': result, 'payload':f'{self.payload}'}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    def create_app(self):
        #create RestAPI and Webinterface 
        app = Flask(self.name)
        swagger = Swagger(app)

        @app.route(f'/{self.name}/create_json_from_database', methods=['POST'])
        @swag_from({
            'parameters': [
                {
                    'name': 'body',
                    'in': 'body',
                    'required': True,
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'database_path': {'type': 'string', 'example': r'C:\Users\martin.mellueh\Documents\Project\Develop\PythonParserRESTAPI\TextDB.db'},
                            'json_path': {'type': 'string', 'example': r'C:\Users\martin.mellueh\Documents\Project\Develop\PythonParserRESTAPI\TextDBParser\TextDB.json'}
                        }
                    }
                }
            ],
            'responses': {
                '200': {
                    'description': 'Method executed successfully',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'result': {'type': 'string'}
                        }
                    }
                },
                '500': {
                    'description': 'Error occurred',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        })
        def create_json_from_database():
            data = request.json
            return self.execute_method('create_json_from_database', data)

        @app.route(f'/{self.name}/create_database_from_json', methods=['POST'])
        @swag_from({
            'parameters': [
                {
                    'name': 'body',
                    'in': 'body',
                    'required': True,
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'database_path': {'type': 'string', 'example': r'C:\Users\martin.mellueh\Documents\Project\Develop\PythonParserRESTAPI\TextDBParser\TextDB_from_JSON.db'},
                            'json_path': {'type': 'string', 'example': r'C:\Users\martin.mellueh\Documents\Project\Develop\PythonParserRESTAPI\TextDBParser\TextDB.json'}
                        }
                    }
                }
            ],
            'responses': {
                '200': {
                    'description': 'Method executed successfully',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'result': {'type': 'string'}
                        }
                    }
                },
                '500': {
                    'description': 'Error occurred',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        })
        def create_database_from_json():
            data = request.json
            return self.execute_method('create_database_from_json', data)

        @app.route(f'/{self.name}/merge_json_into_translation_excel', methods=['POST'])
        @swag_from({
            'parameters': [
                {
                    'name': 'body',
                    'in': 'body',
                    'required': True,
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'json_path': {'type': 'string', 'example': r'C:\Users\martin.mellueh\Documents\Project\Develop\PythonParserRESTAPI\TextDBParser\TextDB.json'},
                            'excel_path': {'type': 'string', 'example': r'C:\Users\martin.mellueh\Documents\Project\Develop\PythonParserRESTAPI\translation_excel.xlsx'},
                            'language_description': {'type': 'string', 'example': 'deutsch'}
                        }
                    }
                }
            ],
            'responses': {
                '200': {
                    'description': 'Method executed successfully',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'result': {'type': 'string'}
                        }
                    }
                },
                '500': {
                    'description': 'Error occurred',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        })
        def merge_json_into_translation_excel():
            data = request.json
            return self.execute_method('merge_json_into_translation_excel', data)

        @app.route(f'/{self.name}/get_json_from_translation_excel', methods=['POST'])
        @swag_from({
            'parameters': [
                {
                    'name': 'body',
                    'in': 'body',
                    'required': True,
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'json_path': {'type': 'string', 'example': r'C:\Users\martin.mellueh\Documents\Project\Develop\PythonParserRESTAPI\TextDBParser\JSON_from_excel.json'},
                            'excel_path': {'type': 'string', 'example': r'C:\Users\martin.mellueh\Documents\Project\Develop\PythonParserRESTAPI\translation_excel.xlsx'},
                            'language_description': {'type': 'string', 'example': 'deutsch'}
                        }
                    }
                }
            ],
            'responses': {
                '200': {
                    'description': 'Method executed successfully',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'result': {'type': 'string'}
                        }
                    }
                },
                '500': {
                    'description': 'Error occurred',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        })
        def get_json_from_translation_excel():
            data = request.json
            return self.execute_method('get_json_from_translation_excel', data)

        return app
       
    @abstractmethod
    def create_json_from_database(self, database_path, json_path):
        pass

    @abstractmethod
    def create_database_from_json(self, database_path, json_path):
        pass

    @abstractmethod
    def merge_json_into_translation_excel(self, json_path, excel_path, language_description):
        pass

    @abstractmethod
    def get_json_from_translation_excel(self, json_path, excel_path, language_description):
        pass 

 
    
