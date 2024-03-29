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

# Cooling function
def cool( temperature: int, coolingFactor: int ) -> int:
    temperature *= coolingFactor
    return temperature

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

# Here is main function ...

## Parameters needed
### Parameters for whole algorithm
cases = 50          # <--- Modify if needed
"""
filenames = [
    'tai100_10_1.txt',  'tai100_5_1.txt',   'tai20_20_1.txt',
    'tai50_10_1.txt',   'tai50_5_1.txt',    'tai100_20_1.txt',
    'tai20_10_1.txt',   'tai20_5_1.txt',    'tai50_20_1.txt'
]
"""
filenames = [
    'tai20_5_1.txt',  'tai20_10_1.txt',   'tai20_20_1.txt',
    'tai50_10_1.txt',   'tai50_5_1.txt',    'tai100_20_1.txt',
    'tai100_5_1.txt',   'tai100_10_1.txt',    'tai50_20_1.txt'
]

f2 = open( './statistics/SA.txt', "w")

for each in filenames:
    best = 10000
    worst = 0
    avg = 0
    standardDeviation = 0
    ### Parameters for whole algorithm
    total = 0

    ### Parameters for SA
    epochLength = 10     # <--- Modify if needed
    temperature = 1000  # <--- Modify if needed
    coolingFactor = 0.9   # <--- Modify if needed
    MaxSteps = 1000      # <--- Modify if needed

    f2.write( f'Initial temperature: {temperature}, cooling factor: {coolingFactor}, Epoch length: {epochLength}\n' )

    ## Read Data
    Data = ReadData( './PFSP_benchmark_data_set/' + each )
    machines = Data[0]
    jobs = Data[1]
    data = Data[2]
    plotCase = random.randrange( 0, cases + 1, 1 )
    timeCount = 0

    ## Initial Solution: generating via randomness

    for _ in range( cases ):
        # If you are testing the program, I really recommend to uncomment the following line to print log file?
        #print( f'\t--- In {each} case {_}/50' )
        startTime = time.time()

        sol = [ i for i in range( jobs ) ]
        random.shuffle( sol )
        TestSol = [ i for i in sol ]
        curr = SpantimeCalculate( sol, data, jobs, machines )
        temperature = 1000   # <--- Modify if needed
        steps = 0

        plotX = []
        plotY = []
        for __ in range( MaxSteps ):   # Stopping criteria

            ## Neighborhood Function
            BIFlag = 1
            tmp = 0
            while BIFlag == 1 and tmp < 20:
                tmp += 1
                i = random.randrange( 0, jobs, 1 )
                j = random.randrange( 0, jobs, 1 )
                swap( TestSol, i, j )

                ## Calculate Machine Time
                Time = SpantimeCalculate( TestSol, data, jobs, machines )
                #print(f'curr = {curr}, Time = {Time}, step = {__}, cases = {_}')

                ## Selecting Function
                if Time < curr:
                    curr = Time
                    sol = TestSol
                    BIFlag = 0
                else:
                    #print(f'{math.exp( ( curr - Time ) / temperature )}, {temperature}')
                    if math.exp( ( curr - Time ) / temperature ) > random.uniform( 0.0, 1.0 ):
                        curr = Time
                        sol = TestSol
                        BIFlag = 0

            ## Temperature Control
            steps += 1
            if steps % epochLength == 0:
                temperature = cool( temperature, coolingFactor )

            ## Plot parameters
            if _ == plotCase:
                plotX.append( __ + 1 )
                plotY.append( curr )

        #print( f'\t\tIn {_} round: {curr}' )
        if curr < best:
            best = curr
        if curr > worst:
            worst = curr
        total += curr
        standardDeviation += ( curr * curr )

        # Plot
        if _ == plotCase:
            plt.title( f"SA {each[:-4]}", loc = 'center')
            plt.xlabel("Steps")
            plt.ylabel("makespan")
            plt.plot( plotX, plotY, )
            plt.savefig(f'./statistics/plot/SA/Normal/SA_{each[:-4]}.png')
            plt.clf()

        endTime = time.time()
        timeCount += ( endTime - startTime )

    avg = round( total / cases, 2 )
    standardDeviation = round( math.sqrt( ( standardDeviation / cases ) - ( avg * avg ) ), 2 )
    avgTime = round( timeCount / cases, 2 )

    print( f'In {each}:\n\tBest: {best}\n\tWorst: {worst}\n\tAverage: {avg}\n\tStandard deviation: {standardDeviation}\n\tTime: {avgTime}' )
    f2.write( f'\t{each}\t{best}\t{avg}\t{worst}\t{standardDeviation}\t{avgTime}\n' )
f2.close()
