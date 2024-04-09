import random
import math
import matplotlib.pyplot as plt
import time

# ReadData method
def ReadData( filepath: str ) -> tuple[ int, int, list[ list[ int ] ] ]:
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
def swap( sol: list[int], a: int, b: int ) -> list[ int ]:
    tmp = 0
    tmp = sol[a]
    sol[a] = sol[b]
    sol[b] = tmp
    return sol

#
def SpantimeCalculate( sol: list[int], data: list[list[int]], jobs: int, machines: int ) -> int:
    currEnd = [ 0 for i in range( jobs) ]   # Indicate current ending time for each job
    currTime = 0
    for i in range( machines ):
        currTime = currEnd[ sol[0] ]
        for j in range( jobs ):
            currEnd[ sol[j] ] = max( currTime, currEnd[ sol[j] ] ) + data[i][sol[j]]
            currTime = currEnd[ sol[j] ]
    return currTime

def Parentselection():
    parent1 = random.randrange( 0, 4, 1 )
    parent2 = random.randrange( 0, 4, 1 )
    parent3 = random.randrange( 0, 4, 1 )
    parent4 = random.randrange( 0, 4, 1 )
    return parent1, parent2, parent3, parent4

# LOX
def LOX( sol, parent1, parent2, start, end ):
    tmp = [ 0 for i in range(end)]
    tmp[0:start] = sol[parent1][0:start]
    idx = start
    for i in range( 0,len(sol[parent2]) ):
        if not sol[parent2][i] in tmp:
            tmp[idx] = sol[parent2][i]
            idx += 1
    sol.append( tmp )

def crossOver( sol, parent1, parent2, parent3, parent4, start, end ):
    idx = populationSize
    LOX( sol, parent1, parent2, start, end )
    LOX( sol, parent2, parent1, start, end )
    LOX( sol, parent3, parent4, start, end )
    LOX( sol, parent4, parent3, start, end )

def mutation(sol, populationSize, jobs):
    threshhold = 70
    for i in range(populationSize, populationSize*2):
        mutationRate = random.randrange(0,101,1)
        if mutationRate > threshhold:
            a = random.randrange(0,jobs,1)
            b = random.randrange(0,jobs,1)
            sol[i] = swap( sol[i], a, b )

def II( sol: list[int], data: list[list[int]], jobs: int, machines: int ):
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

def selection(sol, IIScore):
    for i in range(populationSize):
        idx = IIScore.index( min(IIScore) )
        IIScore.pop(idx)
        sol.pop(idx)

# Here is main function ...

## Parameters needed
### Parameters for whole algorithm
cases = 3          # <--- Modify if needed
filenames = [
    'tai20_5_1.txt',  'tai20_10_1.txt',   'tai20_20_1.txt',
    'tai50_5_1.txt',   'tai50_10_1.txt',    'tai50_20_1.txt',
    'tai100_5_1.txt',   'tai100_10_1.txt',    'tai100_20_1.txt'
]

count = 0
for each in filenames:
    writeFileName = 'TA0' + str( count ) + '1.txt'
    f2 = open( writeFileName, 'w' )
    populationSize = 4
    MaxSteps = 500

    ## Read Data
    Data = ReadData( './PFSP_benchmark_data_set/' + each )
    machines = Data[0]
    jobs = Data[1]
    data = Data[2]

    for _ in range( cases ):
        # Initial Solution
        sol = [ [] for i in range(populationSize) ]  # Population size
        IIScore = [ 0 for i in range(populationSize) ]
        for i in range( populationSize ):
            sol[i] = [ j for j in range( jobs ) ]
            random.shuffle( sol[i] )

        for i in range(populationSize):
            IIScore[i] = II( sol[i], data, jobs, machines )
    
        for steps in range(MaxSteps):
            parent1, parent2, parent3, parent4 = Parentselection()
            #print('\tParents:', parent1, parent2, parent3, parent4)
            crossOver( sol, parent1, parent2, parent3, parent4, jobs//2, jobs )
            #print('\tCrossOver')
            mutation(sol, populationSize, jobs)
            #print('\tmutation')
            #print('\tsol size: ', len( sol ))
            for i in range(populationSize,populationSize*2):
                #print(f'\t\t{populationSize}, {populationSize*2}, {i}')
                IIScore.append( II( sol[i], data, jobs, machines ) )
            selection(sol, IIScore)
            #print('\tselection')
    idx = IIScore.index( min(IIScore) )
    print(f'{each}\t{IIScore[idx]}\t{sol[idx]}')
    for i in range(jobs):
        f2.write( f'{sol[i]} ' )
    f2.close()
    count += 1
