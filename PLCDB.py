from DataBaseParser import DatabaseParser
import os
import json
import re


class PLCdb(DatabaseParser):
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

        for full_key, value in json_obj.items():
            lines.append(f'{full_key}={value}')

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
        current_namespace = ""

        # Regex to recognize namespace header
        namespace_pattern = re.compile(r'\[.*namespace="(.+?)"\]')

        # Regex to recognice namespace reset
        namespace_reset_pattern = re.compile(r'\[Namespace Reset\]')
        namespace_reset_pattern2= re.compile(r'\[.*Message"(.+?)"\]')
        namespace_reset_pattern3= re.compile(r'\[.*MessageSource"(.+?)"\]')
        
        # Regex to recognice H - and L- numbers in TextDB
        special_key_pattern = re.compile(r'^[A-Za-z]\d+$|^\d+$')

        for line in lines:
            # check for namespace
            namespace_match = namespace_pattern.match(line.strip())


            if namespace_match:
                # extract namespace
                current_namespace = namespace_match.group(1)


            elif namespace_reset_pattern.match(line.strip()) or namespace_reset_pattern2.match(line.strip()) or namespace_reset_pattern3.match(line.strip()):
                # reset namespace
                current_namespace = ""
                


            elif '=' in line:
                # split key and value
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                # check for special handling
                if special_key_pattern.match(key):
                    # reset namespace when key is H - L - number
                    full_key = key
                else:
                    # add namespace
                    full_key = f"{current_namespace}.{key}" if current_namespace else key
                
                json_obj[full_key] = value

        # sort namespace keys alphabeticaly
        sorted_json_obj = {k: v for k, v in sorted(json_obj.items())}

        # write dict in JSON
        with open(database_as_json, 'w', encoding='latin-1') as json_file:
            json.dump(sorted_json_obj, json_file, indent=4, ensure_ascii=False)
        
        #send JSON as payload
        with open(database_as_json, 'r', encoding='latin-1') as text_file:
            self.payload=str(text_file.read())

        return f'Die JSON-Datei wurde erfolgreich erstellt: {database_as_json}'
    
    

if __name__=="__main__":
    TestParser=PLCdb("PLC_DB")

