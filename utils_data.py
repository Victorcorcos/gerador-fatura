# utils_data.py
"""
Utilitários para manipulação de datas e períodos.
"""

from datetime import datetime
from calendar import monthrange
import os


class UtilsData:
    
    @staticmethod
    def calcular_periodo(mes_completo):
        try:
            mes, ano = mes_completo.split('/')
            mes = int(mes)
            ano = int(ano)

            data_inicio = f"01/{mes:02d}/{ano}"

            ultimo_dia = monthrange(ano, mes)[1]
            data_fim = f"{ultimo_dia:02d}/{mes:02d}/{ano}"

            return data_inicio, data_fim

        except ValueError:
            raise ValueError("Formato de mês inválido. Use MM/YYYY (ex: 05/2025)")
    
    @staticmethod
    def formatar_nome_arquivo(numero_fatura, data_inicio, data_fim):
        # Criar diretório faturas se não existir
        faturas_dir = "faturas"
        if not os.path.exists(faturas_dir):
            os.makedirs(faturas_dir)
        
        data_inicio_fmt = data_inicio.replace('/', '-')
        data_fim_fmt = data_fim.replace('/', '-')
        filename = f"Fatura_{numero_fatura}_{data_inicio_fmt}_a_{data_fim_fmt}.pdf"
        
        return os.path.join(faturas_dir, filename)
    
    @staticmethod
    def validar_formato_data(data_str, formato="%d/%m/%Y"):
        try:
            datetime.strptime(data_str, formato)
            return True
        except ValueError:
            return False
