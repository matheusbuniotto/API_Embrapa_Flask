from datetime import datetime
from flask import Flask, jsonify, Response, request
import requests
import csv
import io
import unicodedata
from collections import OrderedDict

app = Flask(__name__)
app.json.sort_keys = False

current_year = datetime.now().year

BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/download/"


def get_csv_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content, None
    except requests.RequestException as e:
        return None, f"Error fetching CSV: {str(e)}"


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


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/<csv_type>')
def get_csv(csv_type):
    url = f"{BASE_URL}{csv_type}.csv"
    csv_content, error = get_csv_content(url)

    if error:
        return jsonify({"error": error}), 400

    format_param = request.args.get('format', 'raw')
    year_param = request.args.get('year')

    # Determine the delimiter based on the CSV type
    delimiter = '\t' if csv_type in ['ProcessaAmericanas', 'ProcessaMesa', 'ProcessaSemclass'] else ';'

    if format_param == 'json':
        try:
            csv_file = io.StringIO(csv_content.decode('utf-8'))
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            headers = next(csv_reader)
            data = []

            for row in csv_reader:
                formatted_row = OrderedDict()
                formatted_row['id'] = row[0]
                formatted_row['control'] = replace_special_chars(remove_special_chars(row[1]))
                formatted_row['cultivar'] = replace_special_chars(remove_special_chars(row[2]))

                ano_data = OrderedDict()
                for i, year in enumerate(headers[3:], start=3):
                    if year.isdigit():
                        if not year_param or year == year_param:
                            ano_data[year] = row[i] if i < len(row) else ''

                formatted_row['year'] = ano_data

                # Set measure_type based on csv_type
                if csv_type.lower().startswith('processa'):
                    formatted_row["measure_type"] = 'kg'
                else:
                    formatted_row["measure_type"] = 'liter'

                # Only append the row if it has year data when year_param is specified
                if not year_param or ano_data:
                    data.append(formatted_row)

            return jsonify(data)
        except Exception as e:
            return jsonify({"error": f"Error parsing CSV: {str(e)}"}), 500
    else:
        return Response(
            csv_content,
            mimetype="text/csv",
            headers={"Content-Type": "text/plain"}
        )


def get_comercio():
    url = f"{BASE_URL}Comercio.csv"
    csv_content, error = get_csv_content(url)

    if error:
        return jsonify({"error": error}), 400

    format_param = request.args.get('format', 'raw')
    year_param = request.args.get('year')

    if format_param == 'json':
        try:
            csv_file = io.StringIO(csv_content.decode('utf-8'))
            csv_reader = csv.reader(csv_file, delimiter=';')
            headers = next(csv_reader)
            data = []

            for row in csv_reader:
                formatted_row = OrderedDict()
                formatted_row['id'] = row[0]
                formatted_row['control'] = replace_special_chars(remove_special_chars(row[1]))
                formatted_row['product'] = replace_special_chars(remove_special_chars(row[2]))

                ano_data = OrderedDict()
                for i, year in enumerate(headers[3:], start=3):
                    if year.isdigit():
                        if not year_param or year == year_param:
                            ano_data[year] = row[i] if i < len(row) else ''

                formatted_row['year'] = ano_data
                formatted_row["measure_type"] = 'liter'

                # Only append the row if it has year data when year_param is specified
                if not year_param or ano_data:
                    data.append(formatted_row)

            return jsonify(data)
        except Exception as e:
            return jsonify({"error": f"Error parsing CSV: {str(e)}"}), 500
    else:
        return Response(
            csv_content,
            mimetype="text/csv",
            headers={"Content-Type": "text/plain"}
        )


if __name__ == '__main__':
    app.run(debug=True)