import statistics
from statistics import mean
import random
import math
#import matplotlib.pyplot as plt
import time

from initialization import *

# ReadData method
def ReadData( filepath):
    # Open file
    f = open( filepath, "r")

    # Read data
    info = f.readline().split()
    cols = int( info[0] )
    rows = int( info[1] )
    data = [ [ 0 for j in range( cols ) ] for i in range( rows ) ]
    for i in range( rows ):
        rowData = f.readline()[1:-1].split()
        for j in range( cols ):
            data[i][j] = int( rowData[j] )

    # Return
    return rows, cols, data

# Neighborhood function: SWAP
def swap( sol, a, b):
    tmp = 0
    tmp = sol[a]
    sol[a] = sol[b]
    sol[b] = tmp
    return sol

def SpantimeCalculate( sol, data, jobs, machines):
    currEnd = [ 0 for i in range( jobs) ]   # Indicate current ending time for each job
    currTime = 0
    for i in range( machines ):
        currTime = currEnd[ sol[0] ]
        for j in range( jobs ):
            currEnd[ sol[j] ] = max( currTime, currEnd[ sol[j] ] ) + data[i][sol[j]]
            currTime = currEnd[ sol[j] ]
    return currTime

def Parentselection(parentNum, populationSize, IIScore):
    parents = []
    avg = mean(IIScore)
    
    for i in range(parentNum):
        a = random.randrange( 0, populationSize, 1 )
        b = random.randrange( 0, populationSize, 1 )
        """while IIScore[a] > avg and IIScore[b] > avg:
            a = random.randrange( 0, populationSize, 1 )
            b = random.randrange( 0, populationSize, 1 )"""
        parents.append([a, b])
    
    return parents

# OX
def OX( sol, parent1, parent2, start, end ):
    tmp = [ -1 for i in range(len(sol[parent2]))]
    tmp[start:end] = sol[parent1][start:end]
    idx = end
    for i in range( end, len(sol[parent2]) ):
        if sol[parent2][i] not in tmp:
            tmp[idx] = sol[parent2][i]
            idx += 1
            if idx == len(sol[parent2]):
                idx = 0
    for i in range( 0, end ):
        if sol[parent2][i] not in tmp:
            tmp[idx] = sol[parent2][i]
            idx += 1
            if idx == len(sol[parent2]):
                idx = 0
    sol.append( tmp )

# LOX
def LOX( sol, parent1, parent2, start, end ):
    tmp = [ -1 for i in range(len(sol[parent2]))]
    tmp[start:end] = sol[parent1][start:end]
    idx = 0
    for i in range( 0, len(sol[parent2]) ):
        if idx == start:
            idx = end
        if sol[parent2][i] not in tmp:
            tmp[idx] = sol[parent2][i]
            idx += 1
    sol.append( tmp )

# PMX
def PMX( sol, parent1, parent2, start, end ):
    tmp = [ sol[parent2][i] for i in range(len(sol[parent2])) ]
    for i in range( start, end ):
        c = sol[parent2].index(sol[parent1][i])
        tmp[i] = sol[parent1][i]
        tmp[c] = sol[parent2][i]
    sol.append( tmp )

# CX
## Problem: Is CX always start from 0?
def CX( sol, parent1, parent2, start, end ):
    tmp = [ sol[parent2][i] for i in range(len(sol[parent2])) ]
    c = sol[parent1][0]
    while True:
        idx = sol[parent1].index( c )
        c = sol[parent2][idx]
        tmp[idx] = sol[parent1][idx]

def crossOver( sol, parents, parentNum, start, end, crossOverMethod ):
    for i in range(parentNum):
        if crossOverMethod == 'LOX':
            LOX( sol, parents[i][0], parents[i][1], start, end )
            LOX( sol, parents[i][1], parents[i][0], start, end )
        elif crossOverMethod == 'OX':
            OX( sol, parents[i][0], parents[i][1], start, end )
            OX( sol, parents[i][1], parents[i][0], start, end )
        elif crossOverMethod == 'PMX':
            PMX( sol, parents[i][0], parents[i][1], start, end )
            PMX( sol, parents[i][1], parents[i][0], start, end )
        elif crossOverMethod == 'CX':
            CX( sol, parents[i][0], parents[i][1], start, end )
            CX( sol, parents[i][1], parents[i][0], start, end )

def mutation(sol, populationSize, parentNum, jobs, threshold ):
    for i in range(populationSize, populationSize + parentNum):
        mutationRate = random.randrange(0,101,1)
        if mutationRate > threshhold:
            a = random.randrange(0,jobs,1)
            b = random.randrange(0,jobs,1)
            sol[i] = swap( sol[i], a, b )

def II( sol, data, jobs, machines):
    temp_time = 0
    List = [0,0]
    best_time = 0
    for i in range(jobs):
        best_time = temp_time
        temp_time = 100000
        for j in range(jobs):#sub_round
            sol = swap(sol, i, j)
            m_time = SpantimeCalculate(sol, data, jobs, machines)
            sol = swap(sol, i, j)
            if m_time <= temp_time:
                List[0] = sol[i]
                List[1] = sol[j]
                temp_time = m_time

        if best_time < temp_time and best_time != 0:#if record didn't get better
            return best_time
        else:
            sol = swap(sol, List[0], List[1])#into the next round

def selection(sol, IIScore, populationSize):
    while len(IIScore) > populationSize:
        idx = IIScore.index( max(IIScore) )
        IIScore.pop(idx)
        sol.pop(idx)

# Here is main function ...

## Parameters needed
### Parameters for whole algorithm
cases = 20      # <--- Modify if needed
filenames = [
    'tai20_10_1.txt', 'tai50_10_1.txt', 'tai100_10_1.txt'
]

count = 0
cross = ['OX', 'LOX', 'PMX', 'CX']
for crossOverMethod in cross: 
    for each in filenames:
        writeFileName = f'C{crossOverMethod}{each[:-4]}.txt'
        f2 = open( writeFileName, 'w' )
        populationSize = 10  # <-- Modify
        parentNum = 10       # <-- Modify
        MaxSteps = 500
        bestSol = [' ', 10000000]
        ## Read Data
        Data = ReadData( './PFSP_benchmark_data_set/' + each )
        machines = Data[0]
        jobs = Data[1]
        data = Data[2]

        record = []
        
        start = time.time()

        sol = [ [] for i in range(populationSize) ]  # Population size
        IIScore = [ 0 for i in range(populationSize) ]
        stepCount = [ 0 for i in range(cases)]

        for iter in range( cases ):
            # Initial Solution
            #sol = initialization2(data, jobs, machines, populationSize)
            for i in range(populationSize):
                sol[i] = [j for j in range(jobs)]
                random.shuffle(sol[i])

            for i in range(populationSize):
                IIScore[i] = SpantimeCalculate( sol[i], data, jobs, machines) #II( sol[i], data, jobs, machines ) 
        
            for steps in range(MaxSteps):
                parents = Parentselection(parentNum, populationSize, IIScore)

                crossOver( sol, parents, parentNum, jobs//2, jobs, crossOverMethod )
                mutation(sol, populationSize, parentNum, jobs, 50)

                for i in range(populationSize,populationSize + parentNum):
                    IIScore.append( II( sol[i], data, jobs, machines ) )

                idx = IIScore.index( min(IIScore) )
                if (bestSol[1] > IIScore[idx]):
                    bestSol[0] = sol[idx]
                    bestSol[1] = IIScore[idx]

                selection(sol, IIScore, populationSize )
                
                stepCount[iter] += 1
                end = time.time()
                if (end - start) > 180:
                    break

            # Move into for steps <---
            idx = IIScore.index( min(IIScore) )
            record.append(IIScore[idx])

        # Write file
        f2.write(f'=== Mutation Test ===\n')
        f2.write(f'crossover method = {crossOverMethod}\n')
        f2.write(f'======================\n')
        f2.write(f'Best case: {bestSol[1]}\n')
        f2.write(f'Average case: {mean(record)}\n')
        f2.write(f'Worst case: {max(record)}\n')
        f2.write(f'Stdev: {statistics.stdev(record)}\n')
        f2.write(f'Steps: {mean(stepCount)}\n')
        f2.write(f'Best seq: {bestSol[0]}\n')

        print(bestSol[1])
        count += 1
        f2.close()
