# config.py
"""
Arquivo de configuração para o gerador de faturas.
Configure aqui suas informações pessoais e parâmetros.
"""

import os
from datetime import date
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://digitalize.oxean.com.br/graphql"
API_HEADERS = {
    'Content-Type': 'application/json'
}

LOGIN_CREDENTIALS = {
    "email": os.getenv("EMAIL"),
    "password": os.getenv("PASSWORD")
}

INFO_FATURA = {
    "razao_social": os.getenv("RAZAO_SOCIAL"),
    "cnpj": os.getenv("CNPJ"),
    "endereco": os.getenv("ENDERECO"),
    "pix": os.getenv("PIX"),
    "cliente_nome": os.getenv("CLIENTE_NOME"),
    "cliente_cnpj": os.getenv("CLIENTE_CNPJ"),
    "cliente_endereco": os.getenv("CLIENTE_ENDERECO")
}

NUMERO_FATURA = os.getenv("NUMERO_FATURA")
TAXA_HORA = float(os.getenv("TAXA_HORA", "1.0"))
MES_COMPLETO = os.getenv("MES_COMPLETO", (date.today() - relativedelta(months=1)).strftime("%m/%Y"))

PDF_CONFIG = {
    "pagesize": "A4",
    "margins": {
        "right": 72,
        "left": 72,
        "top": 72,
        "bottom": 72
    }
}

TAGS_INTERESSE = os.getenv("TAGS_INTERESSE", "development,meeting").split(",")
