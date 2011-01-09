class Timer(object):
    def __init__(self, icool):
        self.icool = icool
        self.cool = self.icool
        
    def check(self, dt):
        self.cool -= dt
        if self.cool <= 0:
            self.cool = self.icool
            return True
        return False
        
