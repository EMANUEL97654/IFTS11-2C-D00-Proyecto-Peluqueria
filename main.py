from datetime import datetime, timedelta
import os
import uuid
import csv


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
""" turno = Turno("Juan", "2022-01-01 10:00:00", 30, "Corte de cabello")
print(turno) """

class Peluqueria(object):
    def __init__(self,nombre,horario_apertura="09:00",horario_cierre="20:00"):
        self.nombre = nombre
        self.turnos = []
        self.clientes = []
        self.horario_apertura = datetime.strptime(horario_apertura, "%H:%M").time()
        self.horario_cierre = datetime.strptime(horario_cierre, "%H:%M").time()
        
        #Carga los clientes al inicio si existe elarchivo
        if os.path.exists("clientes.csv"):
            self.cargar_clientes_desde_csv("clientes.csv")
        
        if os.path.exists("turnos.json"):
            self.cargar_turnos_desde_csv("turnos.json")
    
    def buscar_cliente_por_telefono(self,telefono):
        for cliente in self.clientes:
            if cliente.telefono == telefono:
                return cliente
        return None
    
    def registrar_cliente(self,nombre,telefono,email=""):
        cliente_existente = self.buscar_cliente_por_telefono(telefono)
        if cliente_existente:
            print(f"Ya existe un cliente con ese telefono: {cliente_existente.nombre}.")
        
        cliente = Cliente(nombre,telefono,email)
        self.clientes.append(cliente)
        self.guardar_clientes_en_csv()
        return cliente
    
    def guardar_clientes_en_csv(self, archivo="clientes.csv"):
        with open(archivo,"w",newline="",encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Id","Nombre","Telefono","Email"])
            for cliente in self.clientes:
                writer.writerow([cliente.id,cliente.nombre,cliente.telefono,cliente.email])
            print(f"Datos de clientes guardados en {archivo}.")
    
    
#cargar cliente a ver si funciona el guardado en csv
""" pelu = Peluqueria("Peluqueria Emanuel")

nombre = input("Ingrese el nombre del cliente: ")
telefono = input("Ingrese el telefono del cliente: ")
email = input("Ingrese el email del cliente: ")

pelu.registrar_cliente(nombre,telefono,email) """

