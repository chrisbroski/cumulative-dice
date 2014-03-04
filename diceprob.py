#!/usr/bin/python
 
"Utility functions for cumulative discrete probability (dice) calculations"
 
def probDist(bunchOfDice):
    """
        Accepts a list of lists of uniformly distributed options.
        Returns a dict of probability distribution with
        roll total as key, probability as value.
         
        Example:
            probDist([[1,2], [1,2,3,4]])
        Will return:
            {2: 0.125, 3: 0.25, 4: 0.25, 5: 0.25, 6: 0.125}
    """
     
    maxCombs = __distMaxComb(bunchOfDice)
    allCombs = __dictSumComb(bunchOfDice, maxCombs)
     
    return dict([(x, float(allCombs[x]) / maxCombs[0]) for x in allCombs])
 
 
def __distMaxComb(listDice):
    """
        Input a list of lists. Output a dict of maximum combinations for each die group.
        Optimized: It used to just return one value at a time, but now returns all in a dict.
    """
 
    maxCombGroup = {}
    for ii in range(len(listDice)+1):
        maxCombGroup[ii] = 1
         
        leftDie = [len(x) for x in listDice[ii:]]
        for ll in leftDie:
            maxCombGroup[ii] *= ll
     
    return maxCombGroup
 
 
def __dictSumComb(bunchOfDice, maxCombs):
    """
        Returns a dict of totals and the number of times they occur.
        Optimized: added dieLengths and eachDie vars, integer division
    """
     
    dictComb = {}
    dieLengths = [len(x) for x in bunchOfDice]
    eachDie = range(len(bunchOfDice))
     
    for ii in range(maxCombs[0]):
        sumComb = 0
        for iDie in eachDie:
            sumComb += bunchOfDice[iDie][ii//maxCombs[iDie+1] % dieLengths[iDie]]
         
        if sumComb in dictComb:
            dictComb[sumComb] += 1
        else:
            dictComb[sumComb] = 1
         
    return dictComb
 
 
def chanceToBeatNum(probDistToRoll, numToBeat):
    "Add up all probabilities in a distribution greater than the numToBeat"
    return sum([probDistToRoll[x] for x in probDistToRoll if x > numToBeat])
 
 
def chanceToBeatDie(probDistToRoll, probDistToBeat):
    """
        Sum all probabilities in the distribution probDistToRoll greater
        than all probabilities in the distribution probDistToBeat
    """
    return sum([chanceToBeatNum(probDistToRoll, x) * probDistToBeat[x] for x in probDistToBeat])
 
 
if __name__ == "__main__":
    probDist2d6 = probDist([range(1,7),range(1,7)])
    probDist3d6 = probDist([range(1,7),range(1,7),range(1,7)])
    ThreeBeatsTwo = chanceToBeatDie(probDist3d6, probDist2d6)
     
    print('Odds a 3d6 will beat a 2d6: ' + str(round(ThreeBeatsTwo,4)*100) + '%')
