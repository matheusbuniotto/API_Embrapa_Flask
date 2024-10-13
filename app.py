from flask import Flask, jsonify, request
from processing import get_csv_content, get_csv_content_from_local, process_csv_content
import os
app = Flask(__name__)

BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/download/"
LOCAL_CSV_DIR = "raw_data"

@app.route('/api/status', methods=['GET'])
def show_status():
    return ('The API is running. Check the docummentation at /api/docs \n' 
            'PT-BR: A API está ativa. Consulte a documentação em /api/docs')
@app.route('/api/docs', methods=['GET'])
def api_docs():
    """
    Documentação dos endpoints disponíveis na API.
    """
    docs = {
        "status": {
            "method": "GET",
            "description": "Verificar se a API está em execução.",
            "endpoint": "/api/status"
        },
        "Comercio": {
            "method": "GET",
            "description": ("Busca e processa o arquivo 'Comercio.csv' tanto do sistema local "
                            "ou da URL remota dependendo do parâmetro 'use_local'."),
            "endpoint": "/api/Comercio",
            "query_params": {
                "use_local": "Opcional, definir como 'true' para buscar o arquivo CSV localmente."
            }

        },
        "Produção": {
            "method": "GET",
            "description": ("Busca e processa o arquivo 'Producao.csv' tanto do sistema local "
                            "ou da URL remota dependendo do parâmetro 'use_local'."),
            "endpoint": "/api/Producao",
            "query_params": {
                "use_local": "Opcional, definir como 'true' para buscar o arquivo CSV localmente."
            }
        },
        "Processamento": {
            "method": "GET",
            "description": ("Busca e processa arquivos CSV do tipo 'ProcessaFile_type.csv' tanto do "
                            "sistema local ou da URL remota dependendo do parâmetro 'use_local'."),
            "endpoint": "/api/processa/file_type",
            "query_params": {
                "use_local": "Opcional, definir como 'true' para buscar o arquivo CSV localmente."
            },
            "path_params": {
                "file_type": "Obrigatório, o tipo de arquivo a ser buscado (ex.: 'Frescas', 'Passas', 'Suco', 'Vinhos')."
            }
        },
        "Exportação": {
            "method": "GET",
            "description": ("Busca e processa arquivos CSV do tipo 'ExpFile_type.csv' tanto do sistema local "
                            "ou da URL remota dependendo do parâmetro 'use_local'."),
            "endpoint": "/api/exp/file_type",
            "query_params": {
                "use_local": "Opcional, definir como 'true' para buscar o arquivo CSV localmente."
            },
            "path_params": {
                "file_type": "Obrigatório, o tipo de arquivo a ser consultado (ex.: 'Uva', 'Suco', 'Espumantes', 'VInho')."
            }
        },
        "Importação": {
            "method": "GET",
            "description": ("Busca e processa arquivos CSV do tipo 'ImpFile_Type.csv' tanto do sistema local "
                            "ou da URL remota dependendo do parâmetro 'use_local'."),
            "endpoint": "/api/imp/file_type",
            "query_params": {
                "use_local": "Opcional, definir como 'true' para buscar o arquivo CSV localmente."
            },
            "path_params": {
                "file_type": "Cam,po obrigatório, o tipo de arquivo a ser consultado (ex.: 'Americanas', 'Semclass', 'Viniferas')."
            }
        }
    }

    return jsonify(docs)


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

@app.route('/api/processa/<file_type>', methods=['GET'])
def get_processa_files(file_type):
    # Check if the 'use_local' query parameter is passed
    use_local = request.args.get('use_local', 'false').lower() == 'true'

    # Define the CSV file name based on the file_type
    csv_filename = f"Processa{file_type}.csv"

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

@app.route('/api/exp/<file_type>', methods=['GET'])
def get_exportation_files(file_type):
    # Check if the 'use_local' query parameter is passed
    use_local = request.args.get('use_local', 'false').lower() == 'true'

    # Define the CSV file name based on the file_type
    csv_filename = f"Exp{file_type}.csv"

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

@app.route('/api/imp/<file_type>', methods=['GET'])
def get_importation_files(file_type):
    # Check if the 'use_local' query parameter is passed
    use_local = request.args.get('use_local', 'false').lower() == 'true'

    # Define the CSV file name based on the file_type
    csv_filename = f"Imp{file_type}.csv"

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

