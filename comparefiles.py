import cantools
import csv
import can
import os
import os.path

ECUFiles=[]
OtherFiles=[]
LengthsECU=[]
LengthsOther=[]

def readCSV():
    for root, dirs, files in os.walk('./ECUCANData/'):
        for file in files:
            if file.lower().endswith(".csv"):
                #f=open(file, 'r')
                #perform calculation
                #STILL NEED TO CHECK IF DATA IS GOOD
                ECUFiles.append(file)
                #f.close()

    findLength('./ECUCANData/', ECUFiles, LengthsECU)
    # print(LengthsECU)

    for root, dirs, files in os.walk('./OtherCANData/'):
        for file in files:
            if file.lower().endswith(".csv"):
                #f=open(file, 'r')
                #perform calculation
                #STILL NEED TO CHECK IF DATA IS GOOD
                OtherFiles.append(file)
                #f.close()

    findLength('./OtherCANData/', OtherFiles, LengthsOther)
    # print(LengthsOther)

def findLength(pathPrefix, arr, lengths_arr):
    a = 0
    # print(len(arr))
    while a < len(arr):
        with open(pathPrefix + arr[a]) as csv_file:
            #csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            # TO DO: Use readline() instead of readlines() in order to only skip malformed line instead of entire csv
            try:
                for line in csv_file.readlines():
                    line_count += 1
            except:
                print("Malformed packet")
                line_count += 1
            # print(arr[a] + str(line_count))
        lengths_arr.append(line_count)
        a += 1
    # print(lengths_arr)

#Compares lengths between each file of ECU and Other CAN Data, appends next file in ECU files to current ECU file if the lengths
#of current file is less than length of corresponding Other file
def compareLengths(pathPrefix1, pathPrefix2):
    loopcount = len(LengthsECU)
    i = 0
    j = 0
    while i < loopcount:
        if i < len(LengthsECU) and j < len(LengthsOther) and LengthsECU[i] <= LengthsOther[j]:
            LengthsECU[i] = LengthsECU[i] + LengthsECU[i+1]
            LengthsECU.remove(LengthsECU[i+1])
            i -= 1
        i += 1
        j += 1

print('\n')
readCSV()
print('\n')
print('Before comparing lengths:')
print('LengthsECU:')
print(LengthsECU)
print('LengthsOther:')
print(LengthsOther)
compareLengths('./ECUCANData/', './OtherCANData/')
print('\n')
print('After comparing lengths:')
print('LengthsECU:')
print(LengthsECU)
print('LengthsOther:')
print(LengthsOther)
print('\n')
