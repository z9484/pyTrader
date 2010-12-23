import re

class Console(object):
    #def __init__(self):
        #pass

    def viewBalance(self):
         print "Balance:", str(self.balance).rjust(5)
         print "Food:", str(self.food).rjust(8)
         print "Minerals:", str(self.minerals).rjust(4)
         print "Eqipment:", str(self.equipment).rjust(4)
         print "Cargo:", (str(self.findcargo())+"/"+str(self.maxcargo)).rjust(7)

    def buy(self, commodity):
        tt = raw_input("How much {0}?".format(commodity)).strip()
        try:
            amt = int(tt)
            if (self.balance - (amt * 5) < 0) or (self.findcargo() + amt > self.maxcargo):
                raise BalanceError
            self.balance -= (amt * 5)
            exec("self." + commodity + " += amt")
            self.viewBalance()
        except:
            print "Invalid amount"
    

    def execute(self, cmd):
        print cmd
        if cmd == "b" or cmd == "B":
            print "GG"

    def run(self):
        while (True):
            raw = raw_input(">").strip()
            
            shouldQuit = re.search(r"q|quit|exit", raw, re.I)
            if shouldQuit:
                break

            if raw == "b" or raw == "B":
                choice = raw_input("What would you like to buy?").strip()
                if choice == "f" or choice == "F":
                    self.buy("food")                  
                elif choice == "m" or choice == "M":
                    self.buy("minerals")
                elif choice == "e" or choice == "E":
                    self.buy("equipment")
                elif choice == "d" or choice == "D":
                    break
                else:
                    print "Invalid amount"

            elif raw == "v" or raw == "v":
                self.viewBalance()
                
if __name__ == "__main__":
    cc = cheese()
    cc.run()
    
