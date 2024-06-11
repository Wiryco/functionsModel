import os
import dotenv
import sqlalchemy as sa
import urllib
import pandas as pd
import smtplib
import codecs
from sqlalchemy.orm import sessionmaker
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential

dotenv.load_dotenv()

class keyVault:
    def __init__(self):
        self.vaultUrl = os.getenv('azureVaultUrl')
        self.tenantId = os.getenv('azureTenantId')
        self.clientId = os.getenv('azureClientId')
        self.clientSecretId = os.getenv('azureClientSecret')

        os.environ['AZURE_TENANT_ID'] = self.tenantId
        os.environ['AZURE_CLIENT_ID'] = self.clientId
        os.environ['AZURE_CLIENT_SECRET'] = self.clientSecretId

    def setCredentials(self):
        credential = ClientSecretCredential(tenant_id=self.tenantId,
                                            client_id=self.clientId,
                                            client_secret=self.clientSecretId,
                                            additionally_allowed_tenants=["*"])
        return credential

    def getSecret(self, secret=str):
        client = SecretClient(vault_url=self.vaultUrl, credential=self.setCredentials())
        return client.get_secret(secret)

class dataBase():
    def __init__(self):
        self.serverName = os.getenv('serverName')
        self.dataBase = os.getenv('dataBase')
        self.userName = os.getenv('userName')
        self.password = os.getenv('password')
        self.drive = os.getenv('driveConnection')
    
    def connectDataBase(self):
        """
        Em caso de não preenchimento dos campos userName e password no .env, a função usa autenticação do Windows para conectar ao banco de dados
        """
        if self.userName and self.password:
            ps = urllib.parse.quote(self.password)

            connection_string = (
                f'Driver=' + self.drive + ';'
                f'Server=' + self.serverName + ';'
                f"Database=" + self.dataBase + ';'
                f'UID=' + self.userName + ';'
                f'PWD=' + ps + ';'
                f"Trusted_Connection=no;"
            )

            connection_url = sa.engine.URL.create(
                "mssql+pyodbc", 
                query={"odbc_connect": connection_string}
            )

            try:
                return sa.create_engine(connection_url,fast_executemany=True)
            except Exception as ex:
                return False, ex
        else:
            connection_string = (
                f'Driver=' + self.drive + ';'
                f'Server=' + self.serverName + ';'
                f"Database=" + self.dataBase + ';'
                f"Trusted_Connection=yes;"
            )

            connection_url = sa.engine.URL.create(
                "mssql+pyodbc", 
                query={"odbc_connect": connection_string}
            )

            try:
                return sa.create_engine(connection_url,fast_executemany=True)
            except Exception as ex:
                return False, ex

    def select(self, query=str):
        return pd.DataFrame(pd.read_sql(sql= query, con=self.connectDataBase()))
    
    def execDML(self, query=str):
        Session = sessionmaker(bind=self.connectDataBase())
        session = Session()

        try:
            session.execute(sa.text(query))
            session.commit()
            return True, "Script executado com sucesso!"
        except Exception as ex:
            session.rollback()
            return False, f"Erro durante a execução do script: {ex}"
        finally:
            session.close()

class email():
    def __init__(self):
        self.host = os.getenv('emailHost')
        self.port = os.getenv('emailPort')
        self.user = os.getenv('emailUser')
        self.password = os.getenv('emailPassword')
        self.html = os.getenv('emailHtml')

    def sendEmail(self, to='', subject='', msg='', sendFiles=[]):
        sendEmail = MIMEMultipart()

        server = smtplib.SMTP(self.host, self.port)
        server.starttls()
        server.login(self.user, self.password)

        if not to:
            print('Destinatário é parâmetro obrigatório para envio de e-mail!')
            return False

        if not subject:
            print('Assunto é parâmetro obrigatório para envio de e-mail!')
            return False

        if not self.html and not msg:
            print('Mensagem ou arquivo html é parâmetro obrigatório para envio de e-mail!')
            return False

        sendEmail['From'] = self.user
        sendEmail['To'] = to
        sendEmail['Subject'] = subject

        if self.html:
            msg_html = codecs.open(r'' + self.html, 'r', "utf-8")
            msg = msg_html.read()
            sendEmail.attach(MIMEText(msg, 'html'))
        elif msg:
            sendEmail.attach(MIMEText(msg, 'plain'))

        if len(sendFiles) > 0:
            for _file in sendFiles:
                with open(_file, "rb") as fil:
                    part = MIMEApplication(fil.read(), Name=os.path.basename(_file))
                    
                part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(_file)
                sendEmail.attach(part)

        try:
            server.sendmail(sendEmail['From'], sendEmail['To'].split(';'), sendEmail.as_string())
            return True
        except Exception as ex:
            server.quit()
            return False, ex
        finally:
            server.quit()
            
class functions():
    def __init__(self):
        pass
