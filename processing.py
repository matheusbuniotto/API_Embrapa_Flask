import csv
import io
from collections import OrderedDict
import requests
import unicodedata


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

def get_csv_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content.decode('utf-8'), None
    except requests.RequestException as e:
        return None, f"Error fetching CSV: {str(e)}"

# Function to fetch CSV content from local file
def get_csv_content_from_local(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read(), None
    except FileNotFoundError as e:
        return None, f"Error: File not found - {str(e)}"


# Function to process CSV and return structured data
def process_csv_content(csv_content_tuple, delimiter=';'):
    csv_content, error = csv_content_tuple
    if error:
        return {"error": error}  # Handle the error appropriately

    csv_file = io.StringIO(csv_content)
    csv_reader = csv.reader(csv_file, delimiter=delimiter)

    headers = next(csv_reader)

    data = []
    for row in csv_reader:
        formatted_row = OrderedDict()
        formatted_row['id'] = row[0]
        formatted_row['control'] = replace_special_chars(remove_special_chars(row[1]))
        formatted_row['product'] = replace_special_chars(remove_special_chars(row[2]))

        yearly_data = OrderedDict()
        for year, value in zip(headers[3:], row[3:]):
            yearly_data[year] = value

        formatted_row['yearly_data'] = yearly_data
        data.append(formatted_row)

    return data

