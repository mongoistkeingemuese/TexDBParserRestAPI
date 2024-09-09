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
        database_path=os.path.normpath(database_path)
        json_path=os.path.normpath(json_path)
        new_database = database_path

        with open(json_path, 'r', encoding='utf-8') as file:
            json_obj = json.load(file)

        lines = []

        for full_key, value in json_obj.items():
            lines.append(f'{full_key}={value}')

        # Schreibe die Textzeilen in die Textdatei
        with open(new_database, 'w', encoding='utf-8') as text_file:
            text_file.write('\n'.join(lines))

        with open(new_database, 'r', encoding='utf-8') as text_file:
            self.payload=str(text_file.read())

        return f'Die Textdatei wurde erfolgreich erstellt: {new_database}'

    def create_json_from_database(self, database_path, json_path):
        database_path=os.path.normpath(database_path)
        json_path=os.path.normpath(json_path)
    
        database_name= os.path.basename(database_path)
        # Erstelle den Pfad zur JSON-Datei basierend auf dem Namen der Eingabedatei
        database_as_json = json_path

        # Lese die Textdatei ein
        with open(database_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Erstelle ein Dictionary, um die Daten zu speichern
        json_obj = {}
        current_namespace = ""

        # Regex zum Erkennen des Namespace Headers
        namespace_pattern = re.compile(r'\[.*namespace="(.+?)"\]')

        # Regex zum Erkennen des Namespace Resets
        namespace_reset_pattern = re.compile(r'\[Namespace Reset\]')
        
        # Regex zum Erkennen von Keys, die nur aus einer Zahl oder einem Buchstaben gefolgt von einer Zahl bestehen
        special_key_pattern = re.compile(r'^[A-Za-z]\d+$|^\d+$')

        for line in lines:
            # Überprüfen, ob die Zeile einen Namespace definiert
            namespace_match = namespace_pattern.match(line.strip())
            if namespace_match:
                # Extrahiere den Namespace
                current_namespace = namespace_match.group(1)

            elif namespace_reset_pattern.match(line.strip()):
                # Setze den Namespace zurück
                current_namespace = ""

            elif '=' in line:
                # Splitte jede Zeile in Key und Value
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                # Überprüfen, ob der Key den speziellen Kriterien entspricht
                if special_key_pattern.match(key):
                    # Wenn der Key aus einem Buchstaben und einer Zahl oder nur aus einer Zahl besteht,
                    # wird er keinem Namespace zugeordnet und bleibt unverändert
                    full_key = key
                else:
                    # Andernfalls wird der Namespace hinzugefügt
                    full_key = f"{current_namespace}.{key}" if current_namespace else key
                
                json_obj[full_key] = value
        # Sortiere die Einträge alphabetisch nach Key
        sorted_json_obj = {k: v for k, v in sorted(json_obj.items())}

        # Schreibe das Dictionary in die JSON-Datei
        with open(database_as_json, 'w', encoding='utf-8') as json_file:
            json.dump(sorted_json_obj, json_file, indent=4, ensure_ascii=False)
        
        with open(database_as_json, 'r', encoding='utf-8') as text_file:
            self.payload=str(text_file.read())

        return f'Die JSON-Datei wurde erfolgreich erstellt: {database_as_json}'
 
    def merge_json_into_translation_excel(self, json_path, excel_path, language_description):
        excel_path=os.path.normpath(excel_path)
        json_path=os.path.normpath(json_path)

        # Prüfe, ob die bestehende Excel-Datei existiert und nicht leer ist
        if os.path.exists(excel_path) and os.path.getsize(excel_path) > 0:
            # Lese die bestehende Excel-Datei ein
            df_existing = pd.read_excel(excel_path, engine='openpyxl')
            # Drucke die Spaltennamen zur Fehlersuche
            print(f"Spaltennamen in der bestehenden Excel-Datei: {df_existing.columns.tolist()}")
        else:
            # Initialisiere ein leeres DataFrame, wenn die Datei nicht existiert oder leer ist
            df_existing = pd.DataFrame(columns=['Key', 'Value'])
            print("Die bestehende Excel-Datei existiert nicht oder ist leer. Ein neues DataFrame wird erstellt.")

        # Lese die neue JSON-Datei ein
        with open(json_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        # Erstelle ein DataFrame aus der neuen JSON-Daten
        df_new = pd.DataFrame(list(json_data.items()), columns=['Key', language_description])

        if df_existing.empty:
            # Wenn das bestehende DataFrame leer ist, erstelle eine neue Tabelle mit den neuen Daten
            df_result = df_new
        else:
            # Überprüfe, ob die 'Key' Spalte vorhanden ist
            if 'Key' not in df_existing.columns:
                raise KeyError("Die Spalte 'Key' fehlt in der bestehenden Excel-Datei.")
            
            # Setze den Key als Index für beide DataFrames, um sie korrekt zu kombinieren
            df_existing.set_index('Key', inplace=True)
            df_new.set_index('Key', inplace=True)

            # Kombiniere die beiden DataFrames
            df_combined = df_existing.combine_first(df_new)

            # Setze den Index zurück, um die 'Key'-Spalte als normale Spalte zu behalten
            df_result = df_combined.reset_index()

        # Konvertiere die Key-Spalte in Strings, um Vergleichsfehler bei der Sortierung zu vermeiden
        df_result['Key'] = df_result['Key'].astype(str)

        # Sortiere das DataFrame alphabetisch nach der Key-Spalte
        df_result.sort_values(by='Key', inplace=True)

        # Speichere das aktualisierte DataFrame zurück in eine Excel-Datei
        df_result.to_excel(excel_path, index=False, engine='openpyxl')

        self.payload=str("<3 kannst die Excel als String ehh nicht lesen :P")
        
        return f'Die Excel-Datei wurde erfolgreich erstellt/aktualisiert: {excel_path}'

    def get_json_from_translation_excel(self, json_path, excel_path, language_description):
           
        excel_path=os.path.normpath(excel_path)
        json_path=os.path.normpath(json_path)

        # Lese die Excel-Datei ein
        df = pd.read_excel(excel_path, engine='openpyxl')
        key_column='Key'
        
        # Überprüfe, ob die angegebenen Spalten vorhanden sind
        if key_column not in df.columns or language_description not in df.columns:
            raise ValueError(f"Die angegebenen Spalten '{key_column}' oder '{language_description}' existieren nicht in der Excel-Datei.")
        
        # Entferne Zeilen, in denen entweder der Key oder der Value NaN ist
        df_cleaned = df.dropna(subset=[key_column, language_description])
        
        # Erstelle ein Dictionary aus den angegebenen Spalten
        json_data = dict(zip(df_cleaned[key_column], df_cleaned[language_description]))
        
        # Schreibe das Dictionary in die JSON-Datei
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)

        with open(json_path, 'r', encoding='utf-8') as text_file:
            self.payload=str(text_file.read())
        
        return f'Die JSON-Datei wurde erfolgreich erstellt: {json_path}' 


if __name__=="__main__":
    TestParser=TextDBParser("TextDB")

