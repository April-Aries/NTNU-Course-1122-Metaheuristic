import matplotlib.pyplot as plt
import numpy as np
import random
import statistics as stat
import itertools
import math

## --------------------------------------------------------------------
##  TestFunctions: classic continuous benchmark functions
## --------------------------------------------------------------------

class TestFunction:
    def __init__(self, dim=2, lb=-1., ub=1.):
        self.dim = dim
        self.lb = lb
        self.ub = ub    

class Sphere(TestFunction):      
    def __call__(self, x):
        return sum(e**2 for e in x)
    def __str__(self):
        return f'Sphere (D={self.dim})'

class Schwefel12(TestFunction):
    def __call__(self, x):
        D = len(x)
        return sum([e**2 for e in [sum(x[:i+1]) for i in range(D)]])
    def __str__(self):
        return f'Schwefel1.2 (D={self.dim})'
## --------------------------------------------------------------------
##  Algorithms: differential evolution
## -------------------------------------------------------------------

class Individual:
    def __init__(self, dim):
        self.genes = np.zeros(dim)
        self.obj = 0
    def __lt__(self, rhs):
        return self.obj < rhs.obj

## --------------------------------------------------------------------
def RandInit(genome, lb, ub):
    genome.genes = np.random.uniform(lb, ub, len(genome.genes))

def Evaluate(genome, func):
    genome.obj = func(genome.genes)

def MutateRand1(t, pop, F):
    cand = [pop[i] for i in range(len(pop)) if i!=t]
    r1, r2, r3 = random.sample(cand, 3)
    mutant = Individual(len(pop[0].genes))
    mutant.genes = r1.genes + F*(r2.genes - r3.genes)
    return mutant

def BoundValue(indv, objfunc):
    for i in range(len(indv.genes)):
        if indv.genes[i] < objfunc.lb:
            indv.genes[i] = objfunc.lb
        elif indv.genes[i] > objfunc.ub:
            indv.genes[i] = objfunc.ub

def CrossoverBin(target, mutant, CR):
    D = len(target.genes)
    trial = Individual(D)
    rp = random.randint(0, D-1)
    for i in range(D):
        if i==rp or random.random()<CR:
            trial.genes[i] = mutant.genes[i]
        else:
            trial.genes[i] = target.genes[i]
    return trial
## --------------------------------------------------------------------
class DifferentialEvolution:
    def __init__(self, np = 10, maxgen = 10, CR = 0.5, F = 0.5):
        self.NP_ = np
        self.MaxGen_ = maxgen
        self.CR_ = CR
        self.F_ = F

    def __str__(self):
        return f'DE: {self.NP_}x{self.MaxGen_} w. CR={self.CR_}, F={self.F_}'

    def Solve(self, history, objfunc):
        LB, UB = objfunc.lb, objfunc.ub
        D = objfunc.dim

        CR, F = self.CR_, self.F_
        NP = max(4, self.NP_)
        MaxGen = max(1, self.MaxGen_)

        # ---------- initialization ----------
        pop = [Individual(D) for _ in range(NP)]
        for x in pop:
            RandInit(x, LB, UB)
            Evaluate(x, objfunc)
        history.append(pop)

        # ---------- evolution ----------
        for t in range(MaxGen):
            offspring = []
            for i, x in enumerate(pop):
                m = MutateRand1(i, pop, F)
                BoundValue(m, objfunc)
                tr = CrossoverBin(x, m, CR)
                Evaluate(tr, objfunc)
                if tr.obj <= x.obj:
                    offspring.append(tr)
                else:
                    offspring.append(x)
            pop = offspring
            history.append(pop)            

   
## -------------------------------------------------------------------------------    
def main():
    np.random.seed(0)
    random.seed(0)
    objfunc = Schwefel12(dim=2)

    best_in_runs = []
    de = DifferentialEvolution(np=20, maxgen=50, CR=0.9, F=0.5)

    print(de)
    for r in range(10):
        history = []
        de.Solve(history, objfunc)
        best_in_runs.append(min([x.obj for x in history[-1]]))

    print(' mean:', f'{stat.mean(best_in_runs):.4e}')
    print('worst:', f'{max(best_in_runs):.4e}')
    print('  std:', f'{stat.stdev(best_in_runs):.4e}')
    print()


if __name__ == '__main__':
    main()
