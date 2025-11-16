from datetime import datetime, timedelta
import json
import os
import uuid
import csv


class Cliente(object):
    def __init__(self,nombre,telefono,email=""):
        self.id = str(uuid.uuid4())[0:4]
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def __str__(self):
        return f"{self.nombre}-{self.telefono}-{self.email}"
    
#casos de ejemplo
""" cliente = Cliente("Juan", "1234567890", "juan@gmail.com")
print(cliente) """

class Turno(object):
    def __init__(self,cliente,fecha_hora,duracion,servicio):
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
        
        while True: 
            cliente_existente = self.buscar_cliente_por_telefono(telefono)
            if cliente_existente:
                print(f"Ya existe un cliente con ese telefono: {cliente_existente.nombre}.")
                telefono = input("Ingrese otro telefono: ")
            else:
                break
        cliente_existente = self.buscar_cliente_por_telefono(telefono)
        if cliente_existente:
            print(f"Ya existe un cliente con ese telefono: {cliente_existente.nombre}.")
        
        cliente = Cliente(nombre,telefono,email)
        self.clientes.append(cliente)
        self.guardar_clientes_en_csv()
        print(f"Cliente registrado: {cliente.nombre}")
        return cliente
    
    def guardar_clientes_en_csv(self, archivo="clientes.csv"):
        with open(archivo,"w",newline="",encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Id","Nombre","Telefono","Email"])
            for cliente in self.clientes:
                writer.writerow([cliente.id,cliente.nombre,cliente.telefono,cliente.email])
            print(f"Datos de clientes guardados en {archivo}.")
    
    def cargar_clientes_desde_csv(self,archivo="clientes.csv"):
        try:
            with open(archivo,newline="",encoding="utf-8") as archivo:
                reader = csv.DictReader(archivo)
                for row in reader:
                    if not self.buscar_cliente_por_telefono(row["Telefono"]):
                        cliente = Cliente(row["Nombre"],row["Telefono"],row["Email"])
                        cliente.id = row["Id"]
                        self.clientes.append(cliente)
            print(f"Datos de clientes cargados desde {archivo}.")
        except FileNotFoundError:
            print(f"Error al cargar clientes desde {archivo}. Archivo no encontrado.")
    
    
    #Area de gestion de turnos
    def agregar_turno(self,cliente,fecha_hora,duracion,servicio):
        fecha_finalizacion = fecha_hora + timedelta(minutes=duracion)
        
        if fecha_hora.time() < self.horario_apertura or fecha_finalizacion.time() > self.horario_cierre:
            print(f"El turno se encuentra fuera del horario laboral ({self.horario_apertura.strftime('%H:%M') - self.horario_cierre.strftime('%H:%M')}).")
            return
        
        #Chequear que no se solapen los turnos
        for turno in self.turnos:
            if turno.cliente == cliente:
                print(f"El cliente {cliente.nombre} ya tiene un turno asignado.")
                return
            if fecha_hora < turno.fecha_hora_finalizacion and fecha_finalizacion > turno.fecha_hora:
                print(f"El turno se solapa con el turno del cliente {turno.cliente.nombre}.")
                return
        
        turno = Turno(cliente, fecha_hora, duracion, servicio)
        self.turnos.append(turno)
        self.turnos.sort(key=lambda turno: turno.fecha_hora)
        print(f"TUrno agregado: {turno}")
        self.guardar_turno_en_csv()
        return turno
    
    def guardar_turno_en_csv(self,archivo="turnos.csv"):
        with open(archivo,"w",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Id","nombre","telefono","servicio","Fecha","Hora","duracion"])
            for turno in self.turnos:
                writer.writerow([turno.id,
                                turno.cliente.nombre,
                                turno.cliente.telefono,
                                turno.fecha_hora.date().isoformat(),
                                turno.fecha_hora.time().strftime("%H:%M"),
                                turno.duracion])
        
        print(f"Datos de turno guardado en {archivo}")
        
    def listar_turnos(self):
        if not self.turnos: 
            print("No hay turnos registrados.")
            return 
        print("\n --- Lista de turnos ---")
        for turno in self.turnos:
            print(turno)
    
    def modificar_turno(self,id_turno,nueva_fecha):
        for turno in self.turnos:
            if turno.id.startswith(id_turno):
                turno.fecha_hora = nueva_fecha
                self.turnos.sort(key=lambda x: x.fecha_hora)
                print("Turno modificado con éxito: {turno}")
                return
        print("No se encontró el turno a modificar.")
        
    def generar_slots_disponibles(self,fecha,duracion_slot=15):
        fecha_inicial = datetime.combine(fecha.date(),self.horario_apertura)
        fecha_final = datetime.combine(fecha.date(),self.horario_cierre)
        slots = []
        while fecha_inicial < fecha_final:
            slots.append(fecha_inicial)
            fecha_inicial += timedelta(minutes=duracion_slot)
        return slots
    
    def mostrar_slots_disponibles(self,fecha,duracion_servicio,duracion_slot=15):
        slots_iniciales = self.generar_slots_disponibles(fecha,duracion_slot)
        print("\n ### Slots disponibles ###")
        
        for item,inicio in enumerate(slots_iniciales,1):
            fin = inicio + timedelta(minutes=duracion_servicio)
            if fin.time() > self.horario_cierre:
                continue
            #verificar si el slot esta disponible
            ocupado = any(
                (t.fecha_hora < fin and t.fecha_fin > inicio)
                for t in self.turnos
                if t.fecha_hora.date() == fecha.date()
            )
            estado = "[X]" if ocupado else "[ ]"
            print(f"{item:02d}. {estado} {inicio.strftime('%H:%M')} - {fin.strftime('%H:%M')}")
    
    def csv_a_json(self,archivo_csv="turnos.csv",archivo_json="turnos.json"):
        try:
            with open(archivo_csv,newline="",encoding="utf-8") as archivo:
                reader = csv.DictReader(archivo)
                datos = list(reader)
            with open(archivo_json,"w",encoding="utf-8") as archivoJson:
                json.dump(datos,archivoJson,indent=4,ensure_ascii=False)
            print("Archivo CSV convertido a JSON exitosamente")
        except FileNotFoundError:
            print("No se encontro el archivo CSV")
        except Exception as e:
            print(f"Ocurrio un error al convertir el archivo CSV a JSON: {e}")
    
    
    
    
    
#cargar cliente a ver si funciona el guardado en csv
""" pelu = Peluqueria("Peluqueria Emanuel")

nombre = input("Ingrese el nombre del cliente: ")
telefono = input("Ingrese el telefono del cliente: ")
email = input("Ingrese el email del cliente: ")
pelu.registrar_cliente(nombre,telefono,email) """

#cargar cliente desde csv prueba
""" pelu = Peluqueria("Pasdasdasd")
pelu.cargar_clientes_desde_csv("clientes.csv")

for c in pelu.clientes:
    print(f"ID: {c.id}, Nombre: {c.nombre}, Telefono: {c.telefono}, Email: {c.email}") """
    
#Guardar turno en csv

""" fecha1 = datetime(2025,11,12,10,0)
fecha2 = datetime(2025,11,12,11,0)
fecha_fuera=datetime(2025,11,12,20,0)

peluqueria = Peluqueria("Peluqueria Emanuel")

cliente1 = peluqueria.registrar_cliente("Juan Perez","123456789","juanperez@gmail.com")
peluqueria.agregar_turno(cliente1,fecha1,60,"Corte de cabello")

peluqueria.guardar_turno_en_csv("turnos.csv") """

#Falta agregar un metodo para cargar turnos para que lo reconozca el metodo listar turnos
""" pelu = Peluqueria("Peluqueria Emanuel")
pelu.listar_turnos()  """