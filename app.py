from flask import Flask, jsonify, request
from processing import get_csv_content, get_csv_content_from_local, process_csv_content
import os
app = Flask(__name__)

BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/download/"
LOCAL_CSV_DIR = "raw_data"
@app.route('/api/Comercio', methods=['GET'])
def get_comercio_data():
    url = f"{BASE_URL}Comercio.csv"

    # Fetch the CSV content
    csv_content_tuple = get_csv_content(url)

    # Process the CSV content into JSON
    data = process_csv_content(csv_content_tuple)

    # Return the processed data as a JSON response
    return jsonify(data)
@app.route('/api/Producao', methods=['GET'])
def get_producao_data():
    # Check if the 'use_local' query parameter is passed
    use_local = request.args.get('use_local', 'false').lower() == 'true'

    # Define the CSV file name
    csv_filename = "Producao.csv"

    if use_local:
        # Use the CSV file from the local directory
        filepath = os.path.join(LOCAL_CSV_DIR, csv_filename)
        csv_content_tuple = get_csv_content_from_local(filepath)
    else:
        # Fetch the CSV file from the URL
        url = f"{BASE_URL}{csv_filename}"
        csv_content_tuple = get_csv_content(url)

    # Process the CSV content into JSON
    data = process_csv_content(csv_content_tuple)

    # Return the processed data as a JSON response
    return jsonify(data)

@app.route('/api/ProcessaViniferas', methods=['GET'])
def get_processa_data():
    # Check if the 'use_local' query parameter is passed
    use_local = request.args.get('use_local', 'false').lower() == 'true'

    # Define the CSV file name
    csv_filename = "ProcessaViniferas.csv"

    if use_local:
        # Use the CSV file from the local directory
        filepath = os.path.join(LOCAL_CSV_DIR, csv_filename)
        csv_content_tuple = get_csv_content_from_local(filepath)
    else:
        # Fetch the CSV file from the URL
        url = f"{BASE_URL}{csv_filename}"
        csv_content_tuple = get_csv_content(url)

    # Process the CSV content into JSON
    data = process_csv_content(csv_content_tuple)

    # Return the processed data as a JSON response
    return jsonify(data)

@app.route('/api/processa/<file_type>', methods=['GET'])
def get_processa_files(file_type):
    # Check if the 'use_local' query parameter is passed
    use_local = request.args.get('use_local', 'false').lower() == 'true'

    # Define the CSV file name based on the file_type
    csv_filename = f"Processa{file_type.capitalize()}.csv"

    if use_local:
        # Use the CSV file from the local directory
        filepath = os.path.join(LOCAL_CSV_DIR, csv_filename)
        csv_content_tuple = get_csv_content_from_local(filepath)
    else:
        # Fetch the CSV file from the URL
        url = f"{BASE_URL}{csv_filename}"
        csv_content_tuple = get_csv_content(url)

    # Process the CSV content into JSON
    data = process_csv_content(csv_content_tuple)

    # Return the processed data as a JSON response
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

