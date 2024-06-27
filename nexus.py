import mysql.connector

class Catalogo:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS personajes (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            descripcion VARCHAR(255) NOT NULL,
            imagen_url VARCHAR(255))''')
        self.conn.commit()

    # Agregar personaje
    def agregar_personaje(self, nombre, descripcion, imagen):
        sql = "INSERT INTO personajes (nombre, descripcion, imagen_url) VALUES (%s, %s, %s)"
        valores = (nombre, descripcion, imagen)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.lastrowid

    # Método para cerrar la conexión
    def cerrar_conexion(self):
        self.cursor.close()
        self.conn.close()

    # Método para consultar un personaje
    def consultar_personaje(self, id):
        # Consultamos un personaje a partir de su ID
        self.cursor.execute(f"SELECT * FROM personajes WHERE ID = {id}")
        return self.cursor.fetchone()

# Programa principal
catalogo = Catalogo(host='localhost', user='root', password='', database='nexus')

# Llamar al método agregar_personaje correctamente
#catalogo.agregar_personaje('Goku', 'protagonista de Dragon Ball', 'goku.jpg')

# Consultamos un personaje y lo mostramos
id_personaje = input("Ingrese el ID del personaje: ")
try:
    id_personaje = int(id_personaje)
    personaje = catalogo.consultar_personaje(id_personaje)
    if personaje:
        print(f"personaje encontrado: {personaje['nombre']} - {personaje['descripcion']}")
    else:
        print(f'personaje con ID= {id_personaje} no encontrado.')
except ValueError:
    print("El ID debe ser un número entero válido.")

# Cerrar la conexión cuando ya no se necesite
catalogo.cerrar_conexion()
