# Gerador de Faturas

Sistema automatizado para geração de faturas baseado em dados de timesheet obtidos via API GraphQL.

## Estrutura do Projeto

```
gerador_fatura/
├── gerador_fatura.py     # Arquivo principal
├── config.py             # Configurações e dados pessoais
├── cliente_api           # Cliente para interação com API
├── processar_dados.py    # Processamento de dados
├── gerar_PDF.py          # Geração de PDF
├── utils_data.py         # Utilitários de data
├── requirements.txt      # Dependências
└── README.md             # Este arquivo
```

## Instalação

1. Clone o repositorio

    ```bash
    git clone https://github.com/AlbertoLucass/gerador-fatura.git
    ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Configuração

Antes de usar o sistema, configure o arquivo `config.py`:

### Credenciais de Login

```python
LOGIN_CREDENTIALS = {
    "email": "seu.email@exemplo.com",
    "password": "sua_senha_aqui"
}
```

### Configurações da Fatura

```python
NUMERO_FATURA = "3"
TAXA_HORA = 1.0
MES_COMPLETO = "06/2025"  # Formato: MM/YYYY
```

### Informações Pessoais

Edite a seção `INFO_FATURA` com seus dados:

- Razão social
- CNPJ
- Endereço
- Dados do cliente
- etc.

## Uso

Execute o arquivo principal:

```bash
python gerador_fatura.py
```

O sistema irá:

1. Fazer login na API
2. Buscar dados de timesheet do período configurado
3. Processar os dados
4. Gerar um PDF com a fatura

## Estrutura dos Módulos

### `gerador_fatura.py`

Arquivo principal que orquestra todo o processo.

### `config.py`

Contém todas as configurações, credenciais e dados pessoais.

### `cliente_api`

Responsável pela comunicação com a API GraphQL:

- Autenticação
- Consultas de dados

### `processar_dados.py`

Processa os dados brutos da API:

- Filtragem por período
- Agrupamento por tags
- Formatação de dados

### `gerar_PDF.py`

Gera o PDF da fatura:

- Formatação do documento
- Tabelas e estilos
- Cálculos de valores

### `utils_data.py`

Utilitários para manipulação de datas:

- Cálculo de períodos
- Formatação de nomes de arquivo
- Validação de datas

## Personalização

### Adicionar Novas Tags

Edite a lista `TAGS_INTERESSE` no arquivo `config.py`:

```python
TAGS_INTERESSE = ['development', 'meeting', 'tests', 'nova_tag']
```

### Modificar Layout do PDF

Edite os métodos em `gerar_PDF.py` para personalizar:

- Estilos de texto
- Cores das tabelas
- Estrutura do documento

### Alterar Formato de Datas

Modifique os métodos em `utils_data.py` para diferentes formatos.

## Tratamento de Erros

O sistema possui tratamento de erros para:

- Falhas de autenticação
- Problemas de conexão com API
- Dados inválidos
- Erros na geração de PDF

## Arquivos Gerados

Os PDFs são salvos no formato:

```
Fatura_[NUMERO]_[DATA_INICIO]_a_[DATA_FIM].pdf
```

Exemplo: `Fatura_3_01-06-2025_a_30-06-2025.pdf`

## Dependências

- `requests`: Para comunicação com API
- `pandas`: Para manipulação de dados
- `reportlab`: Para geração de PDF
- `python-dateutil`: Para manipulação de datas

## Troubleshooting

### Erro de Autenticação

Verifique se:

- Email e senha estão corretos no `config.py`
- A API está acessível
- As credenciais têm permissões adequadas

### Nenhum Dado Encontrado

Verifique se:

- O período está correto
- Existem dados de timesheet para o período
- As tags estão configuradas corretamente

### Erro na Geração do PDF

Verifique se:

- Todas as dependências estão instaladas
- Há permissão de escrita no diretório
- Os dados processados são válidos

