# Claude Code Guide for Gerador de Faturas

## Project Overview
Automated invoice generation system that fetches timesheet data via GraphQL API and generates PDF invoices.

## Project Structure
```
gerador-fatura/
├── gerador_fatura.py     # Main orchestrator
├── config.py             # Configuration and credentials
├── cliente_api.py        # API client for GraphQL
├── processar_dados.py    # Data processing logic
├── gerar_PDF.py          # PDF generation
├── utils_data.py         # Date utilities
├── requirements.txt      # Dependencies
├── venv/                 # Virtual environment
└── README.md             # Documentation
```

## Key Configuration
- **API Endpoint**: `https://digitalize.oxean.com.br/graphql`
- **Python Version**: 3.10+ required
- **Virtual Environment**: Always use `venv/`
- **Main Config File**: `config.py` contains all settings

## Common Commands

### Environment Setup
```bash
# Activate virtual environment (ALWAYS required)
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Generate invoice with current config
python gerador_fatura.py
```

### Testing/Linting
- No specific test framework configured
- Check for Python syntax: `python -m py_compile *.py`
- Manual testing by running the main script

## Configuration Details

### Invoice Settings (config.py)
- `NUMERO_FATURA`: Invoice number
- `TAXA_HORA`: Hourly rate
- `MES_COMPLETO`: Period (MM/YYYY format, defaults to previous month)
- `TAGS_INTERESSE`: Tags to filter timesheet data

### API Configuration
- Credentials stored in `LOGIN_CREDENTIALS`
- GraphQL endpoint in `API_URL`

## Development Guidelines

### Code Style
- Follow existing Python conventions in the codebase
- Use descriptive variable names in Portuguese (project language)
- Keep modular structure with separate concerns

### Security
- ⚠️ **IMPORTANT**: Never commit real credentials
- API credentials are in `config.py` - handle with care
- Consider environment variables for sensitive data

### Data Flow
1. **Authentication**: `cliente_api.py` handles login
2. **Data Fetching**: GraphQL queries for timesheet data
3. **Processing**: `processar_dados.py` filters and formats data
4. **PDF Generation**: `gerar_PDF.py` creates invoice document
5. **File Output**: PDF saved as `Fatura_[NUM]_[START]_a_[END].pdf`

## Dependencies
- `requests==2.31.0` - API communication
- `pandas==2.0.3` - Data manipulation
- `reportlab==4.0.4` - PDF generation
- `python-dateutil==2.8.2` - Date handling
- `numpy==1.24.4` - Pandas dependency

## Troubleshooting

### Common Issues
- **Authentication errors**: Check credentials in `config.py`
- **No data found**: Verify date period and tags configuration
- **PDF generation fails**: Ensure reportlab is properly installed
- **Import errors**: Always activate virtual environment first

### Debug Steps
1. Verify virtual environment is active
2. Check API connectivity
3. Validate configuration parameters
4. Test with simplified date ranges

## File Patterns
- **Config changes**: Always edit `config.py` for settings
- **API modifications**: Update `cliente_api.py`
- **Data processing**: Modify `processar_dados.py`
- **PDF styling**: Edit `gerar_PDF.py`
- **Date handling**: Update `utils_data.py`

## Git Workflow
- Main branch: `main`
- Current branch: `improve_gerador_de_fatura`
- Virtual environment (`venv/`) is gitignored
- Commit meaningful changes with descriptive messages in Portuguese

## Before Making Changes
1. Always activate virtual environment
2. Read existing code to understand patterns
3. Test changes by running the main script
4. Verify PDF output is generated correctly
5. Check that no sensitive data is exposed in commits

## Pull Request Guidance

When prompted with **"draft a pull request"**:

1. **Analyze changes**
   * Compare everything done on the current branch against `master`/`main` branch of `upstream`.
   * Summarize all relevant commits, file modifications, and key impacts.

2. **Create a Markdown draft**
   * Produce content that can be pasted directly into the PR **title** and **description** fields.
   * **Structure** the description with the template imported below: .github/pull_request_template.md
   * Enhance clarity with markdown code fences with language tags, colors, tables, blockquotes for callouts, admonitions (GitHub alerts), mermaid diagrams, images, collapsible details and etc.

3. **Write the Test Guidance section**
   * Assume a tester is going to test the changes proposed on this pull request.
   * Describe step-by-step checks needs to be performed to carefully test it.

4. **Generate a Markdown file**
   * Generate a `pull_request.md` file containing the Pull Request title and description
