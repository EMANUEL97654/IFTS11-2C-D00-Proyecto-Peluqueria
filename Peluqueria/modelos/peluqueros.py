import uuid


class Peluquero(object):
    def __init__(self,nombre,especialidad="General"):
        self.id = str(uuid.uuid4())[0:4]
        self.nombre = nombre
        self.especialidad = especialidad
    
    def __str__(self):
        return f"{self.nombre} - {self.especialidad}"
    

