✂️ Sistema de Turnos para Peluquería
Proyecto final – Programación Orientada a Objetos (Python)

Este es un sistema de gestión de turnos para una peluquería, desarrollado completamente en Python y utilizando Programación Orientada a Objetos (POO).
Funciona por consola, guarda clientes y turnos en archivos CSV y permite convertirlos a JSON simulando una base de datos persistente.

📌 Características principales
👤 Gestión de clientes

Registrar nuevos clientes.

Validar que no exista otro cliente con el mismo teléfono.

Guardado automático en clientes.csv.

Carga automática de clientes al iniciar el programa.

🗓️ Gestión de turnos

Crear turnos para clientes existentes.

Control de solapamientos entre turnos.

Validación del horario laboral.

Modificación de turnos.

Listado completo de turnos.

Generación de slots disponibles por día.

Guardado automático en turnos.csv.

💾 Persistencia de datos

Los datos se almacenan en archivos CSV.
Conversión de CSV a JSON.
Los datos se cargan automáticamente si existen archivos previos.

📁 Estructura del proyecto
/Proyecto
│── clientes.csv
│── turnos.csv
│── turnos.json
│── README.md
└── peluqueria.py (o archivo principal del sistema)

🧱 Clases principales
Cliente

Representa a un cliente de la peluquería.
Atributos: id, nombre, telefono, email.

Turno

Representa un turno agendado.
Atributos: id, cliente, fecha_hora, duracion, servicio, fecha_finalizacion.

Peluqueria

Administra clientes, turnos, archivos y operaciones del sistema.
Incluye métodos como:

registrar_cliente()

agregar_turno()

listar_turnos()

modificar_turno()

generar_slots_disponibles()

mostrar_slots_disponibles()

guardar_clientes_en_csv()

cargar_clientes_desde_csv()

guardar_turno_en_csv()

csv_a_json()

🔄 Conversión CSV → JSON

El sistema permite convertir el archivo turnos.csv en un archivo turnos.json.

▶️ Ejecución del programa

Solo ejecuta el archivo principal

python peluqueria.py


El sistema mostrará un menú por consola que permite:

1) Registrar nuevo cliente
2) Solicitar turno
3) Listar turnos existentes
4) Modificar turno
5) Cancelar turno
6) Guardar/convertir turno de csv a Json
7) Ver cliente registrados
8) Salir


📄 Licencia

Proyecto académico — uso libre para aprendizaje.
