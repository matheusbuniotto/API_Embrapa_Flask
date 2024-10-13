# Embrapa/Vitibrasil API

## Descrição

Essa API é um serviço web baseado em Flask que fornece acesso a vários conjuntos de dados relacionados à indústria vinícola brasileira. Ela busca e processa arquivos CSV do site da Embrapa ou do armazenamento local, convertendo os dados para o formato JSON para facilitar o consumo.

## Funcionalidades

- Buscar e processar dados sobre produção de vinho, comércio, processamento, exportações e importações
- Opção de usar arquivos CSV locais ou buscar diretamente do site da Embrapa
- Saída em formato JSON para todos os endpoints
- Documentação integrada da API

## Instalação

1. Clone este repositório
2. Crie um ambiente virtual e ative-o (recomendado)
3. Instale os pacotes necessários através do arquivo requirements.txt


## Uso
Para rodar a API localmente, utilize o comando:
`python app.py`

A API estará disponível em http://localhost:5000


## Endpoints da API
- /api/status: Verifica se a API está funcionando
- /api/docs: Visualizar a documentação da API
- /api/Comercio: Obter dados de comércio
- /api/Producao: Obter dados de produção
- /api/processa/<produto>: Obter dados de processamento para diferentes tipos de produto
- /api/exp/<produto>: Obter dados de exportação para diferentes tipos de produto
- /api/imp/<produto>: Obter dados de importação para diferentes tipos de produto
  
Exemplo: colentando dados de Exportação de Uvas http://127.0.0.1:5000/api/exp/Uva

Exemplo: colentando dados de Comércio http://127.0.0.1:5000/api/Comercio

Caso prefira ou necessite consumir os arquivos localmente para validação sem acessar o sit da embrapa, utilize o parametro use_local=true

Exemplo: colentando dados de Exportação de Uvas http://127.0.0.1:5000/api/exp/Uva?use_local=true

Exemplo: colentando dados de Comércio http://127.0.0.1:5000/api/Comercio?use_local=true

Para informações detalhadas sobre cada endpoint, incluindo parâmetros de consulta e variáveis de caminho, consulte o endpoint /api/docs.

## Configuração
BASE_URL: A URL base para buscar arquivos CSV da Embrapa
LOCAL_CSV_DIR: O diretório para armazenar arquivos CSV locais
