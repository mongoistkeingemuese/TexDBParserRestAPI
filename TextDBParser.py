from DataBaseParser import DatabaseParser
import os
import json
import re
from collections import defaultdict
import pandas as pd

class TextDBParser(DatabaseParser):
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

        for full_key, value in json_obj.items():
            lines.append(f'{full_key}={value}')

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

        # Regex to recognize namespace header
        namespace_pattern = re.compile(r'\[.*namespace="(.+?)"\]')

        # Regex to recognice namespace reset
        namespace_reset_pattern = re.compile(r'\[Namespace Reset\]')
        
        # Regex to recognice H - and L- numbers in TextDB
        special_key_pattern = re.compile(r'^[A-Za-z]\d+$|^\d+$')

        for line in lines:
            # check for namespace
            namespace_match = namespace_pattern.match(line.strip())
            if namespace_match:
                # extract namespace
                current_namespace = namespace_match.group(1)

            elif namespace_reset_pattern.match(line.strip()):
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
        with open(database_as_json, 'w', encoding='utf-8') as json_file:
            json.dump(sorted_json_obj, json_file, indent=4, ensure_ascii=False)
        
        #send JSON as payload
        with open(database_as_json, 'r', encoding='utf-8') as text_file:
            self.payload=str(text_file.read())

        return f'Die JSON-Datei wurde erfolgreich erstellt: {database_as_json}'
 
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


if __name__=="__main__":
    TestParser=TextDBParser("TextDB")

