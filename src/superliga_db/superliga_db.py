
import mysql.connector


def conectar_db():
    """
    Establece una conexión a la base de datos y devuelve el objeto de conexión.
    """
    try:

        conexion = mysql.connector.connect(
            host="localhost",
            user="tu_usuario",
            password="tu_contraseña",
            database="nombre_de_la_base_de_datos"
        )

        print("Conexión a la base de datos establecida correctamente.")
        return conexion
    except Exception as error:
        print(f"Error al conectar a la base de datos: {error}")
        return None


def cerrar_db(conexion):
    """
    Cierra la conexión a la base de datos.
    """
    if conexion:
        conexion.close()
        print("Conexión a la base de datos cerrada.")


if __name__ == "__main__":

    mi_conexion = conectar_db()
    if mi_conexion:

        cursor = mi_conexion.cursor()
        cursor.execute("SELECT * FROM Jugador")
        resultados = cursor.fetchall()
        for fila in resultados:
            print(fila)
        cursor.close()

        cerrar_db(mi_conexion)
