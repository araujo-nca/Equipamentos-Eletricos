import numpy as np
from banco_dados import tab641, tab642
class Carga():
    """Parâmetros: 
            contactores : dicionario que armazena a corrente do contator como chave e o tipo de regime como item
                Uma lista que armazena os valores das correntes dos contactores.

            potencia_carga : float
                A potência da carga à ser conectada no secundário do TP. """

    
    def __init__(self, contactores, potencia_carga):

        # recebe o dicionario de contactores
        self.contactores = contactores
        # recebe a potencia da carga
        self.potencia_carga = potencia_carga

    
    def potencias_por_regime(self):
        """ Função que calcula as potências ativa e reativa para cada tipo de regime 

            Return : Potência aparente complexa em regime permanente e curta duração."""

        # lista que armazena as potencias ativas em regime permanente
        potencias_ativas_permanente = []
        # lista que armazena as potencias ativas em curta duracao
        potencias_ativas_curta_duracao = []
        # lista que armazena as potencias reativas em regime permanente
        potencias_reativas_permanente = []
        # lista que armazena as potencias reativas em regime curta duracao
        potencias_reativas_curta_duracao = []
    
        # laco para acessar as correntes dos contactores e os regimes para cada um
        for contactor, regime in self.contactores.values():
            # condicao para regime permanente
            if regime == 'Permanente':
                # recebe a potencia ativa para um contactor
                potencia_ativa = self.potencia_ativa(contactor, regime)
                # adiciona a potencia ativa em uma lista de potencias ativas para regime permanente
                potencias_ativas_permanente.append(potencia_ativa)
                # recebe a potencia reativa para um contactor
                potencia_reativa = self.potencia_reativa(contactor, regime)
                # adiciona a potencia reativa em uma lista de potencias ativas para regime permanente
                potencias_reativas_permanente.append(potencia_reativa)
            # condicao para regime em curta duração 
            elif regime == 'Curta duração':
                # recebe a potencia ativa para um contactor 
                potencia_ativa = self.potencia_ativa(contactor, regime)
                # adiciona a potencia ativa em uma lista de potencias ativas para regime curta duracao
                potencias_ativas_curta_duracao.append(potencia_ativa)
                # recebe a potencia reativa para um contactor 
                potencia_reativa = self.potencia_reativa(contactor, regime)
                # adiciona a potencia reativa em uma lista de potencias ativas para regime curta duracao
                potencias_reativas_curta_duracao.append(potencia_reativa)

        # inicia a potencia ativa permanente
        Pt_permanente = 0
        # inicia a potencia reativa permanente
        Qt_permanente = 0
        # inicia a potencia ativa curta duracao
        Pt_curta_duracao = 0
        # inicia a potencia reativa curta duracao
        Qt_curta_duracao = 0

        # laco para acessar a potencia aparente 
        for potencia_aparente_permanente in zip(potencias_ativas_permanente, potencias_reativas_permanente):
            # recebe a potencia ativa permanente
            Pt_permanente += potencia_aparente_permanente[0]
            # recebe a potencia reativa  
            Qt_permanente += potencia_aparente_permanente[1]
        
        # laco para acessar a potencia aparente
        for potencia_aparente_curta_duracao in zip(potencias_ativas_permanente, potencias_reativas_permanente):
            # potencia ativa curta duracao  
            Pt_curta_duracao += potencia_aparente_curta_duracao[0]
            # potencia reativa curta duracao
            Qt_curta_duracao += potencia_aparente_curta_duracao[1]

        # recebe a potencia complexa permanente
        S_permanente = np.complex(Pt_permanente, Qt_permanente)
        # recebe a potencia complexa curta duracao
        S_curta_duracao = np.complex(Pt_curta_duracao, Qt_curta_duracao)

        return S_permanente, S_curta_duracao 

    def potencia_ativa(self, contactor, regime):
        """ Função que calcula as potências ativa para o regime permanente e regime curta duracao

            Return : Potência ativa em regime permanente e regime curta duracao."""

        # condicao para regime em curta duracao
        if regime == "Curta_Duracao":
            # potencia ativa para determinado contactor
            potencia_individual_ativa = tab641.loc[tab641['Contactor'] == contactor, ['Potência Ativa']].values[0,0]
            return potencia_individual_ativa
       
        # condicao para regime permanente
        elif regime == "Regime_Permanente":
            # potencia ativa para determinado contactor
            potencia_individual_ativa = tab642.loc[tab642.loc['Contactor'] == contactor, ['Potência Ativa']].values[0,0]
            return potencia_individual_ativa

    
    def potencia_reativa(self, contactor, regime):
        """ Função que calcula as potências reativa para o regime permanente

            Return : Potência aparente complexa em regime permanente."""

        if regime == "Curta_Duracao":
            # potencia ativa para determinado contactor
            potencia_individual_reativa = tab641.loc[tab641['Contactor'] == contactor, ['Potência Reativa']].values[0,0]
            return potencia_individual_reativa
        
        elif regime == "Regime_Permanente":
            # potencia ativa para determinado contactor
            potencia_individual_reativa = tab642.loc[tab642['Contactor'] == contactor, ['Potência Reativa']].values[0,0]
            return potencia_individual_reativa

    def fator_potencia(self):
        """ Função que calcula os fatores de potencias

            Return : Fator de potencia para regime permanente e fator de potencia regime curta duracao"""

        # recebe a potencia complexa em regime permanente e potencia complexa em curta duracao
        S_permanente, S_curta_duracao = self.potencias_por_regime()
        # recebe o fator de potencia para regime permanente
        Fp1 = np.real(S_permanente) / np.absolute(S_permanente)
        # recebe o fator de potencia para regime curta duracao
        Fp2 = np.real(S_curta_duracao) / np.absolute(S_curta_duracao)
        
        return Fp1, Fp2
