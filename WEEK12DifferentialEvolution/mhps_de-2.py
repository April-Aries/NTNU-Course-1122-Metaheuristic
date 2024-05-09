import matplotlib.pyplot as plt
import numpy as np
import random
import statistics as stat
import itertools
import math
from mpl_toolkits import mplot3d

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


## --------------------------------------------------------------------
##  Plotting
## -------------------------------------------------------------------
def DrawContour(func, xlb, xub, ylb, yub):
    x = np.linspace(xlb, xub, 200)
    y = np.linspace(ylb, yub, 200)
    z = [[func([a, b]) for a in x] for b in y]
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.contour(x, y, z, levels=[10**((e-30)/4) for e in range(40)])
    

## -------------------------------------------------------------------
def DrawEvolutionContour(history, objfunc, sleep=0.5):
    if len(history[-1][0].genes)!=2:
        print('Evolution contour is available only for D=2')
        return
    plt.ion()
    plt.gcf().set_size_inches(7, 7)
    for gen, pop in enumerate(history):
        plt.clf()
        plt.title('Generation ' + str(gen))
        for x in pop:
            plt.plot(x.genes[0], x.genes[1], 'ob')
        xmin = min(x.genes[0] for x in pop)
        xmax = max(x.genes[0] for x in pop)
        ymin = min(x.genes[1] for x in pop)
        ymax = max(x.genes[1] for x in pop)
        DrawContour(objfunc, objfunc.lb, objfunc.ub, objfunc.lb, objfunc.ub)
        #DrawContour(objfunc, xmin, xmax, ymin, ymax)
        plt.pause(sleep)
    plt.ioff()
    plt.show()

## -------------------------------------------------------------------------------
def DrawConvergenceBoxplot(history, objfunc, de, yscale='log'):
    plt.figure(figsize=(12, 5))
    plt.yscale(yscale) #yscale can be 'linear'
    plt.xlabel('generations')
    plt.ylabel('objective value')
    plt.boxplot([[x.obj for x in pop] for pop in history])
    L = len(history)
    plt.xticks(range(1, L+1, max(1, L//20)), range(0, L, max(1, L//20)))
    plt.title(str(objfunc))
    plt.savefig(f'./mhps_de-2_pic/ConvergenceBox{de.CR_}_{de.F_}.png') 

## -------------------------------------------------------------------------------
def DrawConvergenceLine(history, objfunc, de, yscale='log'):
    plt.figure(figsize=(12, 5))
    plt.yscale(yscale) #yscale can be 'linear'
    plt.xlabel('generations')
    plt.ylabel('best objective value')
    plt.plot([min([x.obj for x in pop]) for pop in history])
    plt.title(str(objfunc))
    plt.savefig(f'./mhps_de-2_pic/ConvergenceLine{de.CR_}_{de.F_}.png') 
    
## -------------------------------------------------------------------------------
def Draw3Dsurface(objfunc):
    if objfunc.dim!=2:
        print('3D surface is available only for D=2')
        return    
    N = 50
    x = np.outer(np.linspace(objfunc.lb, objfunc.ub, N), np.ones(N))
    y = x.copy().T # transpose
    tx = x.reshape(1,x.size).tolist()[0]
    ty = y.reshape(1,y.size).tolist()[0]
    z = np.array([objfunc([a, b]) for a, b in zip(tx, ty)]).reshape(N,N)

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ax.plot_surface(x, y, z, cmap='viridis', edgecolor='none')
    ax.set_title(f'Surface plot:{str(objfunc)}')
    plt.show()

## -------------------------------------------------------------------------------    
def main():
    np.random.seed(0)
    random.seed(0)
    plt.rcParams['font.family'] = 'Arial'
    
    objfunc = Sphere(dim=2)
    Draw3Dsurface(objfunc)

    CR = [0.1, 0.5, 0.9]
    F = [0.1, 0.5, 0.9]
    for p in CR:        # Usign for loop to automatically run
        for q in F:     # Usign for loop to automatically run

            de = DifferentialEvolution(np=20, maxgen=50, CR=p, F=q)
            history = []
            de.Solve(history, objfunc)
            print(de)
            print("min obj:", min(x.obj for x in history[-1]))
            
            #DrawEvolutionContour(history, objfunc, sleep=0.001) #history: populations in all generations
            DrawConvergenceBoxplot(history, objfunc,de)
            DrawConvergenceLine(history, objfunc,de)
            print('==============================')             # Print a division line...
   

if __name__ == '__main__':
    main()
