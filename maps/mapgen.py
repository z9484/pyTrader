import random

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def generatemap():
    numX = 20
    numY = 50

    #init map 
    map1 = []
    for row in xrange(numY):    
        y = []
        for elem in xrange(numX):
            y.append("_")
        map1.append(y)


    #add borders
    for i in xrange(numX):
        map1[0][i] = "#"
        map1[numY-1][i] = "#"

    for i in xrange(numY):
        map1[i][0] = "#"
        map1[i][numX-1] = "#"


    #add capital
    
    row = random.randint(5,numY-7)
    col = random.randint(5,numX-7)
    capital = Point(col, row)
    
    #[row][col]
    map1[1][0] = 'q'
    map1[capital.y][capital.x] = "d"
    map1[capital.y][capital.x+1] = "d"
    map1[capital.y+1][capital.x] = "d"
    map1[capital.y+1][capital.x+1] = "d"
    #map1[capital.y+2][capital.x+1] = "d"
 
    for row in map1:    
        print row
    return map1

def findView(x,y, map1):
    view = []
    for q in xrange(-2,3):
        row = []
        for r in xrange(-2,3):
            print y+q,x+r
            if y+q > 50 or x+r > 20 or y+q <0 or x+r <0:
                row.append("#")
            else:
                row.append(map1[y+q][x+r])
        view.append(row)  


    for row in view:    
        print row

    return view        


if __name__ == "__main__":
    map1 = generatemap()
    
    #findView(1,1, map1)

