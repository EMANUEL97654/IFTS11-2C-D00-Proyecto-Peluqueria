from datetime import datetime, timedelta
import json
import os
import uuid
import csv


class Cliente(object):
    def __init__(self,nombre,telefono,email=""):
        #Genero un id unico corto usando la libreria uuid
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

class Peluqueria(object):
    def __init__(self,nombre,horario_apertura="09:00",horario_cierre="20:00"):
        self.nombre = nombre
        self.turnos = []
        self.clientes = []
        #Convierto horarios a objetos time
        self.horario_apertura = datetime.strptime(horario_apertura, "%H:%M").time()
        self.horario_cierre = datetime.strptime(horario_cierre, "%H:%M").time()
        
        #Carga los clientes al inicio si existe el archivo
        if os.path.exists("clientes.csv"):
            self.cargar_clientes_desde_csv("clientes.csv")
        
        #Carga los turnos al inicio si existe el archivo
        if os.path.exists("turnos.json"):
            self.cargar_turnos_desde_json("turnos.json")
    
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
    
    #Listo todos los clientes en memoria
    def listar_clientes(self):
        if not self.clientes:
            print("No hay clientes registrados en memoria.")
            # Opcional: intentar recargar por si acaso
            if os.path.exists("clientes.csv"):
                print("Intentando cargar clientes desde clientes.csv...")
                self.cargar_clientes_desde_csv("clientes.csv")
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
    
    #Guardo todos los clientes en un csv
    def guardar_clientes_en_csv(self, archivo="clientes.csv"):
        with open(archivo,"w",newline="",encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Id","Nombre","Telefono","Email"])
            for cliente in self.clientes:
                writer.writerow([cliente.id,cliente.nombre,cliente.telefono,cliente.email])
            print(f"Datos de clientes guardados en {archivo}.")
    
    def cargar_clientes_desde_csv(self,archivo="clientes.csv"):
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
    
    def guardar_turno_en_csv(self,archivo="turnos.csv"):
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
    
    
    def cargar_turnos_desde_json(self,archivo="turnos.json"):
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
            
def menu():
    peluqueria = Peluqueria("Peluqueria Emanuel")
    
    while True:
        print("\nBienvenido a la peluqueria Emanuel")
        print("\n ### MENU PRINCIPAL ###")
        print("1. Registrar nuevo cliente")
        print("2. Solicitar turno")
        print("3. Listar turnos existentes")
        print("4. Modificar turno")
        print("5. Cancelar turno")
        print("6. Guardar/Convertir Turnos de csv a Json")
        print("7. Ver clientes registrados")
        print("8. Salir")
        
        opcion = input("Ingrese una opcion: ")
        
        try:
            if opcion == "1":
                nombre = input("Ingrese el nombre del cliente: ")
                telefono = input("Ingrese el telefono del cliente: ")
                email = input("Ingrese el email del cliente: ")
                peluqueria.registrar_cliente(nombre, telefono, email)
            elif opcion == "2":
                peluqueria.listar_clientes()
                if not peluqueria.clientes:
                    print("No hay clientes registrados. Por favor, registre un cliente primero.")
                    continue
                
                telefono = input("Teléfono del cliente: ")
                cliente = peluqueria.buscar_cliente_por_telefono(telefono)
                if not cliente:
                    print("Cliente no encontrado.")
                    continue
                
                # --- FECHA ---
                fecha_input = input("Ingrese la fecha del turno (DD/MM/AAAA): ")
                fecha = datetime.strptime(fecha_input, "%d/%m/%Y")   # fecha como datetime

                # --- SERVICIO ---
                servicio = input("Ingrese el servicio a realizar: ")

                # --- DURACIÓN ---
                duracion = int(input("Ingrese la duración del servicio en minutos: "))

                # --- MOSTRAR SLOTS DISPONIBLES ---
                slots = peluqueria.generar_slots_disponibles(fecha)   # genera lista real de slots

                print("\n### SLOTS DISPONIBLES ###")
                for i, inicio in enumerate(slots, 1):
                    fin = inicio + timedelta(minutes=duracion)

                    #No pasar del horario de cierre
                    if fin.time() > peluqueria.horario_cierre:
                        continue

                    #Revisar solapamientos
                    ocupado = any(
                        (t.fecha_hora < fin and t.fecha_finalizacion > inicio)
                        for t in peluqueria.turnos
                        if t.fecha_hora.date() == fecha.date()
                    )

                    estado = "[X]" if ocupado else "[ ]"
                    print(f"{i:02d}. {estado} {inicio.strftime('%H:%M')} - {fin.strftime('%H:%M')}")

                # --- SELECCIONAR SLOT ---
                opcion_slot = int(input("Seleccione un número de slot disponible: "))
                if opcion_slot < 1 or opcion_slot > len(slots):
                    print("Opción inválida.")
                    continue

                inicio_slot = slots[opcion_slot - 1]
                fin_slot = inicio_slot + timedelta(minutes=duracion)

                # Verificar nuevamente
                solapado = any(
                    (t.fecha_hora < fin_slot and t.fecha_finalizacion > inicio_slot)
                    for t in peluqueria.turnos
                    if t.fecha_hora.date() == fecha.date()
                )

                if solapado:
                    print("El turno se solapa con otro. Seleccione otro horario.")
                    continue

                peluqueria.agregar_turno(cliente, inicio_slot, duracion, servicio)
                print("Turno agregado exitosamente.")
            
            elif opcion == "3":
                peluqueria.listar_turnos()
                
            elif opcion == "4":
                peluqueria.listar_turnos()
                id_turno = input("Ingrese el ID del turno a modificar: ")
                nueva_fecha_string = input("Nueva fecha y hora (DD/MM/AAAA HH:MM): ")
                nueva_fecha = datetime.strptime(nueva_fecha_string, "%d/%m/%Y %H:%M")
                peluqueria.modificar_turno(id_turno, nueva_fecha)
                
            elif opcion == "5":
                peluqueria.listar_turnos()
                id_turno = input("Ingrese el ID del turno a eliminar: ")
                peluqueria.eliminar_turno(id_turno)
            
            elif opcion == "6":
                peluqueria.guardar_turno_en_csv("turnos.csv")
                peluqueria.csv_a_json()
                
            elif opcion == "7":
                print("Mostrando la lista de clientes registrados")
                peluqueria.cargar_clientes_desde_csv()
                peluqueria.listar_clientes()
            
            elif opcion == "8":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida. Por favor, ingrese una opción válida.")
        
        except Exception as e:
            print(f"Ocurrio un error inesperado: {e}")
            

#Donde se va a ejecutar el programa principal
if __name__ == "__main__":
    menu()
            
            
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

#Prueba para csv_a_json
""" pelu = Peluqueria("Peluqueria Emanuel")
cliente = Cliente("Ana","12345678777","ana@gmail.com")
turno = Turno(cliente,"2025-01-01 10:00:00",30,"Coloracion")
pelu.turnos.append(turno)
pelu.guardar_turno_en_csv()

pelu.csv_a_json("turnos.csv","turnos.json")

with open("turnos.json","r",encoding="utf-8") as f:
    print(f.read()) """
    
#prueba para slots de turnos
""" pelu = Peluqueria("Peluqueria Emanuel")
pelu.mostrar_slots_disponibles("2025-01-01 10:00:00",30) """

#Pruebo a ver si lee los turnos desde el json
""" pelu = Peluqueria("Peluqueria Emanuel")
pelu.listar_turnos() """

#prueba a ver si el menu funciona
#Esto funciona pero genera un loop infinito
""" menu() """

