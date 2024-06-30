from flask import Flask, request, jsonify

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------

app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas


class Catalogo:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()
        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err
                
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS personajes (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            descripcion VARCHAR(255) NOT NULL,
            imagen_url VARCHAR(255))''')
        self.conn.commit()
        
        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)    

    # Agregar personaje
    def agregar_personaje(self, nombre, descripcion, imagen):
        sql = "INSERT INTO personajes (nombre, descripcion, imagen_url) VALUES (%s, %s, %s)"
        valores = (nombre, descripcion, imagen)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.lastrowid
    
    def listar_personajes(self):
        self.cursor.execute("SELECT * FROM personajes")
        personajes = self.cursor.fetchall()
        return personajes        

    # Método para consultar un personaje
    def consultar_personaje(self, id):
        # Consultamos un personaje a partir de su ID
        self.cursor.execute(f"SELECT * FROM personajes WHERE ID = {id}")
        return self.cursor.fetchone()
    
    def mostrar_personaje(self, id):
        # Mostramos los datos de un producto a partir de su código
        personaje = self.consultar_personaje(id)
        if personaje:
            print("-" * 40)
            print(f"Código.....: {personaje['ID']}")            
            print(f"Nombre.....: {personaje['nombre']}")            
            print(f"Descripción: {personaje['descripcion']}")
            print(f"Imagen.....: {personaje['imagen_url']}")
            print("-" * 40)
        else:
            print("Producto no encontrado.")    

    def modificar_personaje(self,id, nuevo_nombre, nueva_descripcion, nueva_imagen):
        sql = "UPDATE personajes SET nombre = %s, descripcion = %s, imagen_url = %s WHERE id = %s"
        valores = (nuevo_nombre, nueva_descripcion, nueva_imagen, id)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar_personaje(self, id):
        # Eliminamos un producto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM personajes WHERE id = {id}")
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    # Método para cerrar la conexión
    def cerrar_conexion(self):
        self.cursor.close()
        self.conn.close()

# Programa principal
catalogo = Catalogo(host='localhost', user='root', password='', database='nexus')

# Carpeta para guardar las imagenes
ruta_destino = './static/imagenes/'

# # Llamar al método agregar_personaje correctamente
# catalogo.agregar_personaje('Naruto', 'protagonista de Naruto', 'naruto.jpg')

# # # # Consultamos un personaje y lo mostramos
# id_personaje = input("Ingrese el ID del personaje: ")
# try:
#     id_personaje = int(id_personaje)
#     personaje = catalogo.consultar_personaje(id_personaje)
#     if personaje:
#         print(f"personaje encontrado: {personaje['nombre']} - {personaje['descripcion']}")
#     else:
#         print(f'personaje con ID= {id_personaje} no encontrado.')
# except ValueError:
#     print("El ID debe ser un número entero válido.")
    
# # Listar productos
# personajes = catalogo.listar_personajes()
# for personaje in personajes:
#     print(personaje)
 
# print("-" * 120)   
    
# # Eliminar un personaje
# catalogo.eliminar_personaje(6)
# personajes = catalogo.listar_personajes()
# for personaje in personajes:
#     print(personaje)
    
        

# # Cerrar la conexión cuando ya no se necesite
# catalogo.cerrar_conexion()


# #probando Flask
@app.route("/personajes", methods=["GET"])
def listar_personajes():
    personajes = catalogo.listar_personajes()
    return jsonify(personajes)

@app.route("/personajes/<int:id>", methods=["GET"])
def mostrar_personajes(id):
    personaje = catalogo.consultar_personaje(id)
    if personaje:
        return jsonify(personaje)
    else:
        return "Producto no encontrado", 404
    
@app.route("/personajes", methods=["POST"])
def agregar_personaje():
    #Recojo los datos del form
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    imagen = request.files['imagen_url']
    nombre_imagen = ""

    # Genero el nombre de la imagen
    nombre_imagen = secure_filename(imagen.filename)
    nombre_base, extension = os.path.splitext(nombre_imagen) 
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"

    nuevo_id = catalogo.agregar_personaje(nombre, descripcion, nombre_imagen)
    if nuevo_id:    
            imagen.save(os.path.join(ruta_destino, nombre_imagen))
            return jsonify({"mensaje": "Producto agregado correctamente.", "codigo": nuevo_codigo, "imagen": nombre_imagen}), 201
    else:
            return jsonify({"mensaje": "Error al agregar el producto."}), 500    

@app.route("/personajes/<int:id>", methods=["PUT"])
def modificar_producto(id):
    #Se recuperan los nuevos datos del formulario
    nuevo_nombre = request.form.get("nombre")
    nueva_descripcion = request.form.get("descripcion")
    
    # Verifica si se proporcionó una nueva imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        # Procesamiento de la imagen
        nombre_imagen = secure_filename(imagen.filename) 
        nombre_base, extension = os.path.splitext(nombre_imagen) 
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" 

        # Guardar la imagen en el servidor
        imagen.save(os.path.join(ruta_destino, nombre_imagen))
        
        # Busco el producto guardado
        personaje = catalogo.consultar_personaje(id)
        if personaje: # Si existe el producto...
            imagen_vieja = personaje["imagen_url"]
            # Armo la ruta a la imagen
            ruta_imagen = os.path.join(ruta_destino, imagen_vieja)

            # Y si existe la borro.
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
    else:     
        personaje = catalogo.consultar_personaje(id)
        if personaje:
            nombre_imagen = personaje["imagen_url"]

   # Se llama al método modificar_producto pasando el codigo del producto y los nuevos datos.
    if catalogo.modificar_personaje(id, nuevo_nombre, nueva_descripcion, nombre_imagen):
        return jsonify({"mensaje": "Producto modificado"}), 200
    else:
        return jsonify({"mensaje": "Producto no encontrado"}), 403

@app.route("/personajes/<int:id>", methods=["DELETE"])
def eliminar_personaje(id):
    # Primero, obtiene la información del producto para encontrar la imagen
    personaje = catalogo.consultar_personaje(id)
    if personaje:
        # Eliminar la imagen asociada si existe
        ruta_imagen = os.path.join(ruta_destino, personaje['imagen_url'])
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        # Luego, elimina el producto del catálogo
        if catalogo.eliminar_personaje(id):
            return jsonify({"mensaje": "Producto eliminado"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar el producto"}), 500
    else:
        return jsonify({"mensaje": "Producto no encontrado"}), 404
    
if __name__ == "__main__":
    app.run(debug=True)