import File_Handler
import Data_Analyst
import Binary_Translator



def Signal_Interpreter(datalist):
    print("Starting Translation")
    print(f"Data length - {len(datalist)}")
    start = 0
    end = len(datalist)
    binary_codes = []
    pauses = []
    ones = []
    zeroes = []
    bits = []

    while True:
        zeroblock = []
        #find start of datablock (i.e. end of block of zeroes that lasts longer than 0.005s)
        zeroblock = Data_Analyst.findduration(datalist, start, end, 0, 0.005)
        #end of this zero block represents the start of block of ones
        oneblockstart = zeroblock[1]
        #find end of datablock (i.e. start of next block of zeroes)
        nextzeroblock = Data_Analyst.findduration(datalist, oneblockstart, len(datalist), 0, 0.005)
        #if no data returns, end of sample has been reached
        if nextzeroblock == None:
            break

        else:
            oneblockend = nextzeroblock[0]
            #convert block into binary
            if oneblockend - oneblockstart > 20:
                binary_data = Binary_Translator.binary_translator(datalist, oneblockstart, oneblockend)
                if binary_data != None:
                    binary_codes.append(binary_data[0])
                    pauses.append(datalist[zeroblock[1]][0] - datalist[zeroblock[0]][0])
                    ones.append(binary_data[1])
                    zeroes.append(binary_data[2])
                    bits.append(binary_data[3])

            #else:
                #print(f"Probably noise at {oneblockstart} - {oneblockend}")

        start = oneblockend

    print(f"{len(binary_codes)} binary translations found:\n{binary_codes}")
    
    if len(binary_codes)==0:
        return
    
    pauses = Data_Analyst.deleteoutlier((pauses))
    guess = Data_Analyst.findmostcommon(binary_codes)

    for i in range(len(binary_codes)-1, -1, -1):
        if binary_codes[i] != guess[0]:
            del binary_codes[i]
            del ones[i]
            del zeroes[i]
            del bits[i]

    signal_pause_length = sum(pauses)/len(pauses)
    one_length = sum(ones)/len(ones)
    zero_length = sum(zeroes)/len(zeroes)
    bit_length = sum(bits)/len(bits)
    print(f"\n\nBest Guess at binary data with {guess[1]} repeats:\n{guess[0]}")
    print(f"Signal pause length:\n{signal_pause_length}")
    print(f"One length:\n{one_length}")
    print(f"Zero length:\n{zero_length}")
    print(f"Bit length:\n{bit_length}")

    File_Handler.Generate_Generate_Binary_File(guess, signal_pause_length, one_length, zero_length, bit_length)

if __name__ == "__main__":
    datalist = []
    # generate datalist
    datalist = File_Handler.generate_datalist(datalist)

    Signal_Interpreter(datalist)


    #todo generate code timings based on best guess code