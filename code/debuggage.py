from sauvegarde import *
import scipy.io
from numpy import argmin
from classes import *
from desscore import *
from simulated_annealing_kOPT import *
from matplotlib import pyplot as plt
instancename = "data/inst1"
instancelist = ["data/inst2"+"data/inst3"]
modele = instance(instancename)


def debug1():
    '''débug naif'''
    nvsol = simulated_annealing_kopt_naif(2, modele, score_naif)
    print(nvsol, score_naif(modele, nvsol))


def debug2():
    '''on print l'évolutions des solutions'''

    nvsol, listnvsol, T = simulated_annealing_kopt_naif(
        2, modele, score_naif, True, 200, 10**-7, 0.999, None, True, 10000)
    fig = plt.figure()
    X = [k for k in range(len(listnvsol))]
    Y = [score_naif(modele, sol) for sol in listnvsol]
    X2 = [k for k in range(len(T))]
    X2P = [200*(0.99**k) for k in range(len(T))]
    Y2 = [score_naif(modele, sol) for sol in T]
    plt.plot(X, Y)
    plt.xlabel(' les solutions retenues par lalgorithmes')
    plt.ylabel(' score de la solution')
    plt.savefig(str(instancename) +
                'X en fonction des solutions retenues'+'.jpg')

    # plt.show()
    plt.close(fig)
    fig = plt.figure()

    plt.plot(X2, Y2)
    plt.xlabel('la température')
    plt.ylabel('le score')
    plt.savefig(str(instancename)+'X en fonction de la température '+'.jpg')

    plt.close(fig)

    fig = plt.figure()
    Y3 = [modele.compute_score(sol.get_sol(), False, False, False, True)[
        1] for sol in listnvsol]
    plt.plot(X, Y3)
    plt.xlabel(' les solutions retenues par lalgorithmes' +
               'avec un nombre de villes dans la simulation'+str(len(nvsol.get_ordre())))
    plt.ylabel(' nb_violation de la solution'
               )

    plt.savefig(str(instancename) +
                'nb_violation en fonction des solutions '+'.jpg')
    plt.close(fig)


'''def debug3():
    solution_init = random_solution(modele)
    ind_a_changer = solution_init.get_random_points(2)
    for perm in permutations(ind_a_changer, 2):
        print(perm)
        nvsol = kopt(modele, solution_init, perm, ind_a_changer)
    print('score1,score2', score_naif(
        modele, solution_init), score_naif(modele, nvsol))
    print('sol', solution_init.get_sol() == nvsol.get_sol())'''


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

# debug4()


def save_ordre(sol, name: '', modele, score, expo_global=4):
    '''Sauvegarde l'ordre dans un fichier'''
    ordre = sol.get_ordre()
    with open(name+'ordre.txt', 'w') as f:
        for k in ordre:
            f.write(str(k)+' ')
        f.write('\n')
        f.write(str(int(score(modele, sol, expo_global))))


def read_ordre(ordre, name: ''):
    '''lit l'ordre dans un fichier'''
    with open(name+'ordre.txt', 'r') as f:
        for line in f:
            ordre.append(int(line))


'''sol = simulated_annealing_kopt_naif(2, modele, score_naif, False)
save_ordre(sol.get_sol(), 'data/inst1', modele, score_naif)
'''

# debug2()


def plot_solution(modele, score: score_naif, sol_ini: None, alpha: 0.999, nb_iter=-1, expo_global=3, k=2):
    '''on print l'évolutions des solutions'''
    print('debut du k-opt de plot_solution')
    nvsol, listnvsol, T = simulated_annealing_kopt_naif(
        k, modele, score_naif, True, 200, 10**-7, alpha, sol_ini, True, nb_iter, expo_global)
    print('fin du k-OPT')
    fig = plt.figure()
    X = [k for k in range(len(listnvsol))]
    Y = [score_naif(modele, sol, expo_global) for sol in listnvsol]
    X2 = [k for k in range(len(T))]
    X2P = [200*(0.99**k) for k in range(len(T))]
    Y2 = [score_naif(modele, sol, expo_global) for sol in T]
    plt.plot(X, Y)
    plt.xlabel(' les solutions retenues par au cours du recuit simulé pour exposant' +
               str(expo_global)+'et au moins,'+str(nb_iter)+'itérations'+'k:'+str(k))
    plt.ylabel(' score de la solution')
    plt.savefig(str(instancename) +
                'X en fonction des solutions retenues'+'_expo_'+str(expo_global)+'alpha_'+str(alpha)+'k_'+str(k)+'.jpg')

    # plt.show()
    plt.close(fig)
    fig = plt.figure()

    plt.plot(X2, Y2)
    plt.xlabel('la température')
    plt.ylabel('le score')
    print('expogloabal', expo_global, 'alpha', alpha)
    plt.savefig(str(instancename)+'X en fonction de la température ' +
                '_expo_'+str(expo_global)+'alpha_'+str(alpha)+'k_'+str(k)+'.jpg')

    plt.close(fig)

    fig = plt.figure()
    Y3 = [modele.compute_score(sol.get_sol(), False, False, False, True)[
        1] for sol in listnvsol]
    plt.plot(X, Y3)
    plt.xlabel(' les solutions retenues par lalgorithmes' +
               'avec un nombre de villes dans la simulation'+str(len(nvsol.get_ordre())))
    plt.ylabel(' nb_violation de la solution'
               )

    plt.savefig(str(instancename) +
                'nb_violation en fonction des solutions '+'_expo_'+str(expo_global)+'alpha_'+str(alpha)+'k_'+str(k)+'.jpg')
    plt.close(fig)


def arendrepourlesprofs():
    # * premier plot pour voir en changeant le alpha ou le expo global
    plot_solution(modele, score_naif, None, 0.99, 30000, 3)
    print('2')
    plot_solution(modele, score_naif, None, 0.99, 30000, 2)
    print('3')
    plot_solution(modele, score_naif, None, 0.999, 30000, 3)
    print('4')
    plot_solution(modele, score_naif, None, 0.999, 30000, 2)


# arendrepourlesprofs()


def arendrepourlesprofs2():
    plot_plusieursCI(modele, score_naif, None, 0.99, 30000, 3)
    print('2')
    plot_solution(modele, score_naif, None, 0.99, 30000, 2)
    print('3')
    plot_solution(modele, score_naif, None, 0.999, 30000, 3)
    print('4')
    plot_solution(modele, score_naif, None, 0.999, 30000, 2)


# aa = '_expo_'+str(expo_global)+'alpha_'+str(alpha)

# plot_plusieursCI()

def arendrepourlesprofs3():
    alphal = [0.99, 0.999]
    expol = [2, 3]
    for alpha1 in alphal:
        for expo1 in expol:
            # plot_plusieursCI(modele, score_naif, 100, None, alpha, expo)
            plot_plusieursCI(modele, score_naif, 100, None, alpha1, -1, expo1)
    # plot_plusieursCI(modele, score_naif, 100, None, 0.999)
    # plot_plusieursCI(modele,score_naif,100,None,0.99)


# arendrepourlesprofs3()


# * Conclusion je crois j'aime bien alpha=0.999 et expo=3
# *  inst1 je sais pas quoi c'est plus pour regarder à l'intérieur de l'algorithme et plusieurs CI la fin uniquement


def arendrepourlesprofs4():
    # * On plot les résultats de inst1 pour 3-OPT uniquement
    plot_solution(modele, score_naif, None, 0.999, -1, 3, 3)


'''
arendrepourlesprofs4()
print('fin avant plusieurs CI ')
plot_plusieursCI(modele, score_naif, 100, None, 0.999, -1, 3, 3)
'''


def compute_kopt(modele, n, score: score_naif, sol_ini: None, alpha: 0.999, nb_iter=-1, expo_global=2, k=2, name='sauvegarde', T_init=200, T_final=10**-7, nb_iter_max=-1):
    L_meilleur = []
    L_intermediaire = []
    print('début de la computation de kopt')
    for i in range(n):
        if i % 10 == 0:
            print('i')
        sol, solint = simulated_annealing_kopt_naif(
            k, modele, score, True, T_init, T_final, alpha, sol_ini, False, nb_iter_max, 3)
        L_meilleur.append(sol.get_ordre())
        L_intermediaire.append([soli.get_ordre() for soli in solint])
    print('fin des itérations')
    '''a1 = np.array(L_meilleur).astype(int)
    a2 = np.array([np.array(L_intermediaire[k]).astype(int)
                  for k in range(len(L_intermediaire))])
    '''
    #print(a2, a2.dtype)
    save_ordre2(L_meilleur, name)
    save_ordre2(L_intermediaire, name+'_ALL_intermediaire')

    '''np.save(name+'.npy', a1)
    #scipy.io.mmwrite(name+'_ALL_intermediaire.mtx', a2)
    np.save(name+'_ALL_intermediaire.npy', a2)'''

    # save_ordre()

    print('fin de la sauvegarde')
    return L_meilleur, L_intermediaire


'''print('passé ici ')
compute_kopt(modele, 2, score_naif, None, 0.999, -1,
             2, 2, '2OPTSCORENAIF', 2000, 10**-3, -1)
'''
'''compute_kopt(modele, 100, score_naif, None, 0.999, -1,
             2, 3, '3OPTSCORENAIF', 2000, 10**-3, -1)'''


def load_solution(name):
    return np.load(name+'.npy')
    # * On peut récuperer la solution avec for k in range(shape(u[0])) et un list(u[k])


def load_solution_liste(name):
    M = np.load(name+'_ALL_intermediaire.npy')
    L = []
    n, m = M.shape

    for i in range(n):
        L.append([list(M[i, j]) for j in range(m)])
    return L
    # * On peut récuperer la solution avec for k in range(shape(u[0])) et un list(u[k])
