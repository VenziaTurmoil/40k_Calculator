from utils import r

class Weapon:

    def __init__(self,A, Sk, S, AP, D):
        if Sk > 7 or Sk < 1 or A < 0 or S < 0 or AP < 0 or AP > 6 or D < 0:
            raise ValueError('Please check Weapon Stats')
        self.A = A
        self.Sk = Sk
        self.S = S
        self.AP = AP
        self.D = D

    def attacks(self, target):
        return self.A

    def hit(self, target):
        return (7-self.Sk)/6

    def wound(self, target):
        if 2*self.S <= target.T:
            return 1/6
        if self.S < target.T:
            return 2/6
        if self.S == target.T:
            return 3/6
        if self.S >= 2*target.T:
            return 5/6
        else:
            return 4/6

    def pierce(self, target):
        return min((target.Sv - self.AP - 1)/6, 1)

    def damage(self, target):
        return min(self.D, target.W)

    def sequence(self, target):
        return (self.attacks(target)
            * self.hit(target)
            * self.wound(target)
            * self.pierce(target)
            * self.damage(target))
