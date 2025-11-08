from datetime import datetime, timedelta
import uuid


class Cliente(object):
    def __init__(self,nombre,telefono,email=""):
        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def __str__(self):
        return f"{self.nombre}-{self.telefono}-{self.email}"
    
#casos de ejemplo
""" cliente = Cliente("Juan", "1234567890", "juan@gmail.com")
print(cliente) """

class Turno(object):
    def __init__(self,cliente,fecha_hora,duracion_minutos,servicio):
        self.id = str(uuid.uuid4())
        self.cliente = cliente
        
        #convierte la fecha y hora en string en caso de necesitarlo
        if isinstance(fecha_hora,str):
            self.fecha_hora = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")
        else:
            self.fecha_hora = fecha_hora
            
        self.duracion_minutos = duracion_minutos
        self.servicio = servicio
        self.fecha_finalizacion = self.fecha_hora + timedelta(minutes=duracion_minutos)
        #uso timedelta para representar la diferencia entre dos fechas
        

    def __str__(self):
        return f"Id: {self.id[0:6]} - Cliente: {self.cliente} - Fecha y hora: {self.fecha_hora.strftime('%Y-%m-%d %H:%M')} - Duracion: {self.duracion_minutos} min - Servicio: {self.servicio}"

#casos de ejemplo
turno = Turno("Juan", "2022-01-01 10:00:00", 30, "Corte de cabello")
print(turno)