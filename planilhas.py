import pandas as pd

class Planilha():
    """ ----- Classe para criar a tabela de um arquivo do Excel -----
        Primeiro Argumento é o número da Tabela referente ao livro do Mamede 4ª Ed
        Segundo Argumento é uma string com o nome da planilha"""

    def tabela(self, equipamento, tabela):

        try:
            # Variável que armazena a planilha em formato Pandas    
            sheet = pd.read_excel(f"Tabelas/{equipamento}.xlsx", sheet_name = tabela)
        except:
            # Sai do programa caso o nome da planilha esteja errado
            exit(f"Não existe planilha com o nome {tabela}")

        return sheet
