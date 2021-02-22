from datetime import datetime
import Signal_Interpreter
import RPi.GPIO as GPIO
import matplotlib.pyplot as pyplot


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
 
    print("Writing files...")
    with open('waveform.txt', 'w') as f:
        for i in range(len(RECEIVED_SIGNAL[0])):
            f.write(str(f"{RECEIVED_SIGNAL[0][i]}, {RECEIVED_SIGNAL[1][i]}\n"))
    f.close()
    print("File Saved...")
    
    #convert received signal to dataset
    datalist = []
    for i in range(len(RECEIVED_SIGNAL[0])):
        data = [RECEIVED_SIGNAL[0][i], RECEIVED_SIGNAL[1][i]]
        datalist.append(data)

    #Interpret Signal
    print("Interpreting data...")
    Signal_Interpreter.Signal_Interpreter(datalist)



    print("Plotting...")
    pyplot.plot(RECEIVED_SIGNAL[0], RECEIVED_SIGNAL[1])
    pyplot.axis([4, 5, -1, 2])
    pyplot.show()
    print("Complete")