# Arquivo functionsModel com vários exemplos de funções para auxiliar o dia a dia da análise de dados
Repositório dedicado a criação de uma automatização para enviar arquivos/mensagens utilizando a linguagem de programação python.

## Funcionalidades principais
- Permite enviar mensagens para uma lista de contatos
- Possibilita o envio de erquivos para uma lista de contatos

## Requisitos
O biblioteca utilizado no desenvolvimento deste projeto, utiliza comandos de teclado no padrão do Windows. Os testes foram realizados com a aplicação do WhatsApp Desktop sendo fixada na primeira posição da barra de tarefas do Windows.
Também é necessário realizar a instalação do SQL Server para coletar os dados dos contatos e a linguagem Python em sua maquina.

- Link para download do Python: [Python](https://www.python.org/downloads/)
- Link para download do SQL: [SQL Server Download](https://www.microsoft.com/pt-br/sql-server/sql-server-downloads)
- Link para download do SSMS: [SQL Server Management Studio (SSMS)](https://aka.ms/ssmsfullsetup)

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

## Instalações de bibliotecas pip
```cmd
pip install -r requirements.txt
```

## Exemplos
Após a execução dos passos descritos anteriormente, é possível obter os dados dos clientes ao executar o seguinte comando no banco de dados:
```sql
SELECT C.*, A.ID_TIPO_ENVIO, B.DESCRICAO_TIPO_ENVIO, A.ID_MENSAGEM, A.CAMINHO_ARQUIVO, D.DESCRICAO_MENSAGEM
FROM automatizacao.CONTROLE_ENVIO_WPP A
JOIN automatizacao.TIPO_ENVIO_WPP B ON A.ID_TIPO_ENVIO = B.ID_TIPO_ENVIO
JOIN automatizacao.CONTATOS_WPP C ON A.ID_CONTATO = C.ID_CONTATO
JOIN automatizacao.MENSAGEM_WPP D ON A.ID_MENSAGEM = D.ID_MENSAGEM
WHERE C.ATIVO = 1
```
Ele vai trazer as seguintes informações:
```sql
ID_CONTATO	NOME	    TELEFONE	ATIVO	ID_TIPO_ENVIO	DESCRICAO_TIPO_ENVIO	ID_MENSAGEM	CAMINHO_ARQUIVO	                  DESCRICAO_MENSAGEM
2	        Nome Teste	99999999	1	    2	            DOCUMENTO	            0	        C:\testeSend\Teste RPA.txt	      NULL
2	        Nome Teste	99999999	1	    2	            DOCUMENTO	            0	        C:\testeSend\Teste RPA.docx	      NULL
2	        Nome Teste	99999999	1	    2	            DOCUMENTO	            0	        C:\testeSend\Teste RPA.pdf	      NULL
2	        Nome Teste	99999999	1	    3	            IMAGEM	                1	        C:\testeSend\harrypotter_2.jpeg	  Olá, tudo bem? Esse é um teste do robo que envia mensagem para os contatos do WhatsApp
```
Esta tabela será lida pela função `consultaDadosCliente`, disponibilizada no arquivo `scripts.py`, que retorna um dataframe contendo todas as informações dos contatos e os repositórios onde o Python vai coletar os arquivos que serão enviados.
O loop `for` percorre todas as posições do dataframe, coletando os dados dos clientes, os arquivos associados e enviando-os separadamente, um a um.
O loop `for` descrito é o seguinte:
```python
for contato in dba.select(query=query.consultaDadosCliente()).itertuples():
    contato_wpp = functions.contatoWpp(dadosContato=contato)

    contato_wpp.eventSelectUser()

    if contato.ID_TIPO_ENVIO == 1 and contato.DESCRICAO_MENSAGEM:
        contato_wpp.eventSendMsg()

    if (contato.ID_TIPO_ENVIO == 2 or contato.ID_TIPO_ENVIO == 3) and contato.CAMINHO_ARQUIVO:
        contato_wpp.eventClickFile()
        contato_wpp.eventSendFile()
```
