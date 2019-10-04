import numpy as np

class Dmg():
    
    def __init__(self):
        pass

    def tres_cabos_unipolares(self, diametro):
        """Calcula a distância média geométrica no arranjo de 3 cabos unipolares.
        
            Parâmetros:
                diametro : número
                    Diâmetro do condutor unipolar."""

        Dmg = diametro

        return Dmg

    def um_cabo_tripolar(self, diametro):
        """Calcula a distância média geométrica no arranjo de 1 cabo unipolar.
        
            Parâmetros:
                diametro : número
                    Diâmetro do condutor unipolar."""

        Dmg = diametro

        return Dmg

    def tres_cabos_unipolares_em_triangulo_equilatero(self, distancia):
        """Calcula a distância média geométrica no arranjo de 3 cabos unipolares em triângulo equilátero.
        
            Parâmetros:
                distancia : número
                    Distância entre os condutores unipolares."""

        Dmg = distancia

        return Dmg
        
    def tres_cabos_unipolares_igualmente_espacados(self, distancia):
        """Calcula a distância média geométrica no arranjo de 3 cabos unipolares igualmente espaçados.
        
            Parâmetros:
                distancia : número
                    Distância entre os condutores unipolares."""

        Dmg = 1.26 * distancia

        return Dmg

    def tres_cabos_unipolares_espacados_assimetricamente(self, distancia_1, distancia_2, distancia_3):
        """Calcula a distância média geométrica no arranjo de 3 cabos unipolares espaçados assimetricamente.
        
            Parâmetros:
                distancia_1 : número
                    Distância 1 entre os condutores unipolares.
                    
                distancia_2 : número
                    Distância 2 entre os condutores unipolares.
                    
                distancia_3 : número
                    Distância 3 entre os condutores unipolares."""

        # Dmg recebe a raiz cubica da soma das distancias ao quadrado
        Dmg = np.cbrt(distancia_1**2 + distancia_2**2 + distancia_3**2)

        return Dmg