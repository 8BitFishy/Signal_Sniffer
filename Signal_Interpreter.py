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
        #print("Starting search")
        zeroblock = []
        #find start of datablock (i.e. end of block of zeroes)
        zeroblock = Data_Analyst.findduration(datalist, start, end, 0, 0.005)
        #print(f"Pause found - {zeroblock}")
        #print(f"Pause duration {datalist[zeroblock[1]][0] - datalist[zeroblock[0]][0]}")
        oneblockstart = zeroblock[1]
        #find end of datablock (i.e. start of next block of zeroes)
        #print("Starting nextzeroblock")
        nextzeroblock = Data_Analyst.findduration(datalist, oneblockstart, len(datalist), 0, 0.005)
        #print(f"Next Pause found at {nextzeroblock}")
        if nextzeroblock == None:
            #print("Next pause returns none")
            break

        else:
            oneblockend = nextzeroblock[0]
            #convert block into binary
            if oneblockend - oneblockstart > 20:
                #print(f"Data block = [{oneblockstart}, {oneblockend}]")
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
    #print("\nRemoving ones outliers")
    '''
    ones = Data_Analyst.deleteoutlier(ones)
    #print("Removing zeroes outliers")
    zeroes = Data_Analyst.deleteoutlier(zeroes)
    bits = Data_Analyst.deleteoutlier(bits)
    '''
    #print("Removing pauses outliers")
    del pauses[0]
    del pauses[-1]
    pauses = Data_Analyst.deleteoutlier((pauses))

    guess = Data_Analyst.findmostcommon(binary_codes)
    print(f"Binary data = {binary_data}")
    for i in range(len(binary_data)-1, -1, -1):
        if binary_data[0] != guess:
            del binary_data[i]
    print(f"New binary data = {binary_data}")

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