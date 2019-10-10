import numpy as np
from PIL import Image
 
class TP():
    """Parâmetros: 
            tensao_primaria_nominal : número
                Tensão nominal no primário do transformador [V].

            tensao_medida_secundario : número (opcional)
                Tensão medida no secundário do transformador [V]."""

    def __init__(self, tensao_primaria_nominal, tensao_medida_secundario = None):
        
        self.tensao_medida_secundario = tensao_medida_secundario
        self.tensao_primaria_nominal = tensao_primaria_nominal
        # Tensão nominal secundária de 115 V
        self.tensao_nominal_secundario = 115
        self.RTPn = None

        if self.tensao_medida_secundario:

            # Calcula a relação de transformaçãoo de potencial nominal
            self.RTPn = self.tensao_primaria_nominal / self.tensao_nominal_secundario

            # Calcula a tensão primária não corrigida do transformador
            self.tensao_primario_nao_corrigida = self.RTPn * tensao_medida_secundario


    def RTPr(self, tensao_primaria_aplicada = None, RTPn = None, erro_relacao_transformacao = None, FCRp = None):
        """Calcula a relação de transformação de potencial real [adimensional].
            A equação utilizada depende de quais parâmetros de entrada serão introduzidos.
        
            Parâmetros:
                tensao_primaria_aplicada : número
                    Tensão aplicada no primário do transformador de potencial [V].
                    
                RTPn : número
                    Relação de transformação de potencial nominal [adimensional].
                    
                erro_relacao_transformacao : número
                    Erro de relação de transformação ('epsilon p') [%].
                    
                FCRp : número
                    Fator de correção de relação percentual [%]."""

        if tensao_primaria_aplicada and self.tensao_medida_secundario:
            # Parâmetros dados: tensao_primaria_aplicada e tensao_medida_secundario
            RTPr = tensao_primaria_aplicada / self.tensao_medida_secundario
        elif RTPn and erro_relacao_transformacao:
            # Parâmetros dados: RTPn e erro_relacao_transformacao
            RTPr = RTPn * (100 - erro_relacao_transformacao) / 100
        elif RTPn and FCRp:
            # Parâmetros dados: RTPn e FCRp
            RTPr = RTPn * FCRp / 100
        else:
            # Quando nenhuma das condições são satisfeitas
            print("RTPr – Parametro nao identificado.")

        return RTPr

    def FCRr_e_FCRp(self, RTPr, RTPn = None):
        """Calcula o fator de correção de relação real e percentual [adimensional, %].
            É necessário chamar dois valores de saída para obtenção de ambos.

            Parâmetros:
                RTPr : número
                    Relação de transformação de potencial real [adimensional].
                    
                RTPn : número
                    Relação de transformação de potencial nominal [adimensional]."""

        if self.RTPn:
            FCRr = RTPr / self.RTPn
        elif RTPn:
            FCRr = RTPr / RTPn
        else:
            print("RTPn nao identificado.")

        FCRp = FCRr * 100

        # Retorna duas saídas, FCP real e percentual
        return FCRr, FCRp

    def erro_relacao_transformacao(self, FCRp_ou_TensaoPrimarioAplicada):
        """Calcula o erro de relação de transformação [%].

            Parâmetros:
                FCRp_ou_TensaoPrimarioAplicada : número
                    Fator de correção de relação percentual OU tensão aplicada no primário do TP [%, V]."""

        if FCRp_ou_TensaoPrimarioAplicada > 200:
            # Entrada igual a tensão aplicada no primário
            TensaoPrimarioAplicada = FCRp_ou_TensaoPrimarioAplicada
            Ep = (self.RTPn * self.tensao_medida_secundario - TensaoPrimarioAplicada) * 100 / TensaoPrimarioAplicada
        else:
            # Entrada igual a FCRp
            FCRp = FCRp_ou_TensaoPrimarioAplicada
            Ep = 100 - FCRp

        return Ep

    def tensao_primario_real(self, Ep):
        """Calcula o valor real da tensão primária [V].
        
            Parâmetros:
                Ep : número
                    Erro de relação de transformação ('epsilon p') [%]."""

        # Variável que recebe a tensão no primário corrigida (valor real)
        v_primario_real = self.tensao_primario_nao_corrigida - (self.tensao_primario_nao_corrigida * Ep / 100)

        return v_primario_real

    def delta_tensao_primario(self, tensao_primario_aplicada, RTPn):
        """Calcula a diferença entre a tensão primária aplicada e a real [V].
        
            Parâmetros:
                tensao_primaria_aplicada : número
                    Tensão aplicada no primário do transformador de potencial [V].
                    
                RTPn : número
                    Relação de transformação de potencial nominal [adimensional]."""

        v_primario_real = self.tensao_medida_secundario * RTPn
        delta_tensao_primario = tensao_primario_aplicada - v_primario_real

        return delta_tensao_primario

    def classe_de_exatidao(self, angulo_fase = None, FCRp = None):
        """Gráfico para definição da classe de exatidão do transformador de potencial.
        
            Parâmetros para visualização:
                angulo_fase : número
                    Defasagem entre a tensão vetorial primária e a tensão vetorial secundária ['].
                
                FCRp : número
                    Fator de correção de relação percentual [%]."""

        img_classe_exatidao = Image.open('figura_classedeexatidao.png')
        img_classe_exatidao.show()

        return
    
    def tensao_secundario(self, RTPn):
        """Calcula a tensão secundária do TP [V].
        
            Parâmetros:
                RTPn : número
                    Relação de transformação de potencial nominal [adimensional]."""
        
        v_secundario = self.tensao_primaria_nominal / RTPn

        return v_secundario
        
    def corrente_carga(self, potencia_carga, FP_carga, tensao_secundario):
        """Calcula a corrente que circula na carga [A].
        
            Parâmetros:
                potencia_carga : número
                    Potência aparente consumida pela carga [VA].
                    
                FP_carga : número
                    Fator de potência da carga [adimensional].
                    
                tensao_secundario : número
                    Tensão secundária do TP [V]."""

        Ic = potencia_carga * FP_carga / tensao_secundario
        
        return Ic

    def queda_de_tensao_circuito(self, corrente_carga, resistencia_condutor, comprimento_condutor):
        """Calcula a queda de tensão no circuito da carga [V].
        
            Parâmetros:
                corrente_carga : número
                    Corrente que circula na carga [A].
                    
                resistencia_condutor : número
                    Resistência do condutor do circuito secundário [mΩ/m].
                    
                comprimento_condutor : número
                    Distância entre o TP e a carga [m]."""

        delta_v_circuito = corrente_carga * resistencia_condutor * (2 * comprimento_condutor) / 1000

        return  delta_v_circuito

    def fator_correcao_relacao_carga_total_secundaria(self, FCRp, tensao_secundario, FP_carga, corrente_carga, comprimento_condutor, resistencia_condutor, reatancia_condutor):
        """Calcula o fator de correção de relação compreendendo a carga e os condutores do circuito secundário [adimensional].
        
            Parâmetros:
                FCRp : número
                    Fator de correção de relação percentual [%].
                    
                tensao_secundario : número
                    Tensão secundária do TP [V].
                    
                FP_carga : número
                    Fator de potência da carga [adimensional].
                    
                corrente_carga : número
                    Corrente que circula na carga [A].
                    
                comprimento_condutor : número
                    Distância entre o TP e a carga [m].
                    
                resistencia_condutor : número
                    Resistência do condutor do circuito secundário [mΩ/m].
                
                reatancia_condutor : número
                    Reatância do condutor do circuito secundário [mΩ/m]."""

        Ic = corrente_carga
        Lc = comprimento_condutor
        Rc = resistencia_condutor
        Xc = reatancia_condutor
        FP = FP_carga
        theta_carga = np.arccos(FP)

        FCRct = FCRp / 100 + (Ic * 2 * Lc) / tensao_secundario * (Rc * FP + Xc * np.sin(theta_carga)) / 1000
        
        return FCRct

    def angulo_fase_total(self, angulo_fase, tensao_secundario, FP_carga, corrente_carga, comprimento_condutor, resistencia_condutor, reatancia_condutor):
        """Calcula o ângulo de fase compreendendo a carga e os condutores do circuito secundário ['].
        
            Parâmetros:
                angulo_fase : número
                    Defasagem entre a tensão vetorial primária e a tensão vetorial secundária ['].
                    
                tensao_secundario : número
                    Tensão secundária do TP [V].
                    
                FP_carga : número
                    Fator de potência da carga [adimensional].
                    
                corrente_carga : número
                    Corrente que circula na carga [A].
                    
                comprimento_condutor : número
                    Distância entre o TP e a carga [m].
                    
                resistencia_condutor : número
                    Resistência do condutor do circuito secundário [mΩ/m].
                
                reatancia_condutor : número
                    Reatância do condutor do circuito secundário [mΩ/m]."""
        
        Ic = corrente_carga
        Lc = comprimento_condutor
        Rc = resistencia_condutor
        Xc = reatancia_condutor
        FP = FP_carga
        theta_carga = np.arccos(FP)

        gamma_ct = angulo_fase + (3.438 * Ic * 2 * Lc) / tensao_secundario * (Rc * np.sin(theta_carga) + Xc * FP) / 1000

        return gamma_ct