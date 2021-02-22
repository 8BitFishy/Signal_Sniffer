def generate_datalist(datalist):
    with open('waveform.csv') as f:
        for line in f:
            if not line in ['\n', '\r\n']:
                time, value = line.split(",")
                time = time.rstrip(" ")
                value = value.rstrip(" ")
                value = value.rstrip("\n")
                data = [float(time), int(value)]
                datalist.append(data)
    return datalist

'''
with open('waveform.csv', 'w') as f:
    for i in range(len(datalist)):
        f.write(str(f"{datalist[i][0]}, {datalist[i][1]}\n"))
f.close()
'''


def Generate_Generate_Binary_File(guess, signal_pause_length, one_length, zero_length, bit_length):
    with open('Binary_Data.txt', 'w') as f:
        f.write(str(f"{guess[0]}\n"))
        f.write(str(f"{signal_pause_length}\n"))
        f.write(str(f"{one_length}\n"))
        f.write(str(f"{zero_length}\n"))
        f.write(str(f"{bit_length}\n"))
