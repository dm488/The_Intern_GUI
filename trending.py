import Tkinter,tkFileDialog
from Tkinter import *
import csv

# Solicit user to open a .csv file using tkinter GUI--------------
filename = 'uninitialized'

def getFile():
    global filename
    filename = tkFileDialog.askopenfilename(filetypes=
    [("allfiles","*")])
    print filename
    read = csv.reader(open(filename,"rb"))
    return read

# Convert string into number (keeps decimals, KEEPS SIGN (use for temp shift)
# Returns a single number of type dec-----------------------------
def convertStringT(string):
    a=0
    exp=0
    sign=1
    for i in string:
        if i=='-': continue
        if i in ['0','1','2','3','4','5','6','7','8','9']:
            exp=exp+1
        else: break
    exp=exp-1
    for k in string:
        if k=='-': sign=-1
        if k in ['0','1','2','3','4','5','6','7','8','9']:
            a=int(k)*(10**exp)+a
            exp=exp-1
    return round(sign*a,3)

# Feed an array of strings into the converter-----------
# Returns a vector of numbers of type dec---------------
def convertArrayT(array):
    vector=[]
    for i in array:
        vector.append(convertStringT(i))
    return vector

# Returns the two innermost array values in a new array--
def concatenate(array):
    concatArray=[array[len(array)/2-1], array[len(array)/2]]
    return concatArray

def removeZeroes(array):
    c=0    # indexing
    for i in array:
        if array[c]==0:
            array.remove(0)
            c+=1    # neutralize indexing change if deleting an entry
        c-=1
    return array

# Formats vectors such that they can be written into .csv-
def writerVec1(PN,dB):
    return [PN, dB[0]]

def writerVec2(PN,dB):
    return ['', dB[1]]

# Return whether to use Acc. or regular temperature range
def whatTempToUse(r,temp):
    count=0
    for z in r:
        if temp in z: count+=1
    if count>1:
        if temp=='Cold': return 'Acc. Cold'
        if temp=='Hot': return 'Acc. Hot'
        if temp=='Ambient': return 'Ambient-2'
    else:
        return temp

# Sort a list and get the maximum value
def getMax(array):
    maxi=-100000
    for i in array:
        if i<=-5:
            maxi=max(i,maxi)
    return maxi

def minTrender(array):
    mini=0
    for i in array:
        mini=min(i,mini)
    return mini

def maxTrender(array):
    maxi=0
    for i in array:
        maxi=max(i,maxi)
    return maxi


# Make two vectors the same size (only works on even vectors)
def normalize(a,b):
    if len(a)>len(b):
        rem=(len(a)-len(b))/2
        i=0
        while i<rem:
            a.pop(0)
            a.pop(len(a)-1)
            i+=1
    elif len(b)>len(a):
        rem=(len(b)-len(a))/2
        i=0
        while i<rem:
            b.pop(0)
            b.pop(len(b)-1)
            i+=1
    return [a,b]

# Function for reading and parsing data--------------
##def trending():
##    startCount=0
##    GDCount=0
##    countrej=-1
##    rejectionXVec=[]
##    rejectionYVec=[]
##    dbPointVec=[]
##    mindBVec=[]
##    global numOfWrites
##    global wVec1, wVec2
##    global ind
##    ind = 0
##    cr = getFile()
##    for row in cr:
##        if 'P/N' in row[0]:
##            partNum=row[0]
##        if row[0]=='Relative Group Delay ns':
##                GDCount=0
##        # Count the number of rejection points
##        if startCount==1:
##            # Stop counting when you reach the next section
##            if row[0]=='dB Point':
##                startCount=0
##                GDCount=1
##                continue
##            countrej=countrej+1
##            rejectionXVec.append(row[1])
##            rejectionYVec.append(row[2])
##        if row[0]=='Rejection dB':
##            startCount=1
##
##        # Store dB Points for comparison
##        if GDCount:
##            removeZeroes(convertArray(row))
##            dbPointVec.append(row[3])
##            
##    rejectionXVec=concatenate(convertArray(rejectionXVec))
##    rejectionYVec=concatenate(convertArray(rejectionYVec))
##    dbPointVec=concatenate(convertArray(dbPointVec))
##
##    rejectionPt=min(rejectionXVec)
##    dbPoints=[round(abs(rejectionPt-dbPointVec[0]),3),round(abs(rejectionPt-dbPointVec[1]),3)]
##
##    # Save vectors in a format that can be easily written to a new .csv
####    if numOfWrites==0:
####        wVec1=writerVec1(partNum,dbPoints)
####        wVec2=writerVec2(partNum,dbPoints)
####    else:
##    wVec1.append(writerVec1(partNum,dbPoints))
##    wVec2.append(writerVec2(partNum,dbPoints))
##    
##    numOfWrites+=1

def trending():
    global numOfWrites
    global wVec1, wVec2
    global ind
    startVec=[]
    stopVec=[]
    initialVec=[]
    dbPointVec=[]

    maxPredict=[]

    maxVec=[]
    minVec=[]
    
    chanCount=0
    count=0
    ncount=0
    cr = getFile()
    ok=0
    for row in cr:
        if chanCount==2:
            initial=[i for i,x in enumerate(row) if x == 'Initial']
            dbInd=[i for i,x in enumerate(row) if x == 'Final']  # need to make sure the dB point is at least -5dB
            dbInd[0]+=1
        if chanCount==4:
            start=[i for i,x in enumerate(row) if x == 'Start']
            stop=[i for i,x in enumerate(row) if x == 'Stop']
        if chanCount>0 and chanCount<=4:
            chanCount +=1
        if 'P/N' in row[0]:
            partNum=row[0]
        if 'Channel' in row[0]:
            chanCount = 1
        if 'Relative Group Delay' in row[0]: break
        if ncount > 0 and ncount < count:
            initialVec.append(row[initial[0]])
            maxPredict.append(row[initial[0]+1:dbInd[0]])
            ncount+=1
        if 'dB Point' in row[0]:
            ncount=1
        if count>=1 and ncount==0:
            FC=row[0]
            startVec.append(row[start[0]])
            stopVec.append(row[stop[0]])
            dbPointVec.append(row[dbInd[0]])
            count+=1
        if 'Rejection dB' in row[0]:
            count=1
        
    startVec=normalize(startVec,initialVec)[0]
    stopVec=normalize(stopVec,initialVec)[0]
    initialVec=normalize(startVec,initialVec)[1]
    dbPointVec=normalize(startVec,dbPointVec)[1]

    # Now do analysis on the four vectors obtained
    startVec=convertArrayT(startVec)
    stopVec=convertArrayT(stopVec)
    dbPointVec=convertArrayT(dbPointVec)
    initialVec=convertArrayT(initialVec)

    index=[i for i,x in enumerate(dbPointVec) if x == getMax(dbPointVec)]

    finalStop = stopVec[index[0]] - initialVec[index[0]]
    finalStart = startVec[index[1]] - initialVec[index[1]]
    minVec = maxPredict[index[0]]
    maxVec = maxPredict[index[1]]

    minVec = convertArrayT(minVec)
    maxVec=convertArrayT(maxVec)

    maxiT=maxTrender(maxVec)
    miniT=minTrender(minVec)

    finalStart2 = startVec[index[1]]-maxiT
    finalStop2 = stopVec[index[0]]-miniT

    partNum=partNum+'  Fc '+FC+' MHz'

    wVec1.append([partNum, 'Left Side', finalStop, finalStop2,(abs(finalStop2)+abs(finalStart2))/2])
    wVec2.append(['', 'Right Side', finalStart, finalStart2])

    numOfWrites+=1

# Function for writing to a new csv file-------------
def writer():
    global wVec1, wVec2
    global numOfWrites
    result=open('summary.csv','wb')
    cw=csv.writer(result,dialect='excel')
    for i in range(0,numOfWrites):
        if i==0 and ind==0:
            cw.writerow(['','Side','Ambient->Cold Shift','Ambient->Hot Shift','Average Cold Shift','Average Hot Shift','Average Total Shift'])
            cw.writerow(wVec1[i])
            cw.writerow(wVec2[i])
        elif i==0 and ind==1:
            cw.writerow(['','Side','dB Margin Over Initial Ambient','Minimum dB Margin Over All Phases','Absolute Average Minimum (Among Both Sides)'])
            cw.writerow(wVec1[i])
            cw.writerow(wVec2[i])
        else:
            cw.writerow(wVec1[i])
            cw.writerow(wVec2[i])
    secondWindowOpen=0
    result.close()

# Function for taking the trend of temperature shifts in vacuum
def tempShift():
    startCount=0
    chanCount=0
    countrej=-1
    rejectionXVec=[]
    rejectionYVec=[]
    dbPointVec=[]
    mindBVec=[]
    coldVec=[]
    hotVec=[]
    ambVec=[]
    finalCVec=[]
    finalHVec=[]
    finalAVec=[]
    dbRef=[]
    takeTempData=0
    global numOfWrites
    global wVec1, wVec2
    global ind
    ind = 0
    cr = getFile()
    for row in cr:
        if chanCount==2:
            cold=[i for i,x in enumerate(row) if x == whatTempToUse(row,'Cold')]
            hot=[i for i,x in enumerate(row) if x == whatTempToUse(row,'Hot')]
            amb=[i for i,x in enumerate(row) if x == whatTempToUse(row,'Ambient')]
            dbInd=[i for i,x in enumerate(row) if x == 'Final']  # need to make sure the dB point is at least -5dB
            dbInd[0]+=1
        if chanCount>0 and chanCount<=2:
            chanCount +=1
        if 'P/N' in row[0]:
            partNum=row[0]
        if 'Channel' in row[0]:
            chanCount = 1
        if 'Relative Group Delay' in row[0]:
            takeTempData = 0
        if takeTempData == 1:
            FC=row[0]
            coldVec.append(row[cold[0]])
            hotVec.append(row[hot[0]])
            ambVec.append(row[amb[0]])
            dbRef.append(row[dbInd[0]])
        if 'dB Point' in row[0]:
            takeTempData = 1

    # Now do analysis on the four vectors obtained
    coldVec=convertArrayT(coldVec)
    hotVec=convertArrayT(hotVec)
    ambVec=convertArrayT(ambVec)
    dbRef=convertArrayT(dbRef)

    # Remove all non-relevant entries to the lists
    index=[i for i,x in enumerate(dbRef) if x == getMax(dbRef)]

    finalCVec.append(coldVec[index[0]])
    finalCVec.append(coldVec[index[1]])
    finalHVec.append(hotVec[index[0]])
    finalHVec.append(hotVec[index[1]])
    finalAVec.append(ambVec[index[0]])
    finalAVec.append(ambVec[index[1]])

    partNum=partNum+'  Fc '+FC+' MHz'

    a=[partNum,round((finalCVec[0]-finalAVec[0]),3),round((finalHVec[0]-finalAVec[0]),3)]
    b=['','Right Side',round((finalCVec[1]-finalAVec[1]),3),round((finalHVec[1]-finalAVec[1]),3)]

    wVec1.append([a[0],'Left Side',a[1],a[2],(a[1]+b[2])/2,(a[2]+b[3])/2,((a[1]+b[2])/2 + (a[2]+b[3])/2)/2])
    wVec2.append(b)

    numOfWrites+=1

#--------GLOBAL--INITIALIZATIONS-------------------------
wVec1=[]
wVec2=[]
ind=1
numOfWrites=0

#--------------------------------------------------------
#------------BEGIN---------------------------------------
#--------------------------------------------------------
# Set up buttons-----------------------------------------


main_window = Tk()

label=Label(main_window, text="Trending Analysis", background='white', foreground='black',
            font='Times 40', relief='groove', borderwidth=7)
label.grid(row=0, column=1)
choose_button = Button(main_window, text="Rejection Margin", font='Times 20', command=trending)
choose_button.grid(row=2, column=0)
write_button = Button(main_window, text="Writer", font='Times 20', command=writer)
write_button.grid(row=3, column=1)
quit_button = Button(main_window, text="Quit", font='Times 20', command=main_window.destroy)
quit_button.grid(row=4, column=1)
quit_button = Button(main_window, text="Temp Shift", font='Times 20', command=tempShift)
quit_button.grid(row=2, column=2)
label=Label(main_window, text="Please open only valid .csv files.", background='white', foreground='black',
            font='Times 12', relief='groove', borderwidth=7)
label.grid(row=2, column=1)



mainloop()
