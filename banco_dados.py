from planilhas import Leitura

planilha = Leitura() 

tab421 = planilha.tabela_condutores(sheet_name = "4.21")
tab421 = tab421.replace({'Cabo isolado em XLPE':'XLPE', 'Cabo isolado em EPR':'EPR'})
tab42 = planilha.tabela_condutores(sheet_name = "4.2")
tab46 = planilha.tabela_condutores(sheet_name = "4.6")
tab47 = planilha.tabela_condutores(sheet_name = "4.7")
tab48 = planilha.tabela_condutores(sheet_name = "4.8")
tab49 = planilha.tabela_condutores(sheet_name = "4.9")

tab621 = planilha.tabela_TP(sheet_name = "6.2.1")
tab622 = planilha.tabela_TP(sheet_name = "6.2.2")
tab641 = planilha.tabela_TP(sheet_name = "6.4.1")
tab642 = planilha.tabela_TP(sheet_name = "6.4.2")
tab66 = planilha.tabela_TP(sheet_name = "6.6")

