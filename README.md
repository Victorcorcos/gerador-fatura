# Gerador de Faturas

Sistema automatizado para geração de faturas baseado em dados de timesheet obtidos via API GraphQL.

## Estrutura do Projeto

```
gerador-fatura/
├── gerador_fatura.py     # Arquivo principal
├── config.py             # Configurações e dados pessoais
├── cliente_api           # Cliente para interação com API
├── processar_dados.py    # Processamento de dados
├── gerar_PDF.py          # Geração de PDF
├── utils_data.py         # Utilitários de data
├── requirements.txt      # Dependências
├── faturas/              # Diretório onde os PDFs são salvos
└── README.md             # Este arquivo
```

## Instalação

### Pré-requisitos do Sistema

Antes de instalar o Python e as dependências do projeto, certifique-se de que as bibliotecas de desenvolvimento necessárias estão instaladas:

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y libbz2-dev libsqlite3-dev liblzma-dev libreadline-dev libssl-dev libffi-dev zlib1g-dev
```

#### Fedora/RHEL/CentOS
```bash
sudo dnf install -y bzip2-devel sqlite-devel xz-devel readline-devel openssl-devel libffi-devel zlib-devel
```

#### macOS
```bash
brew install bzip2 sqlite xz readline openssl libffi zlib
```

**Por que essas bibliotecas são necessárias?**

Estas bibliotecas de desenvolvimento são necessárias para compilar módulos built-in do Python (como `_bz2`, `_sqlite3`, `_lzma`). Se o Python for instalado sem essas bibliotecas, você encontrará erros do tipo `ModuleNotFoundError` ao executar o projeto.

**Nota para usuários de gerenciadores de versão Python (asdf, pyenv, etc.):**

Se você usa `asdf`, `pyenv` ou similar, instale as bibliotecas acima **antes** de instalar a versão do Python. Caso contrário, será necessário reinstalar o Python após instalar as bibliotecas:

```bash
# Para asdf
asdf uninstall python 3.10.16
asdf install python 3.10.16

# Para pyenv
pyenv uninstall 3.10.16
pyenv install 3.10.16
```

### Pré-requisitos de Software
- Python **3.10 ou superior**
- Python 3.10 venv instalado (`apt install python3.10-venv`)
- `git` instalado (`sudo apt install -y git`)

### Clone o repositório

```bash
git clone https://github.com/AlbertoLucass/gerador-fatura.git
cd gerador-fatura
```

### Crie e ative um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate # Linux/macOS
# ou
venv\Scripts\activate.bat # Windows
```

### Atualize o gerenciador de pacotes

```bash
pip install --upgrade pip
```

### Instale as dependências

```bash
pip install -r requirements.txt
```

## Configuração

### Variáveis de Ambiente

O sistema agora utiliza variáveis de ambiente para configurações sensíveis. Crie um arquivo `.env` baseado no template `.env.example`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas informações:

```bash
# API Credentials
EMAIL=seu.email@exemplo.com
PASSWORD=sua_senha_aqui

# Company Information
RAZAO_SOCIAL=Sua Empresa LTDA
CNPJ=00.000.000/0001-00
ENDERECO=Seu Endereço Completo
PIX=seu-pix@email.com

# Client Information
CLIENTE_NOME=Nome do Cliente LTDA
CLIENTE_CNPJ=00.000.000/0001-00
CLIENTE_ENDERECO=Endereço do Cliente

# Invoice Configuration
NUMERO_FATURA=1
TAXA_HORA=60.0
MES_COMPLETO=08/2025
TAGS_INTERESSE=development,meeting
```

**Configurações importantes:**
- `MES_COMPLETO`: Período da fatura no formato MM/YYYY (se não especificado, usa o mês anterior automaticamente)
- `TAXA_HORA`: Valor da hora trabalhada 
- `TAGS_INTERESSE`: Tags de timesheet separadas por vírgula (ex: `development,meeting,tests`)

⚠️ **Importante**: O arquivo `.env` contém informações sensíveis e não deve ser commitado no git. Ele já está incluído no `.gitignore`.
## Uso

Execute o arquivo principal:

```bash
python gerador_fatura.py
# ou
python3 gerador_fatura.py
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

Os PDFs são automaticamente salvos no diretório `faturas/` (criado automaticamente se não existir) no formato:

```
faturas/Fatura_[NUMERO]_[DATA_INICIO]_a_[DATA_FIM].pdf
```

Exemplo: `faturas/Fatura_3_01-06-2025_a_30-06-2025.pdf`

## Dependências

- `requests`: Para comunicação com API
- `pandas`: Para manipulação de dados
- `reportlab`: Para geração de PDF
- `python-dateutil`: Para manipulação de datas
- `python-dotenv`: Para carregamento de variáveis de ambiente

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
