# config.py
"""
Arquivo de configuração para o gerador de faturas.
Configure aqui suas informações pessoais e parâmetros.
"""


API_URL = "https://digitalize.oxean.com.br/graphql"
API_HEADERS = {
    'Content-Type': 'application/json'
}

LOGIN_CREDENTIALS = {
    "email": "",
    "password": ""
}

NUMERO_FATURA = "3"
TAXA_HORA = 1.0

MES_COMPLETO = "06/2025"


INFO_FATURA = {
    "razao_social": "",
    "cnpj": "",
    "endereco": "",
    "pix": "",
    "cliente_nome": "",
    "cliente_cnpj": "",
    "cliente_endereco": ""
}


PDF_CONFIG = {
    "pagesize": "A4",
    "margins": {
        "right": 72,
        "left": 72,
        "top": 72,
        "bottom": 72
    }
}


TAGS_INTERESSE = ['development', 'meeting', 'tests']
