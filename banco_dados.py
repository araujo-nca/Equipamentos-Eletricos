from planilhas import Planilha

leitura = Planilha() 
tab421 = leitura.tabela(sheet_name = "4.21")
tab421 = tab421.replace({'Cabo isolado em XLPE':'XLPE', 'Cabo isolado em EPR':'EPR'})
tab42 = leitura.tabela(sheet_name = "4.2")
tab46 = leitura.tabela(sheet_name = "4.6")
tab47 = leitura.tabela(sheet_name = "4.7")
tab48 = leitura.tabela(sheet_name = "4.8")
tab49 = leitura.tabela(sheet_name = "4.9")