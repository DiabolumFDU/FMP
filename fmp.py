'''
This module implement the FM partition algorithm!
'''
from random import random
from random import randint
import time
print("Hello, world!")


nPartition = 2
r = 0.5  #ratio of the sizes of two partitions
t = 5  #From 1 to 49, which is the percantage of tolerance
cost = 0  #The total number of edges cut

#datafile = open('test.hgr')
datafile = open('bigtest0.hgr')
nEdge, nNode = list(map(int, datafile.readline().rstrip().split(' ')))  #Numbers of edges and nodes

edges = []  #For each edge, store the nodeTouched.
for i in datafile:
    edges.append(list(map(int, i.rstrip().split(' '))))

nodes = [[] for i in range(nNode)]  #For each node, store the edgeTouched
for i in range(nEdge):
    for j in edges[i]:
        nodes[j].append(i) #ymc: Caution! List index starts from 0, but name of node starts from 1!!!!

partition = [0 for i in range(nNode)]  #For each node, store the partition
gainByNode = [0 for i in range(nNode)]  #For each node, store the corresponding gain
lockFlag = [0 for i in range(nNode)]  #For each node, store the lock state flag
gainBucket = [{},{}]  #For each partition, store the gains and corresponding nodes. 
partInfo = [[],[]]  #For each partition, store the NUMBER of nodes touched by each edge 


#------Partition Initialize------
#Caution! This global variable is used by most function defined below!!!
#partition = [0,0,1,0,0,0,1,1,0,0,1,1,1,1]  
partition = [0 if random() < r else 1 for i in range(nNode)]
#partition = list(map(int,open('goldenResult.txt').read().rstrip().split('\n')))


#------Find Touched Node------
def findTouched(node):
    nodesTouched = []
    for edgeTouched in nodes[node]:
        nodesTouched += edges[edgeTouched]
    nodesTouched = list(set(nodesTouched))
    nodesTouched.remove(node)
    return nodesTouched


#------Initialization of Partition------
def buildPartition():
    while True:
        curNode = randint(0,nNode-1)
        partition[curNode] = 1
        if sum(partition)/nNode > r: return 0
        nodesTouched = findTouched(curNode)
        for curNode in nodesTouched:
            partition[curNode] = 1
            if sum(partition)/nNode > r: return 0


#buildPartition()

            


#------Is an edge cut?------
def isCut(edge):
    '''This function tells whether an edge is cut'''
    nodesTouched = edges[edge]
    for i in nodesTouched:
        if partition[i] != partition[nodesTouched[0]]:
            return True
    return False


#------Calculate Global Cost------
def calcGlobalCost():
    return  sum(list(map(isCut,range(nEdge))))


#------Build Gain Bucket------
def buildGainBucket():
    gainBucket = [{} for i in range(nPartition)]
    global gainByNode
    gainByNode = list(map(calcGain,range(nNode)))
    for i in range(nNode):
        if gainByNode[i] in gainBucket[partition[i]]:
            gainBucket[partition[i]][gainByNode[i]].append(i)
        else:
            gainBucket[partition[i]][gainByNode[i]]=[i]
    return gainBucket


#------Build PartInfo------
def buildPartInfo():
    partInfo = [[0 for j in range(nEdge)] for i in range(nPartition)]
    for i in range(nEdge):
        for nodeTouched in edges[i]:
            partInfo[partition[nodeTouched]][i] += 1
    return partInfo


#------Calculate Gain------
def calcGain(node):
    gain = 0
    F = partition[node]
    T = 1 - F #ymc: Caution! This is 2-way partition specific!!!
    edgesTouched = nodes[node]
    for i in edgesTouched:
        if partInfo[F][i] == 1: gain += 1
        if partInfo[T][i] == 0: gain -= 1
    return gain
    

#------Move a Node------
def moveNode(node):
    if node == None:
        print('Nothing to move!!!')
        return -1
    #print('Now moving node %d to other partition' % node)
    F = partition[node] #ymc: Caution! This is 2-way partition specific!!!
    T = 1 - F
    lockFlag[node] = 1 #ymc: Modify a global variable
    gainBucket[F][gainByNode[node]].remove(node) #update gainBucket
    if gainBucket[F][gainByNode[node]] == []:
        gainBucket[F].pop(gainByNode[node])
    #Moving a node
    partition[node] = T #ymc: Modify a global variable!!!

    edgesTouched = nodes[node]
    for edgeTouched in edgesTouched:  
        nodesTouched = edges[edgeTouched]

        #Update gain by partInfo before moving
        if partInfo[T][edgeTouched] == 0:
            for nodeTouched in nodesTouched:
                if lockFlag[nodeTouched] == 0:
                    gainBucket[F][gainByNode[nodeTouched]].remove(nodeTouched)
                    if gainBucket[F][gainByNode[nodeTouched]] == []:
                        gainBucket[F].pop(gainByNode[nodeTouched])
                    gainByNode[nodeTouched] += 1 #ymc: Modify a global variable!!!
                    if gainByNode[nodeTouched] in gainBucket[F]:
                        gainBucket[F][gainByNode[nodeTouched]].append(nodeTouched)
                    else:
                        gainBucket[F][gainByNode[nodeTouched]]=[nodeTouched]
        elif partInfo[T][edgeTouched] == 1:
            for nodeTouched in nodesTouched:
                if partition[nodeTouched] == T and lockFlag[nodeTouched] == 0:
                    gainBucket[T][gainByNode[nodeTouched]].remove(nodeTouched)
                    if gainBucket[T][gainByNode[nodeTouched]] == []:
                        gainBucket[T].pop(gainByNode[nodeTouched])
                    gainByNode[nodeTouched] -= 1 #ymc: Modify a global variable!!!
                    if gainByNode[nodeTouched] in gainBucket[T]:
                        gainBucket[T][gainByNode[nodeTouched]].append(nodeTouched)
                    else:
                        gainBucket[T][gainByNode[nodeTouched]]=[nodeTouched]

        #Update partInfo corresponding to the moving
        partInfo[T][edgeTouched] += 1 #ymc: Modify a global variable!!!
        partInfo[F][edgeTouched] -= 1

        #Update gain by partInfo after moving
        if partInfo[F][edgeTouched] == 0:
            for nodeTouched in nodesTouched:
                if lockFlag[nodeTouched] == 0:
                    gainBucket[T][gainByNode[nodeTouched]].remove(nodeTouched)
                    if gainBucket[T][gainByNode[nodeTouched]] == []:
                        gainBucket[T].pop(gainByNode[nodeTouched])
                    gainByNode[nodeTouched] -= 1 #ymc: Modify a global variable!!!
                    if gainByNode[nodeTouched] in gainBucket[T]:
                        gainBucket[T][gainByNode[nodeTouched]].append(nodeTouched)
                    else:
                        gainBucket[T][gainByNode[nodeTouched]]=[nodeTouched]
        elif partInfo[F][edgeTouched] == 1:
            for nodeTouched in nodesTouched:
                if partition[nodeTouched] == F and lockFlag[nodeTouched] == 0:
                    gainBucket[F][gainByNode[nodeTouched]].remove(nodeTouched)
                    if gainBucket[F][gainByNode[nodeTouched]] == []:
                        gainBucket[F].pop(gainByNode[nodeTouched])
                    gainByNode[nodeTouched] += 1 #ymc: Modify a global variable!!!
                    if gainByNode[nodeTouched] in gainBucket[F]:
                        gainBucket[F][gainByNode[nodeTouched]].append(nodeTouched)
                    else:
                        gainBucket[F][gainByNode[nodeTouched]]=[nodeTouched]
    global newCost
    newCost -= gainByNode[node]
    return newCost
            

#------Find Max------
def findMax(x):
    if bool(x) == False: return None
    result = x[0]
    for i in x[1:]:
        if  result < i: result = i
    return result


#------Pick a Node------
def pickNode(F,T):
    #print('from part%d to part%d' % (F,T))
    gains = list(gainBucket[F].keys())
    if gains == []: return None
    gainMax = findMax(gains)
    return gainBucket[F][gainMax][-1] #ymc: !!!


#------One Move------
def oneMove():
    gainMaxs = [findMax(list(gainBucket[i].keys())) for i in range(nPartition)]
    if gainMaxs[0] == None or gainMaxs[1] == None:
        #print('One of the gainBucket is empty!')
        return -1

    #if gainMaxs[0] < 0 and gainMaxs[1] < 0:
        #return -1

    if (sum(partition) + 1)/nNode > r + t/100:
        #print('Imbalance check invalid for 0->1')
        return moveNode(pickNode(1,0))
    if (sum(partition) - 1)/nNode < r - t/100:
        #print('Imbalance check invalid for 1->0')
        return moveNode(pickNode(0,1))

    if gainMaxs[0] > gainMaxs[1]:
        return moveNode(pickNode(0,1))
    elif gainMaxs[0] < gainMaxs[1]:
        return moveNode(pickNode(1,0))
    elif sum(partition)/nNode > r:
        return moveNode(pickNode(1,0))
    else:
        return moveNode(pickNode(0,1))
    
    
#------One Pass------
def onePass():
    global partInfo 
    partInfo = buildPartInfo()  
    global gainBucket 
    gainBucket = buildGainBucket() 
    global lockFlag 
    lockFlag = [0 for i in range(nNode)]
    cost = calcGlobalCost()
    bestPart = partition[:]
    moveCnt = 0
    while True:
        result = oneMove()
        moveCnt += 1
        if result == -1: break
        if result <= cost:
            cost = result
            bestPart = partition[:]
    #print('For one pass, %d moves are done!' % moveCnt)
    return cost, bestPart


#------Main------
cost = calcGlobalCost()
timeCost = 0
newCost = cost
print('Before partition, total cut:', cost)
#print('Initialized partition:', partition)
cnt = 0
resultFile = open('result.txt','w')
statFile = open('statistics.txt','a')

while True:
    print('-'*10, 'Now do Pass', cnt, '-'*10)
    marker0 = time.clock()
    newCost, newPartition = onePass()
    marker1 = time.clock()
    #print('Result of Pass', cnt, ':', newCost, newPartition)
    print('Result of Pass', cnt, ':', newCost)
    timeInteval = marker1 - marker0
    timeCost += timeInteval
    print('Time cost: %.4f seconds' % timeInteval)
    cnt += 1
    change = cost - newCost
    if newCost < cost:
        cost = newCost
        partition = newPartition
    if cost == 0: 
        print('0 cut reached!')
        break
    if change/cost <= 0.01:
        print('Stop next pass!')
        break
for item in partition:
    print(item, file=resultFile)
print('\nFinal result:\nTotal cut:', cost)
print('Ratio: ', sum(partition)/len(partition))
print('Total time cost; %.4f seconds' % timeCost)
print(cost, '%.4f' % timeCost,sep='\t', file=statFile)
    



