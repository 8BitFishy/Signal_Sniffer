from datetime import datetime
import RPi.GPIO as GPIO
import matplotlib.pyplot as pyplot

def findduration(datalist, start, end, value, duration):
    highest_duration = 0.0
    #iterate through datalist from start point to end of list
    for i in range(start, end):

        #if data value is equal to search value
        if datalist[i][1] == value:
            #start = i
            val_start = i

            #iterate from this value onwards
            for j in range(i, end):

                #if value is not equal to search value
                if datalist[j][1] != value:
                    #end of val = j
                    val_end = j
                    #duration of value = time at val_end - time at val_start
                    #if duration is above 5ms, return val_start and val_end positions
                    if datalist[j][0] - datalist[i][0] > duration:
                        return([val_start, val_end])
                    else:
                        break
        else:
            continue


def binary_translator(datalist, start, end):
    binary_signal = ''
    while True:
        onerange = findduration(datalist, start, end+1, 1, 0.00001)
        if onerange != None:
            if datalist[onerange[1]][0] - datalist[onerange[0]][0] < 0.0003:
                binary_signal = binary_signal + str(1)
            else:
                binary_signal = binary_signal + str(0)
            start = onerange[1]
        else:
            break

    print(binary_signal)
    return binary_signal


def receive_signal():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RECEIVE_PIN, GPIO.IN)
    cumulative_time = 0
    beginning_time = datetime.now()
    
    readout1 = readout2 = readout3 = readout4 = readout5 = readout6 = 0
    print("Recording started...")
    
    while cumulative_time < MAX_DURATION:
        
        if cumulative_time == 1 and readout1 == 0:
            print("3")
            readout1 = 1
        if cumulative_time == 2 and readout2 == 0:
            print("2")
            readout2 = 1
        if cumulative_time == 3 and readout3 == 0:
            print("1")
            readout3 = 1

        if cumulative_time >= 4 and cumulative_time <= 5:
                
            RECEIVED_SIGNAL[0].append(time_delta)
            current = GPIO.input(RECEIVE_PIN)
            RECEIVED_SIGNAL[1].append(current)
            
            if cumulative_time == 4 and readout4 == 0:
                print("Press")
                readout4 = 1

            if cumulative_time == 5 and readout6 == 0:
                print("Release")
                readout6 = 1

            
        time_delta = datetime.now() - beginning_time
        cumulative_time = time_delta.seconds


    print("Recording complete...")
    GPIO.cleanup()

    print(f"{len(RECEIVED_SIGNAL[0])} samples recorded")
    
    print("Processing...")
    for i in range(len(RECEIVED_SIGNAL[0])):
        RECEIVED_SIGNAL[0][i] = RECEIVED_SIGNAL[0][i].seconds + RECEIVED_SIGNAL[0][i].microseconds/1000000.0
        
    return RECEIVED_SIGNAL


RECEIVED_SIGNAL = [[], []]  #[[time of reading], [signal reading]]
MAX_DURATION = 6
RECEIVE_PIN = 23

if __name__ == '__main__':

    #receive signal and process
    RECEIVED_SIGNAL = receive_signal()
 
    #convert received signal to dataset
    datalist = []
    for i in range(len(RECEIVED_SIGNAL[0])):
        data = [RECEIVED_SIGNAL[0][i], RECEIVED_SIGNAL[1][i]]
        datalist.append(data)
        
    print(f"Data length - {len(RECEIVED_SIGNAL[0])}")
    
    #find end of zero block
    zeropause = []
    zeropause = findduration(datalist, 0, len(datalist), 0, 0.005)
    print(zeropause)
    #if datablock found
    if zeropause != None:
        #identify start of datablock (i.e. end of zero block)
        blockstart = zeropause[1]
        #find end of datablock
        zeropause = findduration(datalist, blockstart, len(datalist), 0, 0.005)
        blockend = zeropause[0]
        print(f"Block start at {blockstart}, block end at {blockend}")
        #translate datablock into binary
        binary_signal = binary_translator(datalist, blockstart, blockend)
        
        with open('Binary_Code.txt', 'a') as f:
            f.write(binary_signal)
            f.write("/n")
        f.close()
        
    
    print("Writing files...")

    with open('waveform.csv', 'w') as f:
        for i in range(len(RECEIVED_SIGNAL[0])):
            f.write(str(f"{RECEIVED_SIGNAL[0][i]}, {RECEIVED_SIGNAL[1][i]}\n"))
        
    f.close()
    
 
    
    print("File Saved...")
    print("Plotting...")
    pyplot.plot(RECEIVED_SIGNAL[0], RECEIVED_SIGNAL[1])
    pyplot.axis([4, 5, -1, 2])
    pyplot.show()
    print("Complete")
    