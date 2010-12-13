def loadMap(map):
    x = []
    try:
        f = open(map)
        for line in f:
            line = line.strip()
            y = []
            for char in line.split(','):
                y.append(char)
            x.append(y)

    except:
      print "File does not exist or is corrupt"

    return x

if __name__ == "__main__":
    d = loadMap("maps/t1.map")
    #i = 0
    #for row in d:
    #    print i, row
    #    i += 1
