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
    print(LengthsECU)

    for root, dirs, files in os.walk('./OtherCANData/'):
        for file in files:
            if file.lower().endswith(".csv"):
                #f=open(file, 'r')
                #perform calculation
                #STILL NEED TO CHECK IF DATA IS GOOD
                OtherFiles.append(file)
                #f.close()

    findLength('./OtherCANData/', OtherFiles, LengthsOther)
    print(LengthsOther)

def findLength(pathPrefix, arr, lengths_arr):
    a = 0
    print(len(arr))
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
            print(arr[a] + str(line_count))
        lengths_arr.append(line_count)
        a += 1
    print(lengths_arr)

#Compares lengths between each file of ECU and Other CAN Data, appends next file in ECU files to current ECU file if the lengths
#of current file is less than length of corresponding Other file
def compareLengths(pathPrefix1, pathPrefix2)
    with open(pathPrefix1) as csv_file1, open(pathPrefix2) as csv_file2:
        ECUIndex = 0
        for lOther in LengthsOther:
            if lOther > LengthsECU[ECUIndex]:
                ECUWriter = csv.writer(csv_file1)
                otherWriter = csv.writer(csv_file2)
                ECUWriter.writerow([LengthsOther[ECUIndex], csv_file2])
                ECUIndex = ECUIndex + 1


readCSV()
compareLengths()
