import numpy as np

# class Carga():

#     def __init__(self, contactores, potencia_carga):

#         self.contactores = contactores
#         self.potencia_carga = potencia_carga

#     def potencias_por_regime(self):
#         potencias_ativas_permanente = []
#         potencias_ativas_curta_duracao = []
#         potencias_reativas_permanente = []
#         potencias_reativas_curta_duracao = []
    
#         for contactor, regime in self.contactores.values():
#             if regime == 'Permanente':
#                 potencia_ativa = self.potencia_ativa(contactor, regime)
#                 potencias_ativas_permanente.append(potencia_ativa)
#                 potencia_reativa = self.potencia_reativa(contactor, regime)
#                 potencias_reativas_permanente.append(potencia_reativa)

#             elif regime == 'Curta duração':
#                 potencia_ativa = self.potencia_ativa(contactor, regime)
#                 potencias_ativas_curta_duracao.append(potencia_ativa)
#                 potencia_reativa = self.potencia_reativa(contactor, regime)
#                 potencias_reativas_curta_duracao.append(potencia_reativa)

#         Pt_permanente = 0
#         Qt_permanente = 0
#         Pt_curta_duracao = 0
#         Qt_curta_duracao = 0

#         for potencia_aparente_permanente in zip(potencias_ativas_permanente, potencias_reativas_permanente):
#             Pt_permanente += potencia_aparente_permanente[0]
#             Qt_permanente += potencia_aparente_permanente[1]
        
#         for potencia_aparente_curta_duracao in zip(potencias_ativas_permanente, potencias_reativas_permanente):
#             Pt_curta_duracao += potencia_aparente_curta_duracao[0]
#             Qt_curta_duracao += potencia_aparente_curta_duracao[1]

#         S_permanente = np.complex(Pt_permanente, Qt_permanente)
#         S_curta_duracao = np.complex(Pt_curta_duracao, Qt_curta_duracao)

#         return S_permanente, S_curta_duracao 

#     def potencia_ativa(self, contactor, regime):
#         #falta adicionar a tabela 6.4
        
#        # potencia_individual_ativa = tab.loc[tab['Contactor'] == contactor], ['Potência Ativa']].values[0,0]
        
#        # return potencia_individual_ativa

#     def potencia_reativa(self, contactor, regime):

#         #potencia_individual_reativa = tab.loc[tab['Contactor'] == contactor], ['Potência Reativa']].values[0,0]
        
#         #return potencia_individual_reativa

#     def fator_potencia(self):

#         S_permanente, S_curta_duracao = self.potencias_por_regime()
#         Fp1 = np.real(S_permanente) / np.absolute(S_permanente)
#         Fp2 = np.real(S_curta_duracao) / np.absolute(S_curta_duracao)
        
#         return Fp1, Fp2
