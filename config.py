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

# Horas extras manuais (podem variar por mês), padrão 0.0
def _env_float(name: str, default: float = 0.0) -> float:
    try:
        val = os.getenv(name)
        return float(val) if val not in (None, "") else default
    except Exception:
        return default

HORAS_EXTRA = _env_float("HORAS_EXTRA", 0.0)

# Dias úteis por mês (substituível por variáveis de ambiente WORKING_DAYS_*)
_DEFAULT_WORKING_DAYS = {
    'JANUARY': 21,
    'FEBRUARY': 20,
    'MARCH': 22,
    'APRIL': 19,
    'MAY': 22,
    'JUNE': 21,
    'JULY': 21,
    'AUGUST': 23,
    'SEPTEMBER': 21,
    'OCTOBER': 20,
    'NOVEMBER': 20,
    'DECEMBER': 22,
}

def _env_working_days(key: str, default: int) -> int:
    try:
        val = os.getenv(key)
        return int(val) if val is not None and val != '' else default
    except ValueError:
        return default

"""
Permite sobrescrever por .env usando nomes completos do mês:
JANUARY, FEBRUARY, ..., DECEMBER
(valores representam dias úteis do mês)
"""
WORKING_DAYS_BY_MONTH_NAME = {
    m: _env_working_days(m, d) for m, d in _DEFAULT_WORKING_DAYS.items()
}

# Mapeia para código numérico do mês 'MM' -> horas (dias * 8)
_MONTH_CODE_MAP = {
    '01': 'JANUARY', '02': 'FEBRUARY', '03': 'MARCH', '04': 'APRIL', '05': 'MAY', '06': 'JUNE',
    '07': 'JULY', '08': 'AUGUST', '09': 'SEPTEMBER', '10': 'OCTOBER', '11': 'NOVEMBER', '12': 'DECEMBER'
}

WORKING_HOURS_BY_MONTH = {
    code: WORKING_DAYS_BY_MONTH_NAME[name] * 8 for code, name in _MONTH_CODE_MAP.items()
}
