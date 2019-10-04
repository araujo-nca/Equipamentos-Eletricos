import numpy as np 
from planilhas import Planilha

def fluxo_curva_bxh(forca_magnetizante):

    curva_bxh = Planilha("Curva Magnetização", "Ferro")

    H_dado = curva_bxh["H"]
    B_dado = curva_bxh["B"]


    fluxo = np.interp(forca_magnetizante, H_dado.values, B_dado.values)

    return fluxo
