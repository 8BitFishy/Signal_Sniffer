import time
import sys
#import RPi.GPIO as GPIO


def Play_Direct(filename):
    print("Start")
    binary_code = []
    data = []
    row_count = len(open(filename).readlines())
    #with open(filename) as f:
        #row_count = sum(1 for row in f)  # fileObject is your csv.reader
    #print(row_count)
    with open(filename) as f:
        for i in range(row_count):
            line = next(f).strip()
            datastring = line.rsplit(", ")
            #data.append([float(datastring[0]), int(datastring[1])])

    print("done")
    return

def Load_Codes(filename):
    binary_code = []
    with open(filename) as f:
        for i in range(4):
            line = next(f).strip()
            if i == 0:
                binary_code.append(int(line))
            else:
                binary_code.append(float(line))

    print(binary_code)

    return binary_code

NUM_ATTEMPTS = 10
TRANSMIT_PIN = 24
'''
def transmit_code(binary_code):
    #Transmit a chosen code string using the GPIO transmitter
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    for t in range(NUM_ATTEMPTS):
        for i in code:
            if i == '1':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(short_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(long_delay)
            elif i == '0':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(long_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(short_delay)
            else:
                continue
        GPIO.output(TRANSMIT_PIN, 0)
        time.sleep(extended_delay)
    GPIO.cleanup()
'''
if __name__ == '__main__':
    Play_Direct("waveform.txt")
    #Load_Codes('Binary_Data.txt')
    '''
    for argument in sys.argv[1:]:
        exec('transmit_code(' + str(argument) + ')')
'''