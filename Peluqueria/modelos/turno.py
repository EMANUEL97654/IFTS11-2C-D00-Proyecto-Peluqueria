from datetime import datetime,timedelta
import uuid


class Turno(object):
    def __init__(self,cliente,fecha_hora,duracion,servicio):
        #Genero un id unico para el turno
        self.id = str(uuid.uuid4())[0:4]
        self.cliente = cliente
        
        #convierte la fecha y hora en string en caso de necesitarlo
        if isinstance(fecha_hora,str):
            self.fecha_hora = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S")
        else:
            self.fecha_hora = fecha_hora
            
        self.duracion = duracion
        self.servicio = servicio
        self.fecha_finalizacion = self.fecha_hora + timedelta(minutes=duracion)
        #uso timedelta para representar la diferencia entre dos fechas
        

    def __str__(self):
        return f"Id: {self.id[0:4]} - Cliente: {self.cliente} - Fecha y hora: {self.fecha_hora.strftime('%Y-%m-%d %H:%M')} - Duracion: {self.duracion} min - Servicio: {self.servicio}"

#casos de ejemplo
""" turno = Turno("Juan", "2022-01-01 10:00:00", 30, "Corte de cabello")
print(turno) """