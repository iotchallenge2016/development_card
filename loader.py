def parse_csv(csvURL):
    # The row number in the .csv file
    avlb = 2
    zone = 0

    values = [] # Array that holds the availabity of the spaces in each zone
    total = 0 # Holds the total number of occupied spaces in a zone
    diff = "" # Variable used to know when the zone changes while reading the .csv
    json = "["
    # Reads each line the .csv and stores the value of the occupied spaces
    with open(csvURL, 'r') as csv:
        for line in csv.readlines():
            elements = line.strip().split(',')
            if diff == "":
                diff = (elements[zone])
            # Calculates the occupied spaces, their average, and the number of free spaces once a change of zone occurs
            elif diff != elements[zone]:
                ocpd = sum(values)
                free = total - ocpd
                json = json + toJSON(diff,free, total)
                values = []
                total = 0
                diff = elements[zone]
            values.append(int(elements[avlb]))
            total += 1
            
    # Calculates the occupied and free spaces in the last zone
    ocpd = sum(values)
    free = total - ocpd
    return json + toJSONfinal(diff,free, total) + "]"

def toJSON(zone,available,total):
    return "{\"section\":\""+zone+"\", \"capacity\":"+str(available)+",\"max\":"+str(total)+"},"

def toJSONfinal(zone,available,total):
    return "{\"section\":\""+zone+"\", \"capacity\":"+str(available)+",\"max\":"+str(total)+"}"
