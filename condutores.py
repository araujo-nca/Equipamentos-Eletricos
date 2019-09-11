import pandas as pd 


def tabela(numero_tabela, sheet = False):
    excel_file = pd.read_excel(f"Tabelas\Tabela {numero_tabela}.xlsx")
    
    return excel_file
