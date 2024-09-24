from abc import ABC, abstractmethod
from flask import request, jsonify
from flasgger import swag_from
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
                            'excel_path': {'type': 'string', 'example': f'C:\\Users\\martin.mellueh\\Documents\\Project\\Develop\\PythonParserRESTAPI\\TextDB_translation.xlsx'},
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
                            'excel_path': {'type': 'string', 'example':f'C:\\Users\\martin.mellueh\\Documents\\Project\\Develop\\PythonParserRESTAPI\\TextDB_translation.xlsx'},
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
        excel_path = os.path.normpath(excel_path)
        json_path = os.path.normpath(json_path)
        sheet_name = self.name

        if not os.path.exists(excel_path):
            #create new Dataframe
            df_existing = pd.DataFrame(columns=['Key', 'Value'])
            # Erstelle eine neue Excel-Datei mit dem leeren DataFrame
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                df_existing.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"Excel-Datei wurde erstellt: {excel_path}")
            print(f"Neues Sheet '{sheet_name}' wurde hinzugefügt.")
        else:
            # load ecxal sheet
            try:
                df_existing = pd.read_excel(excel_path, sheet_name=sheet_name, engine='openpyxl')
                print(f"Spaltennamen im bestehenden Excel-Sheet '{sheet_name}': {df_existing.columns.tolist()}")
            except ValueError:
                # if sheet does not exist, create new one
                df_existing = pd.DataFrame(columns=['Key', 'Value'])
                print(f"Sheet '{sheet_name}' existiert nicht. Ein neues Sheet wird erstellt.")


        #load Json data
        with open(json_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        df_new = pd.DataFrame(list(json_data.items()), columns=['Key', language_description])

        # Merge with existing data
        if df_existing.empty:
            df_result = df_new
        else:
            if 'Key' not in df_existing.columns:
                raise KeyError("Die Spalte 'Key' fehlt im bestehenden Excel-Sheet.")
            
            df_existing.set_index('Key', inplace=True)
            df_new.set_index('Key', inplace=True)
            df_combined = df_existing.combine_first(df_new)
            df_result = df_combined.reset_index()

        df_result['Key'] = df_result['Key'].astype(str)

        if sheet_name == "TextDB":
            df_result.sort_values(by='Key', inplace=True)

        # save data in excel
        # if sheet exists, load sheet
        with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            if os.path.exists(excel_path):
                book = pd.ExcelFile(excel_path, engine='openpyxl')
                for existing_sheet_name in book.sheet_names:
                    if existing_sheet_name != sheet_name:
                        df_existing_sheet = pd.read_excel(excel_path, sheet_name=existing_sheet_name, engine='openpyxl')
                        df_existing_sheet.to_excel(writer, sheet_name=existing_sheet_name, index=False)
            # write sheet
            df_result.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f'Die Excel-Datei wurde erfolgreich aktualisiert: {excel_path}')
        return f'Excel-Datei wurde erfolgreich aktualisiert: {excel_path}'

    def get_json_from_translation_excel(self, json_path, excel_path, language_description):
           
        excel_path=os.path.normpath(excel_path)
        json_path=os.path.normpath(json_path)

        # read excel dataframe
        df = pd.read_excel(excel_path, engine='openpyxl', sheet_name=self.name)
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


 
    
