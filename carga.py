import numpy as np

class Carga():

    def __init__(self, contactores, potencia_carga):

        self.contactores = contactores
        self.potencia_carga = potencia_carga

    def potencia_aparente(self):
        potencias_ativa = []
        potencias_reativas = []
    
        #for contactor, regime in self.contactores.values():
            #potencias_ativa = self.potencia_ativa_total(contactor, regime)
            #potencias_reativas = self.potencia_reativa_total(contactor, regime)
        Pt = 0
        Qt = 0
        for potencia_aparente in zip(potencias_ativa, potencias_reativas):
            Pt += potencia_aparente[0]
            Qt += potencia_aparente[1]

        S = np.complex(Pt, Qt)

        return S

    def potencia_ativa_total(self, contactor, regime):
       
        #falta adicionar a tabela 6.4
        #incluir o regime
        #potencia_individual_ativa = tab.loc[tab['Contactor'] == contactor], ['Potência Ativa']].values[0,0]
        #potencias_ativa.append(potencia_individual_ativa)

        #return potencias_ativa

    def potencia_reativa_total(self, contactor, regime):
        #potencia_individual_reativa = tab.loc[tab['Contactor'] == contactor], ['Potência Reativa']].values[0,0]
        #incluir o regime
        #potencias_reativa.append(potencia_individual_reativa)

        #return potencias_reativa

    def fator_potencia(self):

        S_permanente, S_curta_duracao = self.potencia_por_regime()
        Fp1 = np.real(S_permanente) / np.absolute(S_permanente)
        Fp2 = np.real(S_curta_duracao) / np.absolute(S_curta_duracao)
        
        return Fp1, Fp2

    def potencia_por_regime(self):
        #falta sincronizar
        S_permanente = self.potencia_aparente()
        S_curta_duracao = self.potencia_aparente()

        return S_permanente, S_curta_duracao
    
    def impedancia_carga(self):
        #pegar da tabela 6.2