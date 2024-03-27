import random
import math
import matplotlib.pyplot as plt

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


def SA( f2, temperature: int, coolingFactor: float, epochLength: int, dataset: str, plotFolder: str, modification ):
    t = temperature
    # Parameters for statistics
    best = 10000
    worst = 0
    avg = 0
    standardDeviation = 0
    total = 0
    # Parameters for SA
    cases = 20          # <--- Modify if needed
    MaxSteps = 1000      # <--- Modify if needed

    # Write log file
    print( f'Initial temperature: {temperature}, cooling factor: {coolingFactor}, Epoch length: {epochLength}\n' )
    f2.write( f'Initial temperature: {temperature}, cooling factor: {coolingFactor}, Epoch length: {epochLength}\n' )

    ## Read Data
    Data = ReadData( './PFSP_benchmark_data_set/' + dataset )
    machines = Data[0]
    jobs = Data[1]
    data = Data[2]
    plotCase = random.randrange( 0, cases + 1, 1 )

    ## Iteration for 'cases' times
    for _ in range( cases ):
        ### Initial Solution: generating via randomness
        sol = [ i for i in range( jobs ) ]
        TestSol = [ i for i in sol ]
        curr = SpantimeCalculate( sol, data, jobs, machines )
        temperature = t # <--- Modify if needed
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
                time = SpantimeCalculate( TestSol, data, jobs, machines )
                #print(f'curr = {curr}, time = {time}, step = {__}, cases = {_}')

                ## Selecting Function
                if time < curr:
                    curr = time
                    sol = TestSol
                    BIFlag = 0
                else:
                    #print(f'{math.exp( ( curr - time ) / temperature )}, {temperature}')
                    if math.exp( ( curr - time ) / temperature ) > random.uniform( 0.0, 1.0 ):
                        curr = time
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
            plt.title( f"SA {dataset[:-4]} T = {t} F = {coolingFactor} EL = {epochLength}", loc = 'center')
            plt.xlabel("Steps")
            plt.ylabel("makespan")
            plt.plot( plotX, plotY, )
            plt.savefig(f'./statistics/plot/SA/{plotFolder}/SA_{plotFolder}_{modification}.png')
            plt.clf()
    # Evaluate statistics
    avg = round( total / cases, 2 )
    standardDeviation = round( math.sqrt( ( standardDeviation / cases ) - ( avg * avg ) ), 2 )

    # Write log file
    print( f'{dataset[:-4]}:\n\tBest: {best}\n\tWorst: {worst}\n\tAverage: {avg}\n\tStandard deviation: {standardDeviation}' )
    f2.write( f'\t{dataset[:-4]}\t{best}\t{avg}\t{worst}\t{standardDeviation}\n' )


# Here is main function ...
if __name__ == '__main__':
    f2 = open( f'./statistics/SA_temperature.txt', "w")
    # SA sub experiment: initial temperature
    SA( f2, temperature = 9000, coolingFactor = 0.9, epochLength = 10, dataset = 'tai20_5_1.txt', plotFolder = 'temperature', modification = 9000 )
    SA( f2, temperature = 6000, coolingFactor = 0.9, epochLength = 10, dataset = 'tai20_5_1.txt', plotFolder = 'temperature', modification = 6000 )
    SA( f2, temperature = 3000, coolingFactor = 0.9, epochLength = 10, dataset = 'tai20_5_1.txt', plotFolder = 'temperature', modification = 3000 )
    SA( f2, temperature = 1000, coolingFactor = 0.9, epochLength = 10, dataset = 'tai20_5_1.txt', plotFolder = 'temperature', modification = 1000 )
    f2.close()

    # SA sub experiment: cooling factor
    f2 = open( f'./statistics/SA_coolingFactor.txt', "w")
    SA( f2, temperature = 1000, coolingFactor = 0.95, epochLength = 10, dataset = 'tai20_5_1.txt', plotFolder = 'coolingFactor', modification = 0.95 )
    SA( f2, temperature = 1000, coolingFactor = 0.9, epochLength = 10, dataset = 'tai20_5_1.txt', plotFolder = 'coolingFactor', modification = 0.9 )
    SA( f2, temperature = 1000, coolingFactor = 0.85, epochLength = 10, dataset = 'tai20_5_1.txt', plotFolder = 'coolingFactor', modification = 0.85 )
    SA( f2, temperature = 1000, coolingFactor = 0.8, epochLength = 10, dataset = 'tai20_5_1.txt', plotFolder = 'coolingFactor', modification = 0.8 )
    f2.close()

    # SA sub experiment: epoch length
    f2 = open( f'./statistics/SA_epochLength.txt', "w")
    SA( f2, temperature = 1000, coolingFactor = 0.9, epochLength = 20, dataset = 'tai20_5_1.txt', plotFolder = 'epochLength', modification = 20 )
    SA( f2, temperature = 1000, coolingFactor = 0.9, epochLength = 10, dataset = 'tai20_5_1.txt', plotFolder = 'epochLength', modification = 10 )
    SA( f2, temperature = 1000, coolingFactor = 0.9, epochLength = 5, dataset = 'tai20_5_1.txt', plotFolder = 'epochLength', modification = 5 )
    SA( f2, temperature = 1000, coolingFactor = 0.9, epochLength = 1, dataset = 'tai20_5_1.txt', plotFolder = 'epochLength', modification = 1 )
    f2.close()
