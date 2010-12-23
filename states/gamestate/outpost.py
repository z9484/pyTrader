class Commodity(object):
    def __init__(self, name, bpmult, capacity, current, cust):
        self.name = name
        
        if name == "Food":
            self.baseprice = 10
        if name == "Mineral":
            self.baseprice = 20
        if name == "Equipment":
            self.baseprice = 30
            
        self.bpmult = bpmult
        self.capacity = capacity
        self.current = current
        self.custmult = cust
        
    def getBuyPrice(self):
        return int(round(self.baseprice * self.bpmult * self.custmult * (2 - (float(self.current) / self.capacity)) * 0.9))
        

    def getSellPrice(self):
        return int(round(self.baseprice * self.bpmult * self.custmult * (2 - (float(self.current) / self.capacity)) * 1.1))


    
class Outpost(object):
    def __init__(self, point, otype, food, mineral, equipment):    
        self.coordinates = point
        self.type = otype 
        self.food = food
        self.mineral = mineral
        self.equipment = equipment
        
    def dailyAdj(self):
        if self.type == "Farm":
            self.calcfood(0.2)
            self.calcmineral(-0.05)
            self.calcequip(-0.1)
        elif self.type == "Mine":
            self.calcfood(-0.1)
            self.calcmineral(0.2)
            self.calcequip(-0.1)
        elif self.type == "Factory":
            self.calcfood(-0.1)
            self.calcmineral(-0.2)
            self.calcequip(0.2)
        elif self.type == "City":
            self.calcfood(-0.125)
            self.calcmineral(-0.125)
            self.calcequip(-0.125)
            
    def calcfood(self, multiplier):
        amt = int(self.food.current + self.food.capacity * multiplier)
        if amt < 0:
            self.food.current = 0
        elif amt > self.food.capacity:
            self.food.current = self.food.capacity
        else:
            self.food.current = amt
        
    def calcmineral(self, multiplier):
        amt = int(self.mineral.current + self.mineral.capacity * multiplier)
        if amt < 0:
            self.mineral.current = 0
        elif amt > self.mineral.capacity:
            self.mineral.current = self.mineral.capacity
        else:
            self.mineral.current = amt
    
    def calcequip(self, multiplier):
        amt = int(self.equipment.current + self.equipment.capacity * multiplier)
        if amt < 0:
            self.equipment.current = 0
        elif amt > self.equipment.capacity:
            self.equipment.current = self.equipment.capacity
        else:
            self.equipment.current = amt
        
        
if __name__ == "__main__":
    tt = Outpost(Point(24,9), "Mine",
                 Commodity("Food", 1.05, 2600, 1300, 1),
                 Commodity("Mineral", 0.9, 7000, 3500, 1),
                 Commodity("Equipment", 1.15, 3500, 1750, 1)
                 )
                 
    print tt.mineral.getBuyPrice()
    print tt.mineral.getSellPrice()
    tt.dailyAdj()
    print tt.food.current,  tt.mineral.current,  tt.equipment.current
    print tt.mineral.getBuyPrice()
    print tt.mineral.getSellPrice()


##    print tt.coordinates
##    cc.run()
    
