def generate_datalist(datalist):
    with open('waveform.txt') as f:
        for line in f:
            if not line in ['\n', '\r\n']:
                time, value = line.split(",")
                time = time.rstrip(" ")
                value = value.rstrip(" ")
                value = value.rstrip("\n")
                data = [float(time), int(value)]
                datalist.append(data)

    f.close()

    return datalist




def Generate_Generate_Binary_File(guess, signal_pause_length, one_length, zero_length, bit_length):
    name = input("Enter button name: ")
    with open(f'{name}_Binary_Data.txt', 'w') as f:
        f.write(str(f"Binary Code - {guess[0]}\n"))
        f.write(str(f"Pause length - {signal_pause_length}\n"))
        f.write(str(f"One length - {one_length}\n"))
        f.write(str(f"Zero length - {zero_length}\n"))
        f.write(str(f"Bit length - {bit_length}"))
