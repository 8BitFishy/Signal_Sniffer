def findduration(datalist, start, end, value, duration):
    #print(f"Starting duration search for {value} from {start} to {end}")
    #iterate through datalist from start point to end of list
    for i in range(start, end):
        #print(f"Searching from {i}")
        #if data value is equal to search value
        if datalist[i][1] == value:
            #print(f"Value {datalist[i][1]} equal to {value}")
            #start of block = i
            val_start = i
            #print(f"start of block of {value} at {i}")
            #print(f"Searching on from j")
            #iterate from this value onwards
            for j in range(i, end):
                #print(f"{i} - {j}")
                #if value is not equal to search value
                if datalist[j][1] != value:
                    #end of block = j
                    val_end = j
                    #print(f"End of block found at j = {j}")
                    #duration of value = time at val_end - time at val_start
                    #if number of opposite value readings is less than 2, discount as noise
                    '''if j-i < 2:
                        print(f"j-i = {j-i}, probably noise, continuing")
                        continue
                    '''
                    #if duration is above 5ms, return val_start and val_end positions
                    if datalist[j][0] - datalist[i][0] > duration:
                        #print("Duration large enough, returning")
                        return([val_start, val_end])
                    else:
                        #print(f"Breaking - duration measured at - {datalist[j][0] - datalist[i][0]}, measuring from {i} to {j}, probably noise")
                        break
                if j == end-1 and datalist[j][1] == value:
                    #print(f"Hit end, {j} == {datalist[j][1]} and {end} and {value}")
                    return None
        else:
            continue

def deleteoutlier(dataset):

    average = sum(dataset) / len(dataset)
    #print(f"Average of dataset - {average}")
    newdataset = []
    for i in range(len(dataset)):
        if abs((average - dataset[i]) / average) * 100 <= 50:
            newdataset.append(dataset[i])
        #else:
            #print(f"Outlier found - {i} - {dataset[i]}")
    return newdataset


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
    return [most_common, highest_count]