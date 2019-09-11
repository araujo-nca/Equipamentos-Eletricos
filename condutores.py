import pandas as pd 

# Função para ler uma planilha Excel
def tabela(numero_tabela, sheet_name = "Sheet1"):
    """ ----- Função para ler um arquivo do Excel e suas planilhas -----
        Primeiro Argumento é o número da Tabela referente ao livro do Mamede 4ª Ed
        Segundo Argumento é uma string com o nome da planilha"""

def tabela(numero_tabela, sheet = False):
    excel_file = pd.read_excel(f"Tabelas\Tabela {numero_tabela}.xlsx")
    
    return excel_file
