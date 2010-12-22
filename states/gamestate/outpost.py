class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Commodity(object):
    def __init__(self, name, bp, bpmult, capacity, current, growth):
        self.name = name
        self.baseprice = bp
        self.bpmult = bpmult
        self.capacity = capacity
        self.current = current
        self.growth = growth
##        self.capMult = 1.5
        
    def getBuyPrice(self):
        return int(round(self.baseprice * self.bpmult * 1 * 1.5))

    def getSellPrice(self):
        return int(round(self.baseprice * self.bpmult * 1 * 1.5))

    def dailyAdj(self):
        pass
    
class Outpost(object):
    def __init__(self, point, otype, food, mineral, equipment):    
        self.coordinates = point
        self.type = otype 
        self.food = food
        self.mineral = mineral
        self.equipment = equipment
        
                
if __name__ == "__main__":
    tt = Outpost(Point(24,9), "Mine",
                 Commodity("Food", 10, 1.05, 2600, 1300, 0.1),
                 Commodity("Minerals", 20, 0.9, 7000, 3500, 0.1),
                 Commodity("Equipment", 30, 1.15, 3500, 1750, 0.1)
                 )
    
    print tt.food.getBuyPrice()
    
##    print tt.coordinates
##    cc.run()
    
