import pandas as pd

class Leitura():
    """ ----- Classe para criar a tabela de um arquivo do Excel -----
        Primeiro Argumento é o número da Tabela referente ao livro do Mamede 4ª Ed
        Segundo Argumento é uma string com o nome da planilha"""

    def tabela_condutores(self, sheet_name):

        try:
            # Variável que armazena a planilha em formato Pandas    
            sheet = pd.read_excel("/home/deilson/Equipamentos-Eletricos/tabelas_condutores.xlsx", sheet_name = sheet_name)
        except:
            # Sai do programa caso o nome da planilha esteja errado
            exit("Não existe planilha com o nome {sheet_name}")

        return sheet
    
    def tabela_TP(self, sheet_name):

        try:
            # Variável que armazena a planilha em formato Pandas    
            sheet = pd.read_excel("/home/deilson/Equipamentos-Eletricos/tabelas_TP.xlsx", sheet_name = sheet_name)
        except:
            # Sai do programa caso o nome da planilha esteja errado
            exit("Não existe planilha com o nome {sheet_name}")

        return sheet
