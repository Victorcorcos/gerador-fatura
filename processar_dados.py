# processar_dados.py
"""
Processador de dados para conversão dos dados da API 
para o formato necessário para geração da fatura.
"""

import pandas as pd
from datetime import datetime
from config import TAGS_INTERESSE


class ProcessarDados:
    
    def __init__(self):
        self.tags_interesse = TAGS_INTERESSE
    
    def processar_dados_api(self, dados_api, data_inicio, data_fim):
        data_inicio_dt = datetime.strptime(data_inicio, "%d/%m/%Y")
        data_fim_dt = datetime.strptime(data_fim, "%d/%m/%Y")
        
        registros_processados = []
        
        for registro in dados_api:
            dynamic_fields = registro.get('dynamicFields', {})
            dynamic_associations = registro.get('dynamicAssociations', {})
            
            start_date_str = dynamic_fields.get('start_date', '')
            description = dynamic_fields.get('description', '')
            duration_str = dynamic_fields.get('duration', '0')
            tag = dynamic_fields.get('tag', 'development')
            # Nome da task vem de dynamicAssociations.task
            task_name = dynamic_associations.get('task', '').strip() if isinstance(dynamic_associations.get('task', ''), str) else ''
            # ID da task (quando existir) pode aparecer em dynamicFields.task
            task_id = dynamic_fields.get('task', '')
            
            # Se não houver descrição, tenta usar o nome da task; se não houver, usa o id; caso contrário, marca como sem descrição
            if not description and task_name:
                description = task_name
            elif not description and task_id:
                description = str(task_id)
            elif not description and not task:
                description = 'Sem descrição'
            
            if start_date_str:
                try:
                    start_date_dt = self._processar_data(start_date_str)
                    
                    if not (data_inicio_dt <= start_date_dt <= data_fim_dt):
                        continue
                        
                except Exception as e:
                    print(f"Erro ao processar data {start_date_str}: {e}")
                    continue
            else:
                continue
            
            try:
                duration = float(str(duration_str).replace(',', '.'))
            except (ValueError, TypeError):
                duration = 0.0
            
            registros_processados.append({
                'start_date': start_date_dt,
                'description': description,
                'duration': duration,
                'tag': tag,
                'task_name': task_name
            })
        
        return self._agrupar_por_task(registros_processados, data_inicio, data_fim)
    
    def _processar_data(self, start_date_str):
        if 'T' in start_date_str:
            start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00')).date()
        else:
            for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]:
                try:
                    start_date = datetime.strptime(start_date_str[:10], fmt).date()
                    break
                except ValueError:
                    continue
            else:
                raise ValueError(f"Formato de data não reconhecido: {start_date_str}")
        
        return datetime.combine(start_date, datetime.min.time())
    
    def _agrupar_por_task(self, registros_processados, data_inicio, data_fim):
        df = pd.DataFrame(registros_processados)

        if df.empty:
            print(f"Nenhum registro encontrado entre {data_inicio} e {data_fim}")
            return {}

        # Considera todos os registros independentemente da tag; inclui também os sem nome de task
        df = df.copy()
        df['task_group'] = df['task_name'].fillna('').astype(str).str.strip()
        df.loc[df['task_group'] == '', 'task_group'] = 'Sem task'

        resultados = {}

        # Para cada task, agrega as descrições e soma a duração
        for task in sorted(df['task_group'].unique()):
            task_df = df[df['task_group'] == task]
            if task_df.empty:
                continue

            agrupado = (
                task_df.groupby('description')['duration']
                .sum()
                .reset_index()
                .sort_values('duration', ascending=False)
            )

            resultados[task] = agrupado

        return resultados
