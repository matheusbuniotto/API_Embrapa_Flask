import os

from flask import Flask, jsonify, request

from src.processing import get_csv_content, get_csv_content_from_local, process_csv_content

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
    # Verifiac o parametro use_local
    use_local = request.args.get('use_local', 'false').lower() == 'true'

    # Deine o nome do csv
    csv_filename = "Comercio.csv"

    if use_local:
        # Usa o csv loacl em caso de use_local=True
        filepath = os.path.join(LOCAL_CSV_DIR, csv_filename)
        csv_content_tuple = get_csv_content_from_local(filepath)
    else:
        # Caso contrário, consome direto do site da embrapa
        url = f"{BASE_URL}{csv_filename}"
        csv_content_tuple = get_csv_content(url)

    # Processa o CSV
    data = process_csv_content(csv_content_tuple)

    # Retorna o JSON
    return jsonify(data)

@app.route('/api/Producao', methods=['GET'])
def get_producao_data():
    # Verfica o parametro use_local
    use_local = request.args.get('use_local', 'false').lower() == 'true'

    # Define o nome do csv
    csv_filename = "Producao.csv"

    if use_local:
        # Usa o csv loacl em caso de use_local=True
        filepath = os.path.join(LOCAL_CSV_DIR, csv_filename)
        csv_content_tuple = get_csv_content_from_local(filepath)
    else:
        # Caso contrário, consome direto do site da embrapa
        url = f"{BASE_URL}{csv_filename}"
        csv_content_tuple = get_csv_content(url)

    # Processa o CSV
    data = process_csv_content(csv_content_tuple)

    # Retorna o JSON
    return jsonify(data)

@app.route('/api/processa/<file_type>', methods=['GET'])
def get_processa_files(file_type):
    # Verfica o parametro use_local
    use_local = request.args.get('use_local', 'false').lower() == 'true'

    # Define o nome do csv
    csv_filename = f"Processa{file_type}.csv"

    if use_local:
        # Usa o csv loacl em caso de use_local=True
        filepath = os.path.join(LOCAL_CSV_DIR, csv_filename)
        csv_content_tuple = get_csv_content_from_local(filepath)
    else:
        # Caso contrário, consome direto do site da embrapa
        url = f"{BASE_URL}{csv_filename}"
        csv_content_tuple = get_csv_content(url)

    # Processa o csv
    data = process_csv_content(csv_content_tuple)

    # Retorna o JSON
    return jsonify(data)

@app.route('/api/exp/<file_type>', methods=['GET'])
def get_exportation_files(file_type):
    # Verfica o parametro use_local
    use_local = request.args.get('use_local', 'false').lower() == 'true'

    # Define o nome do csv
    csv_filename = f"Exp{file_type}.csv"

    if use_local:
        # Usa o csv loacl em caso de use_local=True
        filepath = os.path.join(LOCAL_CSV_DIR, csv_filename)
        csv_content_tuple = get_csv_content_from_local(filepath)
    else:
        # Caso contrário, consome direto do site da embrapa
        url = f"{BASE_URL}{csv_filename}"
        csv_content_tuple = get_csv_content(url)

    # Processa o CSV para JSON
    data = process_csv_content(csv_content_tuple)

    # Returna o JSON
    return jsonify(data)

@app.route('/api/imp/<file_type>', methods=['GET'])
def get_importation_files(file_type):
    # Verfica o parametro use_local
    use_local = request.args.get('use_local', 'false').lower() == 'true'

    # Define o csv
    csv_filename = f"Imp{file_type}.csv"

    if use_local:
        # Usa o csv loacl em caso de use_local=True
        filepath = os.path.join(LOCAL_CSV_DIR, csv_filename)
        csv_content_tuple = get_csv_content_from_local(filepath)
    else:
        # Caso contrário, consome direto do site da embrapa
        url = f"{BASE_URL}{csv_filename}"
        csv_content_tuple = get_csv_content(url)

    # Processa o CSV para JSON
    data = process_csv_content(csv_content_tuple)

    # Returna o JSON
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

