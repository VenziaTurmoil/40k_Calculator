options_list = ['1 Hits RR', 'Hits RR', 
                     '1 Wounds RR', 'Wounds RR']
# Lethal hits, Dev wounds...

class Weapon:

    def __init__(self,A, Sk, S, AP, D, options):
        if Sk > 7 or Sk < 1 or A < 0 or S < 0 or AP < 0 or AP > 6 or D < 0:
            raise ValueError('Please check Weapon Stats')
        self.A = A
        self.Sk = Sk
        self.S = S
        self.AP = AP
        self.D = D
        self.options = options

    def attacks(self, target):
        return self.A

    def hit(self, target):
        p = (7-self.Sk)/6
        if 'Hits RR' in self.options:
            return 2*p - p**2
        elif '1 Hits RR' in self.options:
            return 7*p/6
        else:
            return p

    def wound(self, target):
        if 2*self.S <= target.T:
            p = 1/6
        elif self.S < target.T:
            p = 2/6
        elif self.S == target.T:
            p = 3/6
        elif self.S >= 2*target.T:
            p = 5/6
        else:
            p = 4/6
            
        if 'Wounds RR' in self.options:
            return 2*p - p**2
        elif '1 Wounds RR' in self.options:
            return 7*p/6
        else:
            return p

    def pierce(self, target):
        return min((target.Sv + self.AP -1)/6, 1)

    def damage(self, target):
        return min(self.D, target.W)

    def sequence(self, target):
        return (self.attacks(target)
            * self.hit(target)
            * self.wound(target)
            * self.pierce(target)
            * self.damage(target))
