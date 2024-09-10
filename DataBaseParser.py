from abc import ABC, abstractmethod
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
import pandas as pd
import os
import json


class DatabaseParser(ABC):
    def __init__(self, name):
        self.name = name
        self.payload=''
        

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

    def create_routes(self, app):
        @app.route(f'/{self.name}/create_json_from_database', methods=['POST'], endpoint=f'{self.name}_create_json_from_database')
        @swag_from({
            'parameters': [
                {
                    'name': 'body',
                    'in': 'body',
                    'required': True,
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'database_path': {'type': 'string', 'example':f'C:\\Users\\martin.mellueh\\Documents\\Project\\Develop\\PythonParserRESTAPI\\{self.name}.db'},
                            'json_path': {'type': 'string', 'example': f'C:\\Users\\martin.mellueh\\Documents\\Project\\Develop\\PythonParserRESTAPI\\TextDBParser\\{self.name}.json'}
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

        @app.route(f'/{self.name}/create_database_from_json', methods=['POST'],endpoint=f'{self.name}_create_database_from_json')
        @swag_from({
            'parameters': [
                {
                    'name': 'body',
                    'in': 'body',
                    'required': True,
                    'schema': {
                        'type': 'object',
                        'properties': {
                           'database_path': {'type': 'string', 'example': f'C:\\Users\\martin.mellueh\\Documents\\Project\\Develop\\PythonParserRESTAPI\\TextDBParser\\{self.name}_from_json.db'},
                            'json_path': {'type': 'string', 'example': f'C:\\Users\\martin.mellueh\\Documents\\Project\\Develop\\PythonParserRESTAPI\\TextDBParser\\{self.name}.json'}
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

        @app.route(f'/{self.name}/merge_json_into_translation_excel', methods=['POST'], endpoint=f'{self.name}_merge_json_into_translation_excel')
        @swag_from({
            'parameters': [
                {
                    'name': 'body',
                    'in': 'body',
                    'required': True,
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'json_path': {'type': 'string', 'example': f'C:\\Users\\martin.mellueh\\Documents\\Project\\Develop\\PythonParserRESTAPI\\TextDBParser\\{self.name}.json'},
                            'excel_path': {'type': 'string', 'example': f'C:\\Users\\martin.mellueh\\Documents\\Project\\Develop\\PythonParserRESTAPI\\{self.name}_translation.xlsx'},
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

        @app.route(f'/{self.name}/get_json_from_translation_excel', methods=['POST'], endpoint=f'{self.name}_get_json_from_translation_excel')
        @swag_from({
            'parameters': [
                {
                    'name': 'body',
                    'in': 'body',
                    'required': True,
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'json_path': {'type': 'string', 'example': f'C:\\Users\\martin.mellueh\\Documents\\Project\\Develop\\PythonParserRESTAPI\\TextDBParser\\{self.name}.json'},
                            'excel_path': {'type': 'string', 'example':f'C:\\Users\\martin.mellueh\\Documents\\Project\\Develop\\PythonParserRESTAPI\\{self.name}_translation.xlsx'},
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
    
    def merge_json_into_translation_excel(self, json_path, excel_path, language_description):
        excel_path=os.path.normpath(excel_path)
        json_path=os.path.normpath(json_path)

        if os.path.exists(excel_path) and os.path.getsize(excel_path) > 0:
            # read dataframe from excel
            df_existing = pd.read_excel(excel_path, engine='openpyxl')
            # print existing column descriptions
            print(f"Spaltennamen in der bestehenden Excel-Datei: {df_existing.columns.tolist()}")
        else:
            # initialize excel sheet
            df_existing = pd.DataFrame(columns=['Key', 'Value'])
            print("ecxel file does not exist or is empty ... new file was created")

        with open(json_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        # create new dataframe from JSON
        df_new = pd.DataFrame(list(json_data.items()), columns=['Key', language_description])

        if df_existing.empty:
            # create empty dataframe  
            df_result = df_new
        else:
            #check for Key column
            if 'Key' not in df_existing.columns:
                raise KeyError("Die Spalte 'Key' fehlt in der bestehenden Excel-Datei.")
            
            # set key column active to combine dataframes
            df_existing.set_index('Key', inplace=True)
            df_new.set_index('Key', inplace=True)

            # combine dataframes
            df_combined = df_existing.combine_first(df_new)

            # reset index to keep "Key" column
            df_result = df_combined.reset_index()

        # convert Key column to string to exclude comparing errors
        df_result['Key'] = df_result['Key'].astype(str)

        # sort Keys alphabeticaly
        df_result.sort_values(by='Key', inplace=True)

        # save active dataframe in excel
        df_result.to_excel(excel_path, index=False, engine='openpyxl')

        self.payload=str("<3 cant read excel as sting anyway :P")
        
        return f'Excel file was created/updated successfully: {excel_path}'

    def get_json_from_translation_excel(self, json_path, excel_path, language_description):
           
        excel_path=os.path.normpath(excel_path)
        json_path=os.path.normpath(json_path)

        # read excel dataframe
        df = pd.read_excel(excel_path, engine='openpyxl')
        key_column='Key'
        
        # check columns for language description
        if key_column not in df.columns or language_description not in df.columns:
            raise ValueError(f"Column '{key_column}' or '{language_description}' does not exist in excel file")
        
        # remove Key and Values when NaN  
        df_cleaned = df.dropna(subset=[key_column, language_description])
        
        # create dict from column
        json_data = dict(zip(df_cleaned[key_column], df_cleaned[language_description]))
        
        # write dict in JSON
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)

        # send JSON as payload
        with open(json_path, 'r', encoding='utf-8') as json_file:
            self.payload=str(json_file.read())
        
        return f'JSON file was created successfully: {json_path}' 

       
    @abstractmethod
    def create_json_from_database(self, database_path, json_path):
        pass

    @abstractmethod
    def create_database_from_json(self, database_path, json_path):
        pass


 
    
