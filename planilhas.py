import pandas as pd

def Planilha(equipamento, tabela):
    """Função para criar a tabela de um arquivo do Excel

    Parâmetros:

        equipamento: string

            Equipamento que se precisa consultar a tabela

        tabela: string

            Número da Tabela referente ao livro do Mamede 4ª Ed """

    try:
        # Variável que armazena a planilha em formato Pandas    
        sheet = pd.read_excel(f"Tabelas/{equipamento}.xlsx", sheet_name = tabela)
    except:
        # Sai do programa caso o nome da planilha esteja errado
        exit(f"Não existe planilha com o nome {tabela}")

    return sheet
