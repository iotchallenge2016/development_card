def loadCSV(csvURL,target):
    # The row number in the .csv file
    avlb = 2
    zone = 0

    values = [] # Array that holds the availabity of the spaces in each zone
    total = 0 # Holds the total number of occupied spaces in a zone
    diff = 1 # Variable used to know when the zone changes while reading the .csv

    # Reads each line the .csv and stores the value of the occupied spaces
    with open(csvURL, 'r') as csv:
        for line in csv.readlines():
            elements = line.strip().split(',')
            # Calculates the occupied spaces, their average, and the number of free spaces once a change of zone occurs
            if diff != int(elements[zone]):
                ocpd = sum(values)
                free = total - ocpd
                print("Occupied spaces on zone %d: %d" % (diff, ocpd))
                print("Free spaces on zone %d: %d" % (diff, free))
                toJSON(diff,free,target)
                print()
                values = []
                total = 0
                diff = int(elements[zone])
            values.append(int(elements[avlb]))
            total += 1
            
    # Calculates the occupied and free spaces in the last zone
    ocpd = sum(values)
    free = total - ocpd
    print("Occupied spaces on zone %d: %d" % (diff, ocpd))
    print("Free spaces on zone %d: %d" % (diff, free))
    toJSONfinal(diff,free,target)

def toJSON(zone,available,target):
    target.write("{\"zone\":"+str(zone)+", \"availabe\":"+str(available)+"},\n")
def toJSONfinal(zone,available,target):
    target.write("{\"zone\":"+str(zone)+", \"availabe\":"+str(available)+"}\n")

current = open('current.json','w')
current.write("{\"parking\": [\n")
loadCSV('Estacionamiento.csv',current)
current.write("]}")
