import os
import subprocess
from subprocess import PIPE, run
import time
import datetime
import csv


print("_"*40)
os.system("echo Welcome to USB History Logger")
nuid = input("Please enter your NUID to start: \n")
print("_"*40)
cmd = "system_profiler SPUSBDataType | grep \"Serial Number\" -B5"

start_date = datetime.date.today()
end_date = start_date + datetime.timedelta(days=7)

print("_"*40)
print("We are starting on: {}".format(start_date))
print("We will be sending report on: {}".format(end_date))
print("_"*40)

existing_serial_numbers = []

def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout

def createLogFile():
    try:
        my_output = out(cmd)
        f = open("serialnumbers.txt", "w")
        f.write(my_output)
        f.close()
    except Exception as e:
        print("Some Exception Found.")


def getSerialNumbers():
    file1 = open('serialnumbers.txt', 'r') 
    lines = file1.readlines() 
    serial_numbers = [x.replace("Serial Number:", "").strip() for x in lines if "Serial" in x]
    dates = [getTimeStamp() for x in serial_numbers]
    print([x.replace("Serial Number:", "").strip() for x in lines if "Serial" in x])
    return serial_numbers, dates

def createCSVReport():
    serialnumbers, inserted_dates = getSerialNumbers()
    csv_name = "connected_devices_{}_{}.csv".format(nuid, getTimeStamp())
    with open(csv_name, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Serial Number", "Inserted Date"])
        for idx in range(len(serialnumbers)):
            writer.writerow([serialnumbers[idx], inserted_dates[idx]])

def sendCSVReport():
    day_name = datetime.date.today().strftime("%A")
    end_day_name = "Tuesday"
    if day_name == end_day_name:
        """
            1. Create CSV
            2. Send CSV
            3. Move CSV to Backup Folder
            4. Delete serialnumbers.txt
        """
        #TODO: Send Report
        return True
    else:
        return False

def getTimeStamp():
    dateTimeObj = datetime.datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    return timestampStr

def collect_and_send_serialNumbers():
    while True:
        sendCSVReport()
        createLogFile()
        getSerialNumbers()
        count += 1
        time.sleep(3)
        if count == 3:
            createCSVReport()
            break;
count = 0

if __name__ == "__main__":  
    collect_and_send_serialNumbers()
