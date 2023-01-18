# Sketch de l'algorithme pour 2-OPT
from math import log
from plot import *
from score import load_solution
from classes import *
from recuit_simulé_2OPT import *

from debuggage import *
from desscore import *
n = 200
instancename = "data/inst1"
instancelist = ["data/inst1"+"data/inst2"+"data/inst3"]
modele = instance(instancename)


def test():
    T_bas = 3300
    '''compute_kopt(modele, 4, score_retard, None,
                 0.999, -1, 2, 2, 'test23', T_bas, 1, -1)'''

    plot_solution_ALL_intermediaireMOYENNNE(score_retard, modele,
                                            'test23_ALL_intermediaire', 'testPLOT', particulier=0)

    # L1=1 17 10 20 18 19 11 6 16 2 12 13 7 14 8 3 5 9 21 4 15

    # print(score_retard(modele, l1))
    # score_retard()


print('ici')

print('fin ici')


def bcp_compute():
    n = 100
    instancename = "data/inst1"
    instancelist = ["data/inst1"+"data/inst2"+"data/inst3"]
    modele = instance(instancename)
    nb_iter = 15000
    # * Compute 2-OPT
    Tsup = -log(0.5)/3300*10
    '''compute_kopt(modele, n, score_naif, None, 0.999, -
                 1, 3, 2, '2OPTSCORENAIF', Tsup, 10**-5, -1)
    plot_solution_ALL_intermediaireMOYENNNE(score_naif, modele,
                                            '2OPTSCORENAIF'+'_ALL_intermediaire', 'plot2OPTSCORENAIF', particulier=0)'''
    # compute_kopt()
    # * Compute 3-OPT
    '''compute_kopt(modele, n, score_naif, None, 0.999, 
                 1, 3, 3 '3OPTSCORENAIF', Tsup, 1, -1)'''
    '''compute_kopt(modele, n, score_naif, None, 0.999, -1,
                 3, 3, '3OPTSCORENAIF', Tsup, 10**-8, -1)
    plot_solution_ALL_intermediaireMOYENNNE(score_naif, modele,
                                            '3OPTSCORENAIF'+'_ALL_intermediaire', 'plot3OPTSCORENAIF', particulier=0)'''

    print('Compute 2-OPT but with another score function')
    compute_kopt(modele, n, score_retard, None, 0.999, -1,
                 2, 2, '2OPTscoreretard', 200, 10**-7, -1)
    plot_solution_ALL_intermediaireMOYENNNE(score_retard, modele,
                                            '2OPTscoreretard'+'_ALL_intermediaire', 'plot2OPTSCORERETARD', particulier=0)

    print(' Compute 3-OPT but with another score function')
    compute_kopt(modele, n, score_retard, None, 0.999, -1,
                 2, 3, '3OPTscoreretard', 200, 10**-7, -1)
    plot_solution_ALL_intermediaireMOYENNNE(score_retard, modele,
                                            '3OPTscoreretard'+'_ALL_intermediaire', 'plot3OPTSCORERETARD', particulier=0)


    # * A REPRINT MAIS AVEC UNE SCORE_RETARD ET PAS SCORE_NAIF
instancename = "data/inst1"
modele = instance(instancename)

bcp_compute()
# test()
