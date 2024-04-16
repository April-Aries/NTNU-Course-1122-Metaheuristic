import random

def randomMating(parentNum, populationSize, IIScore):
    parents = []
    
    for i in range(0, parentNum, 2):
        parent1 = random.randrange( 0, populationSize, 1 )
        parent2 = random.randrange( 0, populationSize, 1 )
        parents.append([parent1, parent2])
    
    return parents
    
def ranking(parentNum, populationSize, IIScore):
    parents = []
    tmp_parent = [i for i in range(populationSize)]
    tmp_IIScore = list(IIScore)
    
    sorted_lists = sorted(zip(tmp_IIScore, tmp_parent))
    tmp_IIScore, tmp_parent = zip(*sorted_lists) 
    tmp_parent = list(tmp_parent)
    rank = []
    #print(tmp_parent)
    #print(tmp_IIScore)
    for i in range(populationSize-1, 0, -1):
        r = round((0.5/populationSize + 1.5/populationSize*i/(populationSize-1))*populationSize)
        if r == 0:
            break
        rank.append(r)  
    
    for i in range(0, parentNum, 2):
        #print(rank, tmp_parent)
        idx1 = random.randrange( 0, len(rank), 1 )
        parent1 = tmp_parent[idx1]
        rank[idx1] -= 1
        if rank[idx1] == 0:
            rank.pop(idx1)
            tmp_parent.pop(idx1)
            
        idx2 = random.randrange( 0, len(rank), 1 )
        parent2 = tmp_parent[idx2]
        rank[idx2] -= 1
        if rank[idx2] == 0:
            rank.pop(idx2)
            tmp_parent.pop(idx2)
        
        parents.append([parent1, parent2])
        
    return parents
    
def tournament(parentNum, populationSize, IIScore):
    parents = []
    
    cmp_code = [random.randrange( 0, populationSize, 1 ) for i in range(parentNum*2)]

    for i in range(0, len(cmp_code), 4):
        parent1 = IIScore.index( min(IIScore[cmp_code[i]], IIScore[cmp_code[i+1]]))
        parent2 = IIScore.index( min(IIScore[cmp_code[i+2]], IIScore[cmp_code[i+3]]))
        parents.append([parent1, parent2])

    return parents