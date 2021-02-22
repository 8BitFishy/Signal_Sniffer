import Data_Analyst

def binary_translator(datalist, start, end):
    binary_signal = ''
    binary_data = []
    av_one_length_list = []
    av_zero_length_list = []
    bit_length_start = []
    bit_lengths = []
    search_start = start

    #Run until broken
    while True:
        #Find range of ones (in this bit)
        onerange = Data_Analyst.findduration(datalist, search_start, end+1, 1, 0.00001)

        #if onerange has data
        if onerange != None:
            #add starting index of bit to bit_start_list
            bit_length_start.append(datalist[onerange[0]][0])
            #start of the next search is the end of the current one
            search_start = onerange[1]
        #otherwise break, as no data indicates end of datablock
        else:
            break

    #iterate through bit_length_start list and add the lengths of each bit to the bit_length variable
    for i in range(len(bit_length_start)-1):
        bit_lengths.append(bit_length_start[i+1] - bit_length_start[i])
    av_bit_length = sum(bit_lengths) / len(bit_lengths)



    #run until broken
    while True:

        #find range of 1's
        onerange = Data_Analyst.findduration(datalist, start, end+1, 1, 0.00001)

        #if onerange has data
        if onerange != None:
            #print(f"One range - {onerange} - {datalist[onerange[1]][0]} - {datalist[onerange[0]][0]}")
            #if length of 1 value is less than time, is 1
            # #todo make 0 or 1 calc programmatic
            if datalist[onerange[1]][0] - datalist[onerange[0]][0] < 0.0003:
                binary_signal = binary_signal + str(1)
                av_one_length_list.append(datalist[onerange[1]][0] - datalist[onerange[0]][0])
            #otherwise is 0
            else:
                binary_signal = binary_signal + str(0)
                av_zero_length_list.append(datalist[onerange[1]][0] - datalist[onerange[0]][0])

            start = onerange[1]
        else:
            break

    #if length of zero length list is not 0, data is present
    if len(av_zero_length_list) != 0:

        av_one_length = sum(av_one_length_list) / len(av_one_length_list)
        av_zero_length = sum(av_zero_length_list) / len(av_zero_length_list)

        #print(f"Av bit length - {av_bit_length}")


        #print(f"Binary translation - {binary_signal}")
        binary_data.append(binary_signal)
        binary_data.append(av_one_length)
        binary_data.append(av_zero_length)
        binary_data.append(av_bit_length)
        #print(f"Binary data - {binary_data}")
        #print(f"Av one length - {av_one_length}")
        #print(f"Av zero length - {av_zero_length}")

        return binary_data

    else:
       return