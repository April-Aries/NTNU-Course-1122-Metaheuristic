"""
The test.py file is used to test if the makespan function work as expectation.
If you meet any problem using this python file, please contact luke041510@gmail.com or simply create an issue.
To use this file, please insert your makespan calculation function into line 36 and call it in line 56.
Beware of the difference data format between mine and yours.
Happy Coding!
"""

import random

def SpantimeCalculate( sol: list[int], data: list[list[int]], jobs: int, machines: int ) -> int:
    currEnd = [ 0 for i in range( jobs) ]   # Indicate current ending time for each job
    currTime = 0
    for i in range( machines ):
        currTime = currEnd[ sol[0] ]
        for j in range( jobs ):
            currEnd[ sol[j] ] = max( currTime, currEnd[ sol[j] ] ) + data[i][sol[j]]
            currTime = currEnd[ sol[j] ]
    return currTime

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

# Put your makespan calculate function here

if __name__ == '__main__':

    fileName = [
        'tai100_10_1.txt',  'tai100_5_1.txt',   'tai20_20_1.txt',
        'tai50_10_1.txt',   'tai50_5_1.txt',    'tai100_20_1.txt',
        'tai20_10_1.txt',   'tai20_5_1.txt',    'tai50_20_1.txt'
    ]

    for e in fileName:
        Data = ReadData( './PFSP_benchmark_data_set/' + e )
        machines = Data[0]
        jobs = Data[1]
        data = Data[2]

        sol = [ i for i in range( jobs ) ]
        random.shuffle( sol )

        ans1 = SpantimeCalculate( sol, data, jobs, machines )
        ans2 = # Put your function here
        if ans1 == ans2:
            print('* Pass!')
        else:
            print( f'* Fail @ file {e} with input {sol}' )
