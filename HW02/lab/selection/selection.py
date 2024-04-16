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
    
    for i in range(0, parentNum, 2):
        a = random.randrange( 0, populationSize, 1 )
        b = random.randrange( 0, populationSize, 1 )

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

def crossOver( sol, parents, parentNum, start, end):
    for i in range(parentNum//2):
        LOX( sol, parents[i][0], parents[i][1], start, end )
        LOX( sol, parents[i][1], parents[i][0], start, end )

def mutation(sol, populationSize, jobs):
    threshhold = 50
    for i in range(populationSize, populationSize+4):
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
                break

        if best_time < temp_time and best_time != 0:#if record didn't get better
            return best_time
        else:
            sol = swap(sol, List[0], List[1])#into the next round

# def selection(sol, IIScore, populationSize):
#     while len(IIScore) > populationSize:
#         idx = IIScore.index( max(IIScore) )
#         IIScore.pop(idx)
#         sol.pop(idx)

# def selection(sol,IIScore,populationSize,parentNum):#all child
#     mid_place = parentNum
#     parent_list = IIScore[:mid_place]
#     child_list = IIScore[mid_place:]
#     parent_sol = sol[:mid_place]
#     child_sol = sol[mid_place:]

#     while len(IIScore) >= populationSize and parent_list :
        
#         parent_idx = parent_list.index(max(parent_list))
#         parent_list.pop(parent_idx)
#         parent_sol.pop(parent_idx)
#     IIScore = parent_list+child_list
#     sol = parent_sol + child_sol

    
#         #print(len(sol))
#         #print(len(IIScore))
#     # print("parent:"+str(len(parent_list)))
#     # print("child:"+str(len(child_list)))
#     return sol, IIScore


def selection(sol,IIScore,populationSize,parentNum):#50-50
    mid_place = 400
    parent_list = IIScore[:mid_place]
    child_list = IIScore[mid_place:]
    parent_sol = sol[:mid_place]
    child_sol = sol[mid_place:]
    while len(IIScore) > populationSize and parent_list and child_list:
        parent_idx = parent_list.index(max(parent_list))
        child_idx = child_list.index(max(child_list))
        parent_list.pop(parent_idx)
        
        child_list.pop(child_idx)
        parent_sol.pop(parent_idx)
        child_sol.pop(child_idx)
        IIScore = parent_list+child_list
        sol = parent_sol + child_sol
        # print(parent_idx,child_idx)
    
    
    return sol, IIScore

# Here is main function ...

## Parameters needed
### Parameters for whole algorithm
cases = 20      # <--- Modify if needed
filenames = [
    'tai20_10_1.txt', 'tai50_10_1.txt', 'tai100_10_1.txt'
]

count = 0
for each in filenames:
    writeFileName = each[:-4] + '.txt'
    f2 = open( writeFileName, 'w' )
    populationSize = 500  # <-- Modify
    parentNum = 100        # <-- Modify
    MaxSteps = 1000
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

            crossOver( sol, parents, parentNum, jobs//2, jobs )
            mutation(sol, populationSize, jobs)

            for i in range(populationSize,populationSize + parentNum):
                IIScore.append( II( sol[i], data, jobs, machines ) )

            idx = IIScore.index( min(IIScore) )
            if (bestSol[1] > IIScore[idx]):
                bestSol[0] = sol[idx]
                bestSol[1] = IIScore[idx]

            sol, IIScore = selection(sol, IIScore, populationSize,parentNum )
            
            stepCount[iter] += 1
            end = time.time()
            if (end - start) > 180:
                break

        # Move into for steps <---
        idx = IIScore.index( min(IIScore) )
        record.append(IIScore[idx])

    # Write file
    f2.write('=== Selecting Test ===\n')
    f2.write('selecting method: 50parents-50child\n')
    f2.write('======================\n')
    f2.write('Best case: '+str(bestSol[1])+'\n')
    f2.write('Average case: '+str(mean(record))+'\n')
    f2.write('Worst case: '+str(max(record))+'\n')
    f2.write('Stdev: '+str(statistics.stdev(record))+'\n')
    f2.write('Steps: '+str(mean(stepCount))+'\n')
    f2.write('Best seq: '+str(bestSol[0])+'\n')

    print(bestSol[1])
    count += 1
    f2.close()