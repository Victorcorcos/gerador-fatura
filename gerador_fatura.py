# gerador_fatura.py
"""
Gerador de Faturas - Arquivo Principal
Responsável por orquestrar todo o processo de geração de faturas.
"""

from cliente_api import ClienteAPI
from processar_dados import ProcessarDados
from gerar_PDF import GerarPDF
from utils_data import UtilsData
from config import (
    NUMERO_FATURA, 
    TAXA_HORA, 
    MES_COMPLETO, 
    INFO_FATURA
)

class GeradorFatura:
    
    def __init__(self):
        self.cliente_api = ClienteAPI()
        self.processar_dados = ProcessarDados()
        self.gerar_PDF = GerarPDF()
        self.utils_data = UtilsData()
    
    def gerar_fatura(self):
        try:
            data_inicio, data_fim = self.utils_data.calcular_periodo(MES_COMPLETO)
            print(f"Período selecionado: {data_inicio} a {data_fim}")
            
            info_fatura = self._preparar_info_fatura(data_inicio, data_fim)
            
            print("\nFazendo login na API...")
            self.cliente_api.fazer_login()
            
            print("Buscando dados de timesheet...")
            dados_api = self.cliente_api.buscar_dados_timesheet(data_inicio, data_fim)
            
            print("Processando dados...")
            resultados = self.processar_dados.processar_dados_api(dados_api, data_inicio, data_fim)
            
            if not resultados:
                print("Nenhum dado encontrado para o período especificado.")
                return
            
            nome_arquivo_pdf = self.utils_data.formatar_nome_arquivo(
                NUMERO_FATURA, data_inicio, data_fim
            )
            
            print("Gerando PDF...")
            pdf_gerado, total = self.gerar_PDF.gerar_pdf_fatura(
                resultados, info_fatura, nome_arquivo_pdf, TAXA_HORA
            )
            
            print(f"\nFatura gerada com sucesso: {pdf_gerado}")
            print(f"Valor total da fatura: R$ {total:.2f}")
            
            return pdf_gerado, total
            
        except Exception as e:
            print(f"Erro ao processar: {e}")
            raise
    
    def _preparar_info_fatura(self, data_inicio, data_fim):
        info = INFO_FATURA.copy()
        info.update({
            'fatura_numero': NUMERO_FATURA,
            'data_desenvolvimento_inicio': data_inicio,
            'data_desenvolvimento_fim': data_fim
        })
        return info


def main():
    print("=== GERADOR DE FATURAS ===")
    print("Iniciando processo de geração...")
    
    try:
        gerador = GeradorFatura()
        gerador.gerar_fatura()
        
    except KeyboardInterrupt:
        print("\nProcesso interrompido pelo usuário.")
    except Exception as e:
        print(f"Erro durante a execução: {e}")
        return 1
    
    print("\nProcesso concluído com sucesso!")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
