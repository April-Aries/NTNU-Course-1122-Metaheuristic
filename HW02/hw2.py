from statistics import mean
import random
import math
import matplotlib.pyplot as plt
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

# LOX
def LOX( sol, parent1, parent2, start, end ):
    tmp = [ 0 for i in range(len(sol[parent2]))]
    tmp[start:end] = sol[parent1][start:end]
    tmp[:start] = [-1]*(end-start)

    idx = 0
    for i in range( 0, len(sol[parent2]) ):
        if sol[parent2][i] not in tmp:
            tmp[idx] = sol[parent2][i]
            idx += 1

    sol.append( tmp )


def crossOver( sol, parents, parentNum, start, end):
    for i in range(parentNum):
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

        if best_time < temp_time and best_time != 0:#if record didn't get better
            return best_time
        else:
            sol = swap(sol, List[0], List[1])#into the next round

def selection(sol, IIScore, parentNum):
    for i in range(parentNum):
        idx = IIScore.index( max(IIScore) )
        IIScore.pop(idx)
        sol.pop(idx)

# Here is main function ...

## Parameters needed
### Parameters for whole algorithm
cases = 10      # <--- Modify if needed
filenames = [
    'tai20_5_1.txt',  'tai20_10_1.txt',   'tai20_20_1.txt',
    'tai50_5_1.txt',   'tai50_10_1.txt',    'tai50_20_1.txt',
    'tai100_5_1.txt',   'tai100_10_1.txt',    'tai100_20_1.txt'
]

count = 0
for each in filenames:
    writeFileName = 'TA0' + str( count ) + '1.txt'
    f2 = open( writeFileName, 'w' )
    populationSize = 400
    MaxSteps = 500
    parentNum = 300
    bestSol = [' ', 10000000]
    ## Read Data
    Data = ReadData( './PFSP_benchmark_data_set/' + each )
    machines = Data[0]
    jobs = Data[1]
    data = Data[2]
    
    start = time.time()

    sol = [ [] for i in range(populationSize) ]  # Population size
    IIScore = [ 0 for i in range(populationSize) ]
    
    for iter in range( cases ):
        # Initial Solution
        sol = initialization2(data, jobs, machines, populationSize)

        for i in range(populationSize):
            IIScore[i] = SpantimeCalculate( sol[i], data, jobs, machines) #II( sol[i], data, jobs, machines ) 
    
        for steps in range(MaxSteps):
            parents = Parentselection(parentNum, populationSize, IIScore)

            crossOver( sol, parents, parentNum, jobs//2, jobs )
            mutation(sol, populationSize, jobs)

            for i in range(populationSize,populationSize + parentNum):

                IIScore.append( II( sol[i], data, jobs, machines ) )
            selection(sol, IIScore, parentNum)
            
            end = time.time()
            if (end - start) > 180:
                break

        idx = IIScore.index( min(IIScore) )
        if (bestSol[1] > IIScore[idx]):
            bestSol[0] = sol[idx]
            bestSol[1] = IIScore[idx]

    print(f'{each}\t{bestSol[1]}\t{bestSol[0]}')
    count += 1
