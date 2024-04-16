import statistics
from statistics import mean
import random
import math
import time

from initialization import *
from mating_selection import *

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


def crossOver( sol, parents, parentNum, start, end):
    for i in range(parentNum//2):
        LOX( sol, parents[i][0], parents[i][1], start, end )
        LOX( sol, parents[i][1], parents[i][0], start, end )

def mutation(sol, populationSize, parentNum, jobs, threshold ):
    for i in range(populationSize, populationSize + parentNum):
        mutationRate = random.randrange(0,101,1)
        if mutationRate > threshold:
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

def selection(sol, IIScore, populationSize):
    while len(IIScore) > populationSize:
        idx = IIScore.index( max(IIScore) )
        IIScore.pop(idx)
        sol.pop(idx)

def Parentselection(parentNum, populationSize, IIScore, MatingMethod):
    if MatingMethod == "randomMating":
        return randomMating(parentNum, populationSize, IIScore)
    elif MatingMethod == "ranking":
        return ranking(parentNum, populationSize, IIScore)
    elif MatingMethod == "tournament":
        return tournament(parentNum, populationSize, IIScore)
    

# Here is main function ...

## Parameters needed
### Parameters for whole algorithm
cases = 20     # <--- Modify if needed
filenames = [
    'tai20_10_1.txt', 'tai50_10_1.txt', 'tai100_10_1.txt'
]

count = 0
MatingMethods = ["randomMating","ranking", "tournament"]
for MatingMethod in MatingMethods:
    for each in filenames:
        writeFileName = MatingMethod+"-"+each[:-4]+'.txt'
        f2 = open( writeFileName, 'w' )
        populationSize = 500  # <-- Modify
        parentNum = 100       # <-- Modify
        MaxSteps = 1000
        bestSol = [' ', 10000000]
        ## Read Data
        Data = ReadData( './PFSP_benchmark_data_set/' + each )
        machines = Data[0]
        jobs = Data[1]
        data = Data[2]

        record = []

        IIScore = [ 0 for i in range(populationSize) ]
        stepCount = [ 0 for i in range(cases)]
        
        start = time.time()
        
        for iter in range( cases ):
            # Initial Solution
            sol = randomInit(data, jobs, machines, populationSize)


            for i in range(populationSize):
                IIScore[i] = SpantimeCalculate( sol[i], data, jobs, machines) #II( sol[i], data, jobs, machines ) 

            for steps in range(MaxSteps):
                parents = Parentselection(parentNum, populationSize, IIScore, MatingMethod)

                crossOver( sol, parents, parentNum, jobs//2, jobs )

                mutation(sol, populationSize, parentNum, jobs, 10)

                for i in range(populationSize, populationSize + parentNum):

                    IIScore.append( II( sol[i], data, jobs, machines ) )

                selection(sol, IIScore, populationSize)

                idx = IIScore.index( min(IIScore) )
                if (bestSol[1] > IIScore[idx]):
                    bestSol[0] = sol[idx]
                    bestSol[1] = IIScore[idx]
                
                stepCount[iter] += 1
                end = time.time()
                if (end - start) > 180:
                    break
                    
            record.append(bestSol[1])
           
        f2.write('=== Mating methods Test ===\n')
        f2.write('MatingMethod: '+MatingMethod+'\n')
        f2.write('======================\n')
        f2.write('Best case: '+str(bestSol[1])+'\n')
        f2.write('Average case: '+str(mean(record))+'\n')
        f2.write('Worst case: '+str(max(record))+'\n')
        f2.write('Stdev: '+str(statistics.stdev(record))+'\n')
        f2.write('Steps: '+str(mean(stepCount))+'\n')
        f2.write('Best seq: '+str(bestSol[0])+'\n')


        print(bestSol[1])
        count += 1
