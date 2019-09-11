import pandas as pd 

# Função para ler uma planilha Excel
def tabela(numero_tabela, sheet_name = "Sheet1"):
    """ ----- Função para ler um arquivo do Excel e suas planilhas -----
        Primeiro Argumento é o número da Tabela referente ao livro do Mamede 4ª Ed
        Segundo Argumento é uma string com o nome da planilha"""

    try:
        # Variável que armazena a planilha em formato Pandas    
        sheet = pd.read_excel(f"Tabelas\Tabela {numero_tabela}.xlsx", sheet_name = sheet_name)
    except:
        # Sai do programa caso o nome da planilha esteja errado
        exit(f"Não existe planilha com o nome {sheet_name}")

    return sheet
