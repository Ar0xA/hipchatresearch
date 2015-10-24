#here we read the results, line by line and add occurances 
#the character per position
import sys,string

#resultfile="room_api2.txt"
resultfile="room_api2.txt"
#resultset will be a dict that holds a twodimensional array
resultSet = {}

for line in file(resultfile,"r"):
    pos=0
    print line.strip()
    for character in line.strip():
        #first, does the character exist in the resultset?
        if not character in resultSet:
            #print "char does not exist in resultset"
            newOccurance={character:{pos:1}}
            resultSet.update(newOccurance)
        else:
            #print "char %s  exists in resultset already" % character
            #lets see if its the same position that it exists in
            tmpResult=resultSet.get(character)
            #lets see if the current position already has a value
            tmpPos=tmpResult.get(pos)
            if tmpPos == None:
                #print "current pos has no entry in resultset yet"
                newTmpPos={pos:1}
                tmpResult.update(newTmpPos)
                replaceSet={character:tmpResult}
                #and lets add it back to the resultSet
                #first remove the old value
                del resultSet[character]
                #and lets add the new one
                resultSet.update(replaceSet)
            else:
                #print "current characer %s in  pos %s already has entry in resultset" % (character,tmpPos)
                #get the current value
                tmpResultNum = tmpPos
                #ok then lets add 1
                tmpResultNum += 1
                #and store it back in tmpResult
                tmpPosStr={pos:tmpResultNum}
                del tmpResult[pos]
                tmpResult.update(tmpPosStr)
                #and lets store that back in the resultSet
                replaceSet={character:tmpResult}
                del resultSet[character]
                resultSet.update(replaceSet)
        pos+=1
print
print "DONE!"
#print resultSet
#alright, now we want the distribution PER pos (0-8) and print out the 
#characters and their count for that pos

posRes={}
plotPos=0
allkeys={}
for plotPos in range(0,9):
    allkeys=dict.fromkeys(string.ascii_lowercase+string.ascii_uppercase+string.digits, 0)
    keyStr=""
    valueStr=""
    #first lets prepare our resultset for this position
    for key, value in resultSet.iteritems():
        tmpVal=value.get(plotPos)
        if not tmpVal == None:
            tmpDict={str(key):tmpVal}
            posRes.update(tmpDict)
    #ok, now fill that into the allkeys dictionary
    for key,value in posRes.iteritems():
        #replace key in allkeys with its current value
        del allkeys[key]
        allkeys.update({key:value})
    print "results for position %i" % plotPos
    print allkeys
    print
#and finally lets make a  CSV out of this to make a graph
#top columns are all the keys, under it the values
#file name is the character position
    for key, value in allkeys.iteritems():
        keyStr=keyStr+str(key)+','
        valueStr=valueStr+str(value)+','
    #remove last ,
    keyStr=keyStr[0:len(keyStr)-1]
    valueStr=valueStr[0:len(valueStr)-1]
    outfile = file("result_"+str(plotPos)+".csv",'w')
    outfile.write(keyStr+'\n')
    outfile.write(valueStr)
        


