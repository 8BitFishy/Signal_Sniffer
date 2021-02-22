import time
import sys
import RPi.GPIO as GPIO


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

def Load_Codes(code):
    binary_code = []
    #code = input("Enter Code: ")
    code = str(code)
    filename = f"Binary_Data.txt"
    with open(f"Plugs-White/{code}_{filename}") as f:
        for i in range(5):
            line = next(f).strip()
            data, value = line.rsplit(" - ")
            if i == 0:
                binary_code.append(int(value))
            else:
                binary_code.append(float(value))

    print(binary_code)

    return binary_code

NUM_ATTEMPTS = 20
TRANSMIT_PIN = 24

def transmit_code(binary_code):
    #Transmit a chosen code string using the GPIO transmitter
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    code = str(binary_code[0])
    for t in range(NUM_ATTEMPTS):
        for i in code:
            if i == '1':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(binary_code[2])
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(binary_code[4] - binary_code[2])
            elif i == '0':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(binary_code[3])
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(binary_code[3] - binary_code[2])
            else:
                continue
        GPIO.output(TRANSMIT_PIN, 0)
        time.sleep(binary_code[1])
    GPIO.cleanup()

if __name__ == '__main__':
    #Play_Direct("waveform.txt")
    for i in range(1, 6):
        for j in range(2):
            if j == 0:
                command = 'On'
            else:
                command = 'Off'
     
            print(f"{i}_{command}")
            transmit_code(Load_Codes(f"{str(i)}_{command}"))
    '''
    for argument in sys.argv[1:]:
        exec('transmit_code(' + str(argument) + ')')
'''