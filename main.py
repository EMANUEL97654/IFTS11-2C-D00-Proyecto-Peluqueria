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
cliente = Cliente("Juan", "1234567890", "juan@gmail.com")
print(cliente)