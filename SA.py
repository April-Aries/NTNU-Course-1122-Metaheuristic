import random
import math

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
    temperature -= coolingFactor
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
cases = 20          # <--- Modify if needed
best = 10000
worst = 0
total = 0
avg = 0

### Parameters for SA

epochLength = 10    # <--- Modify if needed
temperature = 1000   # <--- Modify if needed
coolingFactor = 10  # <--- Modify if needed
MaxSteps = 500      # <--- Modify if needed

## Read Data
Data = ReadData( './PFSP_benchmark_data_set/tai50_10_1.txt' )
machines = Data[0]
jobs = Data[1]
data = Data[2]

"""
print(f'There are {machines} machines and {jobs} jobs.\n')
for i in range( machines ):
    for j in range( jobs ):
        print( data[i][j], end = ' ' )
    print('\n', end = '' )
"""

## Encoding Scheme

## Initial Solution

for _ in range( cases ):

    sol = [ i for i in range( jobs ) ]
    TestSol = [ i for i in range( jobs ) ]
    curr = SpantimeCalculate( sol, data, jobs, machines )
    temperature = 1000   # <--- Modify if needed
    steps = 0

    for __ in range( MaxSteps ):   # Stopping criteria

        ## Neighborhood Function
        i = random.randrange( 0, jobs, 1 )
        j = random.randrange( 0, jobs, 1 )
        swap( TestSol, i, j )

        ## Calculate Machine Time
        time = SpantimeCalculate( TestSol, data, jobs, machines )

        ## Selecting Function
        if time < curr:
            curr = time
            sol = TestSol
        else:
            if math.exp( ( time - curr ) / temperature ) < random.uniform( 0.0, 1.0 ):
                curr = time
                sol = TestSol

        ## Temperature Control
        steps += 1
        if steps % epochLength == 0:
            temperature = cool( temperature, coolingFactor )
    
    #print( f'In {_} round: {curr}' )
    if curr < best:
        best = curr
    if curr > worst:
        worst = curr
    total += curr

avg = total / cases

print( f'Best: {best}\nWorst: {worst}\nAverage: {avg}' )
