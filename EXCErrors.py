from DataBaseParser import DatabaseParser
import os
import json


class ExcErrors(DatabaseParser):
    def __init__(self, name):
        super().__init__(name)

    def create_database_from_json(self, database_path, json_path):

        #get key+value from JSON and create TextDB
        database_path=os.path.normpath(database_path)
        json_path=os.path.normpath(json_path)
        new_database = database_path

        with open(json_path, 'r', encoding='latin-1') as file:
            json_obj = json.load(file)

        lines = []

        for key, value in json_obj.items():
            if '#Info' in str(key):
                lines.append(f'{key}={value}')
            else:               
                lines.append(f'"{key}","{value}",""')

        with open(new_database, 'w', encoding='latin-1') as text_file:
            text_file.write('\n'.join(lines))

        #send database as payload
        with open(new_database, 'r', encoding='latin-1') as text_file:
            self.payload=str(text_file.read())

        return f'text database was created successfully  {new_database}'

    def create_json_from_database(self, database_path, json_path):
        database_path=os.path.normpath(database_path)
        json_path=os.path.normpath(json_path)
    
        database_name= os.path.basename(database_path)

        database_as_json = json_path

        with open(database_path, 'r', encoding='latin-1') as file:
            lines = file.readlines()

        json_obj = {}
    

        for line in lines:
            line = line.strip()
            if '#Info:' in line:
                key, value = line.split('=', 1)
            else:
                # Key-Value Parsing
                parts = line.split('","')
                if len(parts)>=2:
                    key = parts[0].strip('"')
                    value = parts[1]
            json_obj[key]=value
                
        # write dict in JSON
        with open(database_as_json, 'w', encoding='latin-1') as json_file:
            json.dump(json_obj, json_file, indent=4, ensure_ascii=False)
        
        #send JSON as payload
        with open(database_as_json, 'r', encoding='latin-1') as text_file:
            self.payload=str(text_file.read())

        return f'Die JSON-Datei wurde erfolgreich erstellt: {database_as_json}'
 
    

if __name__=="__main__":
    TestParser=ExcErrors("SPS_fehl")

