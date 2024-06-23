# Arquivo functionsModel com vários exemplos de funções para auxiliar o dia a dia da análise de dados
Repositório dedicado a criação de um arquivo contendo as principais funções utilizadas no dia a dia. <br><br>
Esse projeto foi desenvolvido utilizando linguagem de programação python e tem por objetivo facilitar as atividade rotineiras da análise de dados.

## Requisitos
- Link para download do Python: [Python](https://www.python.org/downloads/)

## Instalação
Para realizar a instalação, siga estas etapas:
1. Clone o repositório do GitHub:
```bash
git clone https://github.com/Wiryco/functionsModel.git
```
2. Instale as dependências usando pip:
```python
pip install -r requirements.txt
```
3. Execute o codigo principal python:
```python
python main.py
```

## Estrutura do projeto
```
projeto/
└── functionsModel.py
└── main.py
└── requirements.txt
└── .env
```

## Configuração do arquivo .env
O arquivo `.env` é usado para armazenar variáveis de ambiente que o seu projeto python precisa para funcionar corretamente.
Aqui está a estrutura básica do arquivo `.env` para este projeto:

```dotenv
# Informações para conexão com o banco de dados
serverName = ''
dataBase = ''
userName = ''
password = ''
driveConnection = 'SQL Server'
schema = ''

# Conexáo com o e-mail
emailHost = 'smtp-mail.outlook.com'
emailPort = '587'
emailUser = ''
emailPassword = ''
emailHtml = ''

# Azure Key Vault
azureTenantId = ''
azureClientId = ''
azureClientSecret = ''
azureVaultUrl = ''
```
