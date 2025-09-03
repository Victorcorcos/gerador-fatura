# gerar_PDF.py
"""
Gerador de PDF para faturas.
Responsável por criar o documento PDF com os dados processados.
"""

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
from config import PDF_CONFIG, WORKING_HOURS_BY_MONTH, HORAS_EXTRA


class GerarPDF:

    def __init__(self):
        self.estilos = self._criar_estilos()
    
    def gerar_pdf_fatura(self, resultados, info_fatura, nome_arquivo, taxa_hora):
        doc = SimpleDocTemplate(
            nome_arquivo,
            pagesize=A4,
            rightMargin=PDF_CONFIG["margins"]["right"],
            leftMargin=PDF_CONFIG["margins"]["left"],
            topMargin=PDF_CONFIG["margins"]["top"],
            bottomMargin=PDF_CONFIG["margins"]["bottom"]
        )
        
        elementos = []
        elementos.append(Paragraph(f"FATURA Nº {info_fatura['fatura_numero']}", 
                                 self.estilos['titulo']))
        elementos.append(Spacer(1, 0.2 * inch))
        elementos.extend(self._criar_tabela_emissor_cliente(info_fatura))
        elementos.extend(self._criar_informacoes_fatura(info_fatura))
        elementos.append(Paragraph("<b>DETALHES DOS SERVIÇOS</b>", 
                                 self.estilos['subtitulo']))
        tabela_servicos, total_geral = self._criar_tabela_servicos(resultados, taxa_hora)
        elementos.extend([tabela_servicos, Spacer(1, 0.5 * inch)])

        # Seção de resumo por task
        elementos.append(Paragraph("<b>Totais</b>", self.estilos['subtitulo']))
        tabela_resumo = self._criar_tabela_resumo(resultados, taxa_hora, info_fatura)
        elementos.extend([tabela_resumo, Spacer(1, 0.3 * inch)])
        
        doc.build(elementos)
        
        return nome_arquivo, total_geral

    def _criar_estilos(self):
        estilos = getSampleStyleSheet()
        
        estilo_normal = estilos['Normal']
        
        return {
            'titulo': ParagraphStyle(
                'TituloFatura',
                parent=estilos['Heading1'],
                fontSize=16,
                alignment=TA_CENTER,
                spaceAfter=12
            ),
            'subtitulo': ParagraphStyle(
                'Subtitulo',
                parent=estilos['Heading2'],
                fontSize=14,
                spaceAfter=10
            ),
            'normal': estilo_normal,
            'direita': ParagraphStyle(
                'Direita', 
                parent=estilo_normal,
                alignment=TA_RIGHT
            ),
            'tag': ParagraphStyle(
                'TagStyle',
                parent=estilo_normal,
                fontName='Helvetica-Bold',
                fontSize=12,
                textColor=colors.black,
                alignment=TA_LEFT
            ),
            'descricao': ParagraphStyle(
                'DescStyle',
                parent=estilo_normal,
                alignment=TA_CENTER
            )
        }

    def _fmt_brl(self, valor: float) -> str:
        try:
            return f"R$ {valor:,.2f}"
        except Exception:
            return f"R$ {valor:.2f}"

    def _criar_tabela_emissor_cliente(self, info):
        elementos = []
        
        elementos.append(Paragraph("<b>DADOS DO EMISSOR</b>", self.estilos['subtitulo']))
        dados_emissor = [
            ["<b>Razão Social:</b>", info['razao_social']],
            ["<b>CNPJ:</b>", info['cnpj']],
            ["<b>Endereço:</b>", info['endereco']],
            ["<b>PIX:</b>", info['pix']]
        ]
        tabela_emissor = Table([[Paragraph(cell[0], self.estilos['normal']), 
                                Paragraph(cell[1], self.estilos['normal'])] 
                               for cell in dados_emissor], 
                              colWidths=[100, 350])
        tabela_emissor.setStyle(self._estilo_tabela_simples())
        elementos.extend([tabela_emissor, Spacer(1, 0.2 * inch)])
        
        elementos.append(Paragraph("<b>DADOS DO CLIENTE</b>", self.estilos['subtitulo']))
        dados_cliente = [
            ["<b>Cliente:</b>", info['cliente_nome']],
            ["<b>CNPJ:</b>", info['cliente_cnpj']],
            ["<b>Endereço:</b>", info['cliente_endereco']]
        ]
        tabela_cliente = Table([[Paragraph(cell[0], self.estilos['normal']), 
                               Paragraph(cell[1], self.estilos['normal'])] 
                              for cell in dados_cliente], 
                             colWidths=[100, 350])
        tabela_cliente.setStyle(self._estilo_tabela_simples())
        elementos.extend([tabela_cliente, Spacer(1, 0.2 * inch)])
        
        return elementos

    def _criar_informacoes_fatura(self, info):
        elementos = []
        data_fatura = datetime.today().strftime('%d/%m/%Y')
        
        elementos.append(Paragraph("<b>INFORMAÇÕES DA FATURA</b>", self.estilos['subtitulo']))
        info_data = [
            ["<b>Data da Fatura:</b>", data_fatura],
            ["<b>Período:</b>", f"{info['data_desenvolvimento_inicio']} a {info['data_desenvolvimento_fim']}"]
        ]
        tabela_info = Table([[Paragraph(cell[0], self.estilos['normal']), 
                             Paragraph(cell[1], self.estilos['normal'])] 
                            for cell in info_data], 
                           colWidths=[100, 350])
        tabela_info.setStyle(self._estilo_tabela_simples())
        elementos.extend([tabela_info, Spacer(1, 0.3 * inch)])
        
        return elementos

    def _estilo_tabela_simples(self):
        return TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ])

    def _criar_tabela_servicos(self, resultados, taxa_hora):
        cabecalho = ["Task", "Taxa por hora (R$)", "Horas", "Total (R$)"]
        dados_tabela = [cabecalho]
        total_geral = total_horas = 0

        for task, dados in resultados.items():
            if dados.empty:
                continue
            
            # Totais por task
            horas_task = float(dados['duration'].sum())
            total_task = horas_task * taxa_hora

            dados_tabela.append([
                Paragraph(f"<b>{task}</b>", self.estilos['tag']),
                f"{taxa_hora:.2f}".replace('.', ','),
                f"{horas_task:.2f}".replace('.', ','),
                f"{total_task:.2f}".replace('.', ',')
            ])
            
            for _, row in dados.iterrows():
                duracao = row['duration']
                total_linha = duracao * taxa_hora
                total_geral += total_linha
                total_horas += duracao
                
                dados_tabela.append([
                    Paragraph(row['description'], self.estilos['descricao']),
                    f"{taxa_hora:.2f}".replace('.', ','),
                    f"{duracao:.2f}".replace('.', ','),
                    f"{total_linha:.2f}".replace('.', ',')
                ])

        dados_tabela.append([
            "", "",
            Paragraph(f"<b>{total_horas:.2f}</b>".replace('.', ','), self.estilos['descricao']),
            Paragraph(f"<b>R$ {total_geral:.2f}</b>".replace('.', ','), self.estilos['descricao'])
        ])

        tabela = Table(dados_tabela, colWidths=[200, 100, 80, 120])
        estilo = self._estilo_tabela_servicos(len(dados_tabela), resultados)
        tabela.setStyle(estilo)
        
        return tabela, total_geral

    def _criar_tabela_resumo(self, resultados, taxa_hora, info_fatura):
        cabecalho = [
            "Categoria",
            "Horas (H)",
            "Taxa por hora (R$)",
            "Valor Total (R$)"
        ]
        dados = [cabecalho]
        total_horas = 0.0

        # Determina horas cobradas do mês (para usar em diferentes linhas)
        try:
            data_inicio = info_fatura.get('data_desenvolvimento_inicio')
            mes_codigo = data_inicio.split('/')[1] if isinstance(data_inicio, str) and '/' in data_inicio else None
            horas_cobradas = WORKING_HOURS_BY_MONTH.get(mes_codigo, 0)
        except Exception:
            horas_cobradas = 0

        for task, df_task in resultados.items():
            if df_task.empty:
                continue
            horas = float(df_task['duration'].sum())
            total_horas += horas
            dados.append([
                Paragraph(f"Horas Mensais ({task})", self.estilos['normal']),
                f"{horas:.2f}".replace('.', ','),
                "",
                ""
            ])

        # Linha de totalização das horas mensais somadas de todas as tasks
        dados.append([
            Paragraph("Horas Mensais (TOTAL)", self.estilos['normal']),
            f"{total_horas:.2f}".replace('.', ','),
            "",
            ""
        ])

        # Linha Horas Extras = HORAS_EXTRA + (TOTAL - COBRADAS)
        horas_extras = float(HORAS_EXTRA) + (total_horas - float(horas_cobradas))
        dados.append([
            Paragraph("Horas Extras", self.estilos['normal']),
            f"{horas_extras:.2f}".replace('.', ','),
            "",
            ""
        ])

        # Linha Horas Totais (Cobradas) - baseada nas horas do mês (config)
        total_cobrado = horas_cobradas * taxa_hora
        dados.append([
            Paragraph("<b>Horas Totais (Cobradas)</b>", self.estilos['normal']),
            f"{horas_cobradas:.2f}".replace('.', ','),
            self._fmt_brl(taxa_hora),
            self._fmt_brl(total_cobrado)
        ])
        row_total_cobrado = len(dados) - 1

        # Linha Internet (valor fixo 120, sem horas e taxa)
        internet_valor = 120.0
        dados.append([
            Paragraph("Internet", self.estilos['normal']),
            "",
            "",
            self._fmt_brl(internet_valor)
        ])
        row_internet = len(dados) - 1

        # Linha Total (Cobrado) - consolidado final
        # Total (Cobrado) final: soma de Horas Totais (Cobradas) + Internet
        total_cobrado_final = total_cobrado + internet_valor
        dados.append([
            Paragraph("<b>Total (Cobrado)</b>", self.estilos['normal']),
            "",
            "",
            self._fmt_brl(total_cobrado_final)
        ])

        # Calcula índice da linha "Horas Extras" para anotar a célula de horas (coluna 1)
        row_idx_horas_extras = None
        for i, row in enumerate(dados):
            if isinstance(row[0], Paragraph):
                txt = row[0].text
                if 'Horas Extras' in txt and 'TOTAL' not in txt and 'Totais' not in txt:
                    row_idx_horas_extras = i
                    break

        # Monta mensagem explicativa para a anotação
        def fmt2(v):
            return f"{v:.2f}".replace('.', ',')
        explicacao = (
            f"Cálculo das Horas Extras:\n"
            f"HORAS_EXTRA ({fmt2(float(HORAS_EXTRA))}) + "
            f"(Horas Mensais (TOTAL) ({fmt2(total_horas)}) - Horas Totais (Cobradas) ({fmt2(horas_cobradas)})) = "
            f"{fmt2(horas_extras)}"
        )

        annotations = []
        if row_idx_horas_extras is not None:
            # coluna 1 corresponde a "Horas (H)"
            annotations.append({'row': row_idx_horas_extras, 'col': 1, 'text': explicacao})

        tabela = AnnotatedTable(dados, colWidths=[220, 80, 100, 120], annotations=annotations)
        estilo = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ])
        # Estilo para linhas finais: Total (Cobrado) e Total Geral
        last_row = len(dados) - 1  # Total Geral
        # Aplica destaque ao Total (Cobrado) e Total Geral
        estilo.add('BACKGROUND', (0, row_total_cobrado), (-1, row_total_cobrado), colors.lightgrey)
        estilo.add('FONTNAME', (0, row_total_cobrado), (-1, row_total_cobrado), 'Helvetica-Bold')
        estilo.add('LINEABOVE', (0, row_total_cobrado), (-1, row_total_cobrado), 1, colors.black)
        # Internet: fundo cinza como as demais linhas de totalização
        estilo.add('BACKGROUND', (0, row_internet), (-1, row_internet), colors.lightgrey)
        estilo.add('BACKGROUND', (0, last_row), (-1, last_row), colors.lightgrey)
        estilo.add('FONTNAME', (0, last_row), (-1, last_row), 'Helvetica-Bold')
        estilo.add('LINEABOVE', (0, last_row), (-1, last_row), 1, colors.black)
        tabela.setStyle(estilo)
        return tabela

    def _estilo_tabela_servicos(self, num_linhas, resultados):
        estilo = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
            ('BACKGROUND', (0, 1), (-1, -2), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('LINEBELOW', (0, -2), (-1, -2), 1, colors.black),
            ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black)
        ])
        
        linha = 1
        for task in resultados:
            if not resultados[task].empty:
                estilo.add('BACKGROUND', (0, linha), (-1, linha), colors.lightgrey)
                estilo.add('FONTSIZE', (0, linha), (-1, linha), 12)
                estilo.add('FONTNAME', (0, linha), (-1, linha), 'Helvetica-Bold')
                estilo.add('TEXTCOLOR', (0, linha), (-1, linha), colors.black)
                linha += len(resultados[task]) + 1
                
        return estilo

class AnnotatedTable(Table):
    """
    Tabela com suporte a anotações (sticky notes) posicionadas em células específicas.
    annotations: lista de dicts { 'row': int, 'col': int, 'text': str }
    """
    def __init__(self, data, colWidths=None, rowHeights=None, annotations=None, **kwargs):
        super().__init__(data, colWidths=colWidths, rowHeights=rowHeights, **kwargs)
        self._annotations = annotations or []

    def draw(self):
        # Desenha a tabela normalmente
        super().draw()
        # Após desenhar, adiciona anotações
        canv = self.canv
        # Garantir que col/row widths estão calculados
        colWidths = self._colWidths
        rowHeights = self._rowHeights
        total_height = sum(rowHeights)

        for ann in self._annotations:
            r = ann.get('row')
            c = ann.get('col')
            text = ann.get('text', '')
            try:
                # Converter índice de linha (0=top) para coordenadas relativas à base da tabela
                y_top = sum(rowHeights[:r+1])
                y_bottom = sum(rowHeights[:r])
                # Mas como a origem é bottom-left, invertemos em relação à altura total
                y0 = total_height - y_top
                y1 = total_height - y_bottom
                x0 = sum(colWidths[:c])
                x1 = sum(colWidths[:c+1])
                # Reduz a área alvo para ficar bem dentro da célula
                pad = 2
                x0 += pad; x1 -= pad; y0 += pad; y1 -= pad
                # Usa highlightAnnotation (sem ícone grande), mostrando o texto ao passar o mouse
                canv.highlightAnnotation(text, Rect=(x0, y0, x1, y1), Color=[1, 1, 0.85], relative=1)
            except Exception:
                # Se algo falhar, ignora silenciosamente para não quebrar a geração do PDF
                continue
