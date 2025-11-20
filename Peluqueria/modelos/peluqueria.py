from datetime import datetime, timedelta
import os
import csv
import json

from modelos.cliente import Cliente
from modelos.turno import Turno
from modelos.peluqueros import Peluquero


class Peluqueria(object):
    def __init__(self,nombre,horario_apertura="09:00",horario_cierre="20:00"):
        self.nombre = nombre
        self.turnos = []
        self.clientes = []
        self.peluqueros = []
        self.cargar_peluqueros_desde_csv()
        #Convierto horarios a objetos time
        self.horario_apertura = datetime.strptime(horario_apertura, "%H:%M").time()
        self.horario_cierre = datetime.strptime(horario_cierre, "%H:%M").time()
        
        #Carga los clientes al inicio si existe el archivo
        if os.path.exists("Clientes/clientes.csv"):
            self.cargar_clientes_desde_csv("Clientes/clientes.csv")
        
        #Carga los turnos al inicio si existe el archivo
        if os.path.exists("Turnos/turnos.json"):
            self.cargar_turnos_desde_json("Turnos/turnos.json")
            
        if os.path.exists("Peluqueros/peluqueros.csv"):
            self.cargar_peluqueros_desde_csv("Peluqueros/peluqueros.csv")
    
    def buscar_cliente_por_telefono(self,telefono):
        for cliente in self.clientes:
            if cliente.telefono == telefono:
                return cliente
        return None
    
    def registrar_cliente(self,nombre,telefono,email=""):
        #Evito registrar clientes duplicados por telefono
        while True: 
            cliente_existente = self.buscar_cliente_por_telefono(telefono)
            if cliente_existente:
                print(f"Ya existe un cliente con ese telefono: {cliente_existente.telefono}.")
                telefono = input("Ingrese otro telefono: ")
            else:
                break
        cliente_existente = self.buscar_cliente_por_telefono(telefono)
        if cliente_existente:
            print(f"Ya existe un cliente con ese telefono: {cliente_existente.telefono}.")
        
        cliente = Cliente(nombre,telefono,email)
        self.clientes.append(cliente)
        self.guardar_clientes_en_csv()
        print(f"Cliente registrado: {cliente.nombre}")
        return cliente
    
    def registrar_peluquero(self, nombre, especialidad=""):
        peluquero = Peluquero(nombre, especialidad)
        self.peluqueros.append(peluquero)
        self.guardar_peluqueros_en_csv()
        return peluquero

    
    #Listo todos los clientes en memoria
    def listar_clientes(self):
        if not self.clientes:
            print("No hay clientes registrados en memoria.")
            # Opcional: intentar recargar por si acaso
            if os.path.exists("clientes.csv"):
                print("Intentando cargar clientes desde clientes.csv...")
                self.cargar_clientes_desde_csv("Clientes/clientes.csv")
                if not self.clientes:
                    print("El archivo clientes.csv existe pero está vacío o no tiene formato válido.")
                    return
            else:
                return
        
        print("\n ### Lista de clientes registrados (en memoria) ###")
        # Mostrar el encabezado de la tabla
        print("-" * 60)
        #Calculo los espacios para que queden bien alineados
        print(f"{'ID':<6}{'Nombre':<20}{'Teléfono':<15}{'Email':<19}")
        print("-" * 60)
        
        for cliente in self.clientes:
            print(f"{cliente.id:<6}{cliente.nombre:<20}{cliente.telefono:<15}{cliente.email:<19}")
        print("-" * 60)
    
    
    def listar_peluqueros(self):
       try:
           with open("Peluqueros/peluqueros.csv","r",newline="",encoding="utf-8") as file:
               lector = csv.reader(file)
               peluqueros = []
               next(lector,None)
               
               for fila in lector:
                   if len(fila) < 3:
                       continue
               
               id_,nombre,especialidad = fila
               peluqueros.append((id_,nombre,especialidad))
               
               if not peluqueros:
                   print("No hay peluqueros registrados.")
                   return
               
               print("\n ### Lista de peluqueros registrados ###")
               for i, (id_,nombre,especialidad) in enumerate(peluqueros,start=1):
                   esp = especialidad if especialidad else "Sin especialidad"
                   print("-" *60)
                   print(f"{i:<3}-{nombre:<20}{esp:<20} - ID: {id_}")
       except FileNotFoundError:
           print("El archivo de peluqueros no existe.")
        
    #Guardo todos los clientes en un csv
    def guardar_clientes_en_csv(self, archivo="Clientes/clientes.csv"):
        with open(archivo,"w",newline="",encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Id","Nombre","Telefono","Email"])
            for cliente in self.clientes:
                writer.writerow([cliente.id,cliente.nombre,cliente.telefono,cliente.email])
            print(f"Datos de clientes guardados en {archivo}.")
            
    def guardar_peluqueros_en_csv(self,archivo="Peluqueros/peluqueros.csv"):
        os.makedirs(os.path.dirname(archivo),exist_ok=True)
        try:
            with open(archivo,"w",newline="",encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Id","Nombre","Especialidad"])
                for peluquero in self.peluqueros:
                    writer.writerow([peluquero.id,peluquero.nombre,peluquero.especialidad])
            print(f"Datos de peluqueros guardados en {archivo}.")
        except FileNotFoundError:
            print(f"El archivo {archivo} no existe.")
    
    def cargar_clientes_desde_csv(self,archivo="Clientes/clientes.csv"):
        try:
            with open(archivo,newline="",encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if not self.buscar_cliente_por_telefono(row["Telefono"]):
                        cliente = Cliente(row["Nombre"],row["Telefono"],row["Email"])
                        cliente.id = row["Id"]
                        self.clientes.append(cliente)
            print(f"Datos de clientes cargados desde {archivo}.")
        except FileNotFoundError:
            print(f"Error al cargar clientes desde {archivo}. Archivo no encontrado.")
            
    
    def cargar_peluqueros_desde_csv(self,archivo="Peluqueros/peluqueros.csv"):
        if not os.path.exists(archivo):
            print("no existe el archivo de peluqueros")
            return
        try:
            with open(archivo,"r",encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    peluquero = Peluquero(
                        nombre = row["Nombre"],
                        especialidad = row["Especialidad"]
                    )
                    peluquero.id = row["Id"]
                    self.peluqueros.append(peluquero)
        except FileNotFoundError:
            print(f"Error al cargar peluqueros desde {archivo}. Archivo no encontrado.")

            print(f"{len(self.peluqueros)} peluqueros cargados desde {archivo}.")
    
    
    #Area de gestion de turnos
    
    def agregar_turno(self,cliente,fecha_hora,duracion,servicio):
        fecha_finalizacion = fecha_hora + timedelta(minutes=duracion)
        #Comprobacion del horario laboral
        if fecha_hora.time() < self.horario_apertura or fecha_finalizacion.time() > self.horario_cierre:
            print(
                f"El turno se encuentra fuera del horario laboral "
                f"({self.horario_apertura.strftime('%H:%M')} - {self.horario_cierre.strftime('%H:%M')}).")
            return
        
        #Chequear que no se solapen los turnos
        for turno in self.turnos:
            if turno.cliente == cliente:
                print(f"El cliente {cliente.nombre} ya tiene un turno asignado.")
                return
            if fecha_hora < turno.fecha_finalizacion and fecha_finalizacion > turno.fecha_hora:
                print(f"El turno se solapa con el turno del cliente {turno.cliente.nombre}.")
                return
        #Si pasa todas las validaciones, se agrega el turno
        turno = Turno(cliente, fecha_hora, duracion, servicio)
        self.turnos.append(turno)
        self.turnos.sort(key=lambda turno: turno.fecha_hora)
        print(f"Turno agregado: {turno}")
        self.guardar_turno_en_csv()
        return turno
    
    def guardar_turno_en_csv(self,archivo="Turnos/turnos.csv"):
        with open(archivo,"w",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Id","nombre","telefono","servicio","Fecha","Hora","duracion"])
            for turno in self.turnos:
                writer.writerow([turno.id,
                                turno.cliente.nombre,
                                turno.cliente.telefono,
                                turno.servicio,
                                turno.fecha_hora.date().isoformat(),
                                turno.fecha_hora.time().strftime("%H:%M"),
                                turno.duracion
                                ])
        
        print(f"Datos de turno guardado en {archivo}")
        
    def listar_turnos(self):
        if not self.turnos: 
            print("No hay turnos registrados.")
            return 
        print("\n ### Lista de turnos ###")
        for turno in self.turnos:
            print(turno)
    
    def eliminar_turno(self,id_turno):
        for turno in self.turnos:
            if turno.id.startswith(id_turno):
                self.turnos.remove(turno)
                print("Turno eliminado.")
                #agrego persistencia
                self.guardar_turno_en_csv()
                return
        print("No se encontró el turno.")
    
    def modificar_turno(self,id_turno,nueva_fecha):
        for turno in self.turnos:
            if turno.id.startswith(id_turno):
                turno.fecha_hora = nueva_fecha
                turno.fecha_finalizacion = nueva_fecha + timedelta(minutes=turno.duracion)
                self.turnos.sort(key=lambda x: x.fecha_hora)
                #agrego persistencia
                self.guardar_turno_en_csv()
                print(f"Turno modificado con éxito: {turno}")
                return
        print("No se encontró el turno a modificar.")
    
    #Genero una lista de horarios disponibles de un dia
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
    
    def csv_a_json(self,archivo_csv="Turnos/turnos.csv",archivo_json="Turnos/turnos.json"):
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
    
    
    def cargar_turnos_desde_json(self,archivo="Turnos/turnos.json"):
        try:
            with open(archivo,"r",encoding="utf-8") as archivoJson:
                datos = json.load(archivoJson)
            
            nuevos_turnos = []
            #Recorro cada turno del json y busco al cliente por telefono
            for item in datos:
                cliente_nombre = item.get("nombre","")
                telefono_cliente = item.get("telefono","")
                servicio = item.get("servicio","")
                fecha = item.get("Fecha","")
                hora = item.get("Hora","")
                duracion = int(item.get("duracion",0))
                
                #reconstruyo las fechas
                fecha_inicio = datetime.fromisoformat(f"{fecha}T{hora}")
                fecha_fin = fecha_inicio + timedelta(minutes=duracion)   
                             
                cliente = self.buscar_cliente_por_telefono(telefono_cliente)
                #Si aun asi no lo encuentra lo omite
                if not cliente:
                    cliente = Cliente(cliente_nombre,telefono_cliente)
                    self.clientes.append(cliente)
                
                turno = Turno(cliente,fecha_inicio,duracion,item["servicio"])
                turno.id = item["Id"]
                nuevos_turnos.append(turno)
            
            self.turnos.extend(nuevos_turnos)
            self.turnos.sort(key=lambda t: t.fecha_hora)
            print(f"Datos de turnos cargados desde {archivo}")
        except FileNotFoundError:
            print("No se encontro base de datos de turnos previa")
        except Exception as e:
            print(f"Error al cargar JSON: {e}")