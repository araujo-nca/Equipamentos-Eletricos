import pandas as pd 


def tabela(numero_tabela, sheet = False):
    excel_file = pd.ExcelFile(f"Tabelas\Tabela {numero_tabela}.xlsx")

    sheet_names = excel_file.sheet_names
    if (len(sheet_names) == 1):
        return excel_file.sheet_names[0]


table = tabela(4.1)
    

print(table.head())