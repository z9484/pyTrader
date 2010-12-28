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

    def bleft(self):
        return self.capacity - self.current
    
    
class Outpost(object):
    def __init__(self, no, point, otype, food, mineral, equipment):
        self.no = no
        self.coordinates = point
        self.type = otype 
        self.food = food
        self.mineral = mineral
        self.equipment = equipment
        
    def dailyAdj(self):
        if self.type == "Farm":
            self.calc(self.food, 0.2)
            self.calc(self.mineral, -0.05)
            self.calc(self.equipment, -0.1)
        elif self.type == "Mine":
            self.calc(self.food, -0.1)
            self.calc(self.mineral, 0.2)
            self.calc(self.equipment, -0.1)
        elif self.type == "Factory":
            self.calc(self.food, -0.1)
            self.calc(self.mineral, -0.2)
            self.calc(self.equipment, 0.2)
        elif self.type == "City":
            self.calc(self.food, -0.125)
            self.calc(self.mineral, -0.125)
            self.calc(self.equipment, -0.125)
            
    def calc(self, label, multiplier):
        amt = int(label.current + label.capacity * multiplier)
        if amt < 0:
            label.current = 0
        elif amt > label.capacity:
            label.current = label.capacity
        else:
            label.current = amt

    def isValid(self, label, amt):
        exec("commodity = self." + label)
        if commodity.current + amt <= commodity.capacity or  commodity.current + amt >= 0:
            return True
        else:
            return False
            
    def buy(self, label, amt):
        exec("commodity = self." + label)
        commodity.current += amt
        if commodity.current < 0:
            commodity.current = 0
        elif commodity.current > commodity.capacity:
            commodity.current = commodity.capacity
    
            
    # def calc(self, label, multiplier):
        # exec("amt = int(" + label + ".current + " + label + ".capacity * multiplier)")
        # if amt < 0:
            # exec(label + ".current = 0")
        # elif amt > eval(label + ".capacity"):
            # exec(label + ".current = " + label + ".capacity")
        # else:
            # exec(label + ".current = amt")

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
    
