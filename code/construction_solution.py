''' COnstruction de solutoion faisabke '''
# * Useless

from classes import *


# load the instance in the file given in argument


def load_instance(inst_name):
    ''' Load an instance from a file and return a dictionary with the following structure:
    instance = {int: {x,y,wstart,wend},...}
    where int is the number of the node, x and y are the coordinates of the node, wstart and wend are the start and end of the time window'''
    f = open(inst_name, "r")
    # ignoring the beginning
    vals = list(filter(None, f.readline().split(" ")))
    while(not vals[0].isdigit()):
        vals = list(filter(None, f.readline().split(" ")))

    inst = {
        vals[0]: {
            "x": float(vals[1]),
            "y": float(vals[2]),
            "wstart": float(vals[4]),
            "wend": float(vals[5]),
        }
    }
    while vals and vals[0].isdigit() and int(vals[0]) < 999:
        inst[vals[0]] = {"x": float(vals[1]), "y": float(
            vals[2]), "wstart": float(vals[4]), "wend": float(vals[5])}
        vals = list(filter(None, f.readline().split(" ")))

    return inst


def solution_par_wstart(inst_name):
    inst = load_instance(inst_name)
    modele = instance(inst_name)
    # On trie les noeuds par wstart
    inst_sorted = sorted(inst.items(), key=lambda x: x[1]['wstart'])
    # On crée la solution
    L = list([inst_sorted[k][0] for k in range(len(inst_sorted))])
    return solution(modele, L)


instname = 'data/inst1'

#print('ICI', solution_par_wstart(instname))


def solution_par_wend(inst_name):
    inst = load_instance(inst_name)
    modele = instance(inst_name)
    # On trie les noeuds par wstart
    inst_sorted = sorted(inst.items(), key=lambda x: x[1]['wend'])
    # On crée la solution
    L = [inst_sorted[k][0] for k in range(len(inst_sorted))]
    return solution(modele, L)


'''print(solution_par_wend(instname))
'''
