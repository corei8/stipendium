class Idify:
    def make_id(self, city, state):
        vowels = (a,e,y,o,u,)
        id = '' # 8 chars max
        i = 0
        while i != 5:
            for y in self.city:
                if y not in vowels:
                    id += y
                    i += 1
        while i != 8:
            for x in self.state:
                if x not in vowels:
                    id += x
                    i += 1
        return id.upper()
