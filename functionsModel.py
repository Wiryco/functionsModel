import os
import dotenv
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import urllib
import pandas as pd

dotenv.load_dotenv()

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
            
class functions():
    def __init__(self):
        pass