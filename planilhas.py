import pandas as pd
import platform

sistema = platform.system() 

def Planilha(equipamento, tabela):
    """Função para criar a tabela de um arquivo do Excel

    Parâmetros:

        equipamento: string

            Equipamento que se precisa consultar a tabela

        tabela: string

            Número da Tabela referente ao livro do Mamede 4ª Ed """

    
    try:
        # Variável que armazena a planilha em formato Pandas    
        if(sistema == "Windows"):
            sheet = pd.read_excel(f"Tabelas/{equipamento}.xlsx", sheet_name = tabela)
        
        # Fiz isso pois não sei se o diretório no sistema linux funciona da mesma maneira. Caso tenha erro, mudar essa parte do código.
        elif(sistema == "Linux"):
            sheet = pd.read_excel(f"Tabelas/{equipamento}.xlsx", sheet_name = tabela)

        else:
            exit("Sistema Operacional não reconhecido.")

    except:
        # Sai do programa caso o nome da planilha esteja errado
        exit(f"Não existe planilha com o nome {tabela}")

    return sheet



def main():
    tabela = Planilha("Transformador de Corrente", "5.5")

    tensao = tabela[15]
    ampere_espira = tabela.set_index("Ampéres - espiras (AS)")

    print(tabela.columns)
    print(tabela)
    print(ampere_espira)


if __name__ == "__main__":
    main()