from DataBaseParser import DatabaseParser
import os
import json
import re


class IOdb(DatabaseParser):
    def __init__(self, name):
        super().__init__(name)

    def create_database_from_json(self, database_path, json_path):

        #get key+value from JSON and create TextDB
        database_path=os.path.normpath(database_path)
        json_path=os.path.normpath(json_path)
        new_database = database_path

        with open(json_path, 'r', encoding='utf-8') as file:
            json_obj = json.load(file)

        lines = []
        current_section = ""
        current_namespace = ""

        for key, value in json_obj.items():
            # Split the key to extract section, namespace, and actual key
            key_parts = key.split('.')
            if len(key_parts) == 3:
                section, namespace, actual_key = key_parts
            elif len(key_parts) == 2:
                section, actual_key = key_parts
                namespace = ""
            else:
                section = ""
                namespace = ""
                actual_key = key_parts[0]

            # Add section line if section changes
            if section and section != current_section:
                current_section = section
                lines.append(f"[{current_section}]")
                current_namespace = ""  # Reset namespace when section changes
            
            # Add namespace line if namespace changes
            if namespace and namespace != current_namespace:
                current_namespace = namespace
                lines.append(f"[-{current_namespace}-]")

            
            
            # Add the key-value pair line
            lines.append(f"{actual_key}={value}")

        with open(new_database, 'w', encoding='utf-8') as text_file:
            text_file.write('\n'.join(lines))

        #send database as payload
        with open(new_database, 'r', encoding='utf-8') as text_file:
            self.payload=str(text_file.read())

        return f'text database was created successfully  {new_database}'

    def create_json_from_database(self, database_path, json_path):
        database_path=os.path.normpath(database_path)
        json_path=os.path.normpath(json_path)
    
        database_name= os.path.basename(database_path)

        database_as_json = json_path

        with open(database_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        json_obj = {}
        current_namespace = ""
        current_section = ""

        for line in lines:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or '//' in line:
                continue
            
            # Handle sections
            section_match = re.match(r'\[([A-Z]+)\]', line)
            if section_match:
                current_section = section_match.group(1)
                continue
            
            # Handle namespaces
            namespace_match = re.match(r'\[\-(.+)\]', line)
            if namespace_match:
                current_namespace = namespace_match.group(1).strip()
                continue

            # Handle key-value pairs
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                if current_section:
                    if current_namespace:
                        json_key = f"{current_section}.{current_namespace}.{key}"
                    else:
                        json_key = f"{current_section}.{key}" 
                else:
                    json_key = f"{current_namespace}.{key}"
                json_obj[json_key] = value
                
        # write dict in JSON
        with open(database_as_json, 'w', encoding='utf-8') as json_file:
            json.dump(json_obj, json_file, indent=4, ensure_ascii=False)
        
        #send JSON as payload
        with open(database_as_json, 'r', encoding='utf-8') as text_file:
            self.payload=str(text_file.read())

        return f'Die JSON-Datei wurde erfolgreich erstellt: {database_as_json}'
 
    

if __name__=="__main__":
    TestParser=IOdb("SPS_fehl")

