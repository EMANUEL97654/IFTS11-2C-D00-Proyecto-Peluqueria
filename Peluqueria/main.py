from datetime import datetime, timedelta
from modelos.peluqueria import Peluqueria

            
def menu():
    peluqueria = Peluqueria("Peluqueria Emanuel")
    
    while True:
        print("\nBienvenido a la peluqueria Emanuel")
        print("\n ### MENU PRINCIPAL ###")
        print("1. Registrar nuevo cliente")
        print("2. Registar turno")
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
                print("Saliendo del programa...")
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



