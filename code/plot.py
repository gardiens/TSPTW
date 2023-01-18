
from math import sqrt
from sauvegarde import *
import scipy.io
from numpy import argmin
from classes import *
from desscore import *
from simulated_annealing_kOPT import *
from matplotlib import pyplot as plt
instancename = "data/inst1"
instancelist = ["data/inst1"+"data/inst2"+"data/inst3"]
modele = instance(instancename)


def plot_plusieursCI(modele, score: score_naif, nb_iter: 10, sol_ini: None, alpha: 0.99, nb_iterdansOPT=-1, expo_global=4, kopt=2):
    ''' Renvoie un graphique où on teste différentes solutions initiales'''
    list_sol = []
    print('début du calcul pour plusieurs CI ')
    for k in range(nb_iter):
        if k % 10 == 0:
            print('on en a déjà calculé:', k)
        sol = simulated_annealing_kopt_naif(
            kopt, modele, score_naif, False, 200, 10**-7, alpha, sol_ini, False, nb_iterdansOPT, expo_global)
        list_sol.append(sol)
    fig = plt.figure()
    X = [k for k in range(len(list_sol))]
    Y = [score_naif(modele, sol, expo_global) for sol in list_sol]
    plt.plot(X, Y)
    plt.xlabel('Différentes solutions initiales (randomisées aléatoirement)')
    plt.ylabel('le score de chaque solution')
    plt.savefig(str(instancename)+'plusieursCI' +
                '_expo_'+str(expo_global)+'alpha_'+str(alpha)+'k'+str(kopt)+'.jpg')
    plt.close(fig)

    i = argmin(Y)

    # print(i)
    sol = list_sol[int(i)]
    save_ordre(sol, str(instancename)+'plusieursCI' +
               '_expo_'+str(expo_global)+'alpha_'+str(alpha), modele, score, expo_global)


def plot_solution_simple(score: score_naif, modele: modele, namsol='sauvegarde', namesauvegarde='ASAUVEGARDER', particulier=-1):
    '''on print l'évolutions des solutions en supposant déjà compute
    namsol est où le fichier a été sauvegardé, namesauvegarde est le nom du fichier où on sauvegarde ( SANS LE JPG)'''

    listnvsol = load_solution2(namsol)
    fig = plt.figure()
    if particulier == -1:
        X = [k for k in range(len(listnvsol))]

        Y = [score(modele, sol) for sol in listnvsol]
    else:
        X = [k for k in range(len(listnvsol))]
        for sol in listnvsol:
            print(sol)
        Y = [score(modele, sol) for sol in listnvsol]
    '''X2=[k for k in range(len(T))]
    X2P=[200*(0.99**k) for k in range(len(T))]'''
    '''Y2=[score_naif(modele, sol) for sol in T]'''
    plt.plot(X, Y)
    plt.xlabel(' les solutions retenues par au cours du recuit simulé')

    plt.ylabel(' score de la solution')
    plt.savefig(namesauvegarde+'.jpg')
    plt.close(fig)

    Y3 = [modele.compute_score_with_mat(sol, False, False, False, True)[
        1] for sol in listnvsol]
    plt.plot(X, Y3)
    plt.xlabel(' les solutions retenues par au cours du recuit simulé')
    plt.ylabel(' nb_violation de la solution'
               )

    plt.savefig(namesauvegarde+'nb_violation'+'.jpg')

    plt.close(fig)


def plot_solution_ALL_intermediaire(score: score_naif, modele: modele, namsol='sauvegarde', namesauvegarde='ASAUVEGARDER', particulier=-1):
    '''on print l'évolutions des solutions en supposant déjà compute
    namsol est où le fichier a été sauvegardé, namesauvegarde est le nom du fichier où on sauvegarde ( SANS LE JPG)'''

    listnvsol = load_solution2(namsol)
    fig = plt.figure()
    X = [k for k in range(len(listnvsol[particulier]))]
    Y = [score(modele, sol) for sol in listnvsol[particulier]]
    '''X2=[k for k in range(len(T))]
    X2P=[200*(0.99**k) for k in range(len(T))]'''
    '''Y2=[score_naif(modele, sol) for sol in T]'''
    plt.plot(X, Y)
    plt.xlabel(' les solutions retenues par au cours du recuit simulé')
    for sol in listnvsol[particulier]:
        print(score(modele, sol))
    plt.ylabel(' score de la solution')
    plt.savefig(namesauvegarde+'.jpg')
    plt.close(fig)
    fig = plt.figure()
    Y3 = [modele.compute_score_with_mat(sol, False, False, False, True)[
        1] for sol in listnvsol[particulier]]
    plt.plot(X, Y3)
    plt.xlabel(' les solutions retenues par au cours du recuit simulé')
    plt.ylabel(' nb_violation de la solution'
               )

    plt.savefig(namesauvegarde+'nb_violation'+'.jpg')

    plt.close(fig)


def plot_solution_ALL_intermediaireMOYENNNE(score: score_naif, modele: modele, namsol='sauvegarde', namesauvegarde='ASAUVEGARDER', particulier=-1):
    '''on print l'évolutions des solutions en supposant déjà compute
    namsol est où le fichier a été sauvegardé, namesauvegarde est le nom du fichier où on sauvegarde ( SANS LE JPG)'''
    print('début de plot des solutions MOYENNES')
    listnvsol = load_solution2(namsol)
    fig = plt.figure()
    # * On transforme la data en nombre
    Y = []
    for listsol in listnvsol:
        Y.append([score(modele, sol) for sol in listsol])
    X = [k for k in range(len(listnvsol[0]))]
    # * On fait la moyenne
    Ymoy = []
    Ymoysup = []
    Ymoyinf = []
    for k in range(len(Y[0])):

        Ymoy.append(sum([Y[i][k] for i in range(len(Y))])/len(Y))
        n = len(Y)
        nb = sum([(Y[i][k]-Ymoy[k])**2 for i in range(len(Y))])
        Ymoysup.append(
            Ymoy[k]+sqrt(1/n*nb))
        Ymoyinf.append(
            Ymoy[k]-sqrt(1/n*nb))
    '''X2=[k for k in range(len(T))]

    X2P=[200*(0.99**k) for k in range(len(T))]'''
    '''Y2=[score_naif(modele, sol) for sol in T]'''
    plt.plot(X, Ymoy, color='red', label='la valeur moyenne trouvé')
    plt.plot(X, Ymoysup, color='blue',
             label='Intervalle de confiance supérieur')
    # Add a legend to the plot

    plt.plot(X, Ymoyinf, color='green', label='IC de confiance inférieur')
    plt.xlabel(' les solutions retenues par au cours du recuit simulé')
    '''for sol in listnvsol[particulier]:
        print(score(modele, sol))'''
    plt.ylabel(' score de la solution')
    plt.savefig(namesauvegarde+'.jpg')
    plt.close(fig)
    fig = plt.figure()
    Y3 = []
    for listsol in listnvsol:
        Y3.append([modele.compute_score_with_mat(sol, False, False, False, True)[
            1] for sol in listsol])
        '''print('OUI OUI')'''
    Y3moy = []
    Y3moysup = []
    Y3moyinf = []
    for k in range(len(Y[0])):

        Y3moy.append(sum([Y3[i][k] for i in range(len(Y3))])/len(Y3))
        n = len(Y)
        nb2 = sum([(Y3[i][k]-Y3moy[k])**2 for i in range(len(Y3))])
        Y3moysup.append(
            Y3moy[k]+sqrt(1/n*nb2))
        Y3moyinf.append(
            Y3moy[k]-sqrt(1/n*nb2))
    '''Y3 = [modele.compute_score_with_mat(sol, False, False, False, True)[
        1] for sol in listnvsol[particulier]]'''
    # Y3 = []

    # plt.plot(X, Y3moy)
    plt.plot(X, Y3moy, color='red', label='la valeur moyenne trouvé')
    plt.plot(X, Y3moysup, color='blue',
             label='Intervalle de confiance supérieur')
    # Add a legend to the plot

    plt.plot(X, Y3moyinf, color='green', label='IC de confiance inférieur')
    plt.xlabel(' les solutions retenues par au cours du recuit simulé')
    plt.ylabel(' nb_violation de la solution'
               )

    plt.savefig(namesauvegarde+'nb_violation'+'.jpg')

    plt.close(fig)
