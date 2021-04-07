# ************************************************
#   Point.py
#   Define a classe Ponto
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************


class Point:   
    def __init__(self, x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z
        #print ("Objeto criado")
    
    def imprime(self):
        print (self.x, self.y, self.z)
    
    def set(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def multiplica(self, x, y, z):
        self.x *= x
        self.y *= y
        self.z *= z
    
    def isEqual(self, a):
        if self.x == a.x and self.y == a.y:
            return True
        else:
            return False

#P = Point()
#P.set(1,2)
#P.imprime()
#P.set(23,34,56)
#P.imprime()

