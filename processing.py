import csv
import io
from collections import OrderedDict
import requests
import os
import unicodedata

# Funções da tratamento de strings para padronização
def remove_special_chars(text):
    normalized = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in normalized if not unicodedata.combining(c))

def replace_special_chars(text):
    replacements = {
        'ç': 'c', 'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e', 'í': 'i', 'ó': 'o', 'ô': 'o',
        'õ': 'o', 'ú': 'u', 'ü': 'u'
    }
    return ''.join(replacements.get(c.lower(), c) for c in text)

# Função que faz um get no csv disponibilizado no site da embrapa
def get_csv_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content.decode('utf-8'), url, None
    except requests.RequestException as e:
        return None, url, f"Error fetching CSV: {str(e)}"

# Função que consome o csv local na pasta raw_data, caso o request da API seja feito com esse paramêtro
def get_csv_content_from_local(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read(), filepath, None
    except FileNotFoundError as e:
        return None, filepath, f"Error: File not found - {str(e)}"

# Função genérica para processamento de todos os CSVs, independente de seu nome ou origem (local ou direto da embrapa)
def process_csv_content(csv_content_tuple):
    csv_content, filepath, error = csv_content_tuple

    # Get the file name from the filepath
    file_name = os.path.basename(filepath) if filepath else ''
    file_name_without_extension = os.path.splitext(file_name)[0]

    # Define o tipo de delimitador do CSV em casos específicos é necessário ser \t

    delimiter = '\t' if file_name_without_extension in ['ProcessaAmericanas', 'ProcessaMesa', 'ProcessaSemclass'] else ';'
    csv_file = io.StringIO(csv_content)
    csv_reader = csv.reader(csv_file, delimiter=delimiter)

    headers = next(csv_reader, None)

    data = []
    for row in csv_reader:
        formatted_row = OrderedDict()
        formatted_row['id'] = row[0]

        # Check if the file name starts with 'Exp' or 'Imp'
        if file_name_without_extension.startswith(('Exp', 'Imp')):
            formatted_row['country'] = replace_special_chars(remove_special_chars(row[1]))
            formatted_row['product'] = file_name_without_extension
        else:
            formatted_row['name'] = replace_special_chars(remove_special_chars(row[1]))
            formatted_row['product'] = replace_special_chars(remove_special_chars(row[2]))

        yearly_data = OrderedDict()
        for year, value in zip(headers[3:], row[3:]):
            yearly_data[year] = value

        formatted_row['year'] = yearly_data
        data.append(formatted_row)

    return data