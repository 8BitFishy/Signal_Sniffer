def findduration(datalist, start, end, value, duration):

    #iterate through datalist from start point to end of list
    for i in range(start, end):
        print(i)
        #if data value is equal to search value
        if datalist[i][1] == value:

            #start of block = i
            val_start = i

            #iterate from this value onwards
            for j in range(i, end):

                #if value is not equal to search value
                if datalist[j][1] != value:

                    #end of block = j
                    val_end = j

                    #duration of value = time at val_end - time at val_start

                    '''               
                    #if number of opposite value readings is less than 2, discount as noise
                    if j-i < 2:
                        continue'''

                    #if duration is above 5ms, return val_start and val_end positions
                    if datalist[j][0] - datalist[i][0] > duration:
                        return([val_start, val_end])
                    else:
                        print(f"Breaking - duration measured at - {datalist[j][0] - datalist[i][0]}, measuring from {i} to {j}")
                        break

                if j == end and
        else:
            continue

def deleteoutlier(dataset):

    average = sum(dataset) / len(dataset)
    print(f"Average of dataset - {average}")
    newdataset = []
    for i in range(len(dataset)):
        if abs((average - dataset[i]) / average) * 100 <= 50:
            newdataset.append(dataset[i])
        else:
            print(f"Outlier found - {i} - {dataset[i]}")
    return newdataset

def binary_translator(datalist, start, end):
    binary_signal = ''
    binary_data = []
    av_one_length_list = []
    av_zero_length_list = []
    while True:
        onerange = findduration(datalist, start, end+1, 1, 0.00001)
        if onerange != None:
            if datalist[onerange[1]][0] - datalist[onerange[0]][0] < 0.0003:
                binary_signal = binary_signal + str(1)
                av_one_length_list.append(datalist[onerange[1]][0] - datalist[onerange[0]][0])

            else:
                binary_signal = binary_signal + str(0)
                av_zero_length_list.append(datalist[onerange[1]][0] - datalist[onerange[0]][0])

            start = onerange[1]
        else:
            break
    if len(av_zero_length_list) != 0:
        av_one_length = sum(av_one_length_list) / len(av_one_length_list)
        av_zero_length = sum(av_zero_length_list) / len(av_zero_length_list)
        print(f"Binary translation - {binary_signal}")
        binary_data.append(binary_signal)
        binary_data.append(av_one_length)
        binary_data.append(av_zero_length)
        print(f"Binary data - {binary_data}")
        print(f"Av one length - {av_one_length}")
        print(f"Av zero length - {av_zero_length}")

        return binary_data

    else:
       return

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

def findmostcommon(binary_codes):
    highest_count = 0
    most_common = ''

    #iterate through list
    for i in range(len(binary_codes)):
        if binary_codes[i] != None:
            #reset count
            count = 0
            #iterate through list
            for j in range(i, len(binary_codes)):
                if binary_codes[i] == binary_codes[j]:
                    count += 1
                    if count > highest_count:
                        highest_count = count
                        most_common = binary_codes[i]
                else:
                    continue



    return most_common

if __name__ == "__main__":

    datalist = []
    # generate datalist
    datalist = generate_datalist(datalist)
    print(f"Data length - {len(datalist)}")
    start = 0
    end = len(datalist)
    binary_codes = []
    pauses = []
    ones = []
    zeroes = []

    while True:

        zeroblock = []
        #find start of datablock (i.e. end of block of zeroes)
        zeroblock = findduration(datalist, start, end, 0, 0.005)
        print(f"Pause = {zeroblock}")
        print(f"Pause duration {datalist[zeroblock[1]][0] - datalist[zeroblock[0]][0]}")
        oneblockstart = zeroblock[1]
        #find end of datablock (i.e. start of next block of zeroes)
        print("Starting nextzeroblock")
        nextzeroblock = findduration(datalist, oneblockstart, len(datalist), 0, 0.005)
        print(f"Next Pause found at {nextzeroblock}")
        if nextzeroblock == None:
            print("Next pause returns none")
            break

        else:
            oneblockend = nextzeroblock[0]
            #convert block into binary
            if oneblockend - oneblockstart > 20:
                print(f"Data block = [{oneblockstart}, {oneblockend}]")
                binary_data = binary_translator(datalist, oneblockstart, oneblockend)
                if binary_data != None:
                    binary_codes.append(binary_data[0])
                    pauses.append(datalist[zeroblock[1]][0] - datalist[zeroblock[0]][0])
                    ones.append(binary_data[1])
                    zeroes.append(binary_data[2])

            else:
                print(f"Probably noise at {oneblockstart} - {oneblockend}")

        start = oneblockend

    print("\nRemoving ones outliers")
    ones = deleteoutlier(ones)
    print("Removing zeroes outliers")
    zeroes = deleteoutlier(zeroes)
    print("Removing pauses outliers")
    del pauses[0]
    del pauses[-1]
    pauses = deleteoutlier((pauses))
    print(f"\n\nBest Guess at binary data - {findmostcommon(binary_codes)}")
    print(f"Signal pause length = {sum(pauses)/len(pauses)}")
    print(f"One length = {sum(ones)/len(ones)}")
    print(f"Zeroes length = {sum(zeroes)/len(zeroes)}")

