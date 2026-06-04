class Credito:
    def __init__(self, monto, tasa):
        self.monto = monto
        self.tasa = tasa
    def __str__(self):
        return f"Credito(monto): ${self.monto}, tasa: {self.tasa*100}%"

class Cliente:
    def __init__(self, nombre, ingresos):
        self.nombre = nombre
        self.__ingresos = ingresos
        self.creditos = []
    def asignar_credito(self, credito):
        self.creditos.append(credito)
    
CL01 = Cliente("Ana Lopez", 2000)
CR01 = Credito(1000,0.10)
CL01.asignar_credito(CR01)
print(CL01.creditos[0])