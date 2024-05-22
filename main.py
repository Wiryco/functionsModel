import functionsModel as fm

if __name__ == '__main__':
    # conection = fm.dataBase()

    # sql = """SELECT * FROM automatizacao.CONTATOS_WPP"""
    
    # print(conection.select(query=sql))

    # sql = """EXEC [dbo].[ALTERA_NOME_CONTATO] 3, 'Testando a execução de procedure'"""
    
    # print(conection.execDML(query=sql))

    email = fm.email()

    files = [r'C:\Projetos\teste.pdf', r'C:\Projetos\teste1.pdf']

    email.sendEmail(to='vinicius.anlopes@gmail.com', subject='Teste', msg='Teste', sendFiles=files)