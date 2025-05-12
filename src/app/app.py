import os
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.negocio import (
    crear_equipo,
    obtener_equipo_por_id,
    crear_jugador,
    obtener_jugador_por_id,
    actualizar_jugador,
    eliminar_jugador,
    crear_partido,
    obtener_partido_por_id,
    crear_estadistica,
    crear_estado_jugador,
    obtener_jugadores_de_equipo,
    obtener_partidos_de_equipo,
    obtener_estadisticas_de_partido,
    obtener_estado_jugadores_de_partido,
)
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL usando variables de entorno de Clever Cloud
DB_HOST = os.environ.get("POSTGRESQL_ADDON_HOST")
DB_USER = os.environ.get("POSTGRESQL_ADDON_USER")
DB_PASSWORD = os.environ.get("POSTGRESQL_ADDON_PASSWORD")
DB_NAME = os.environ.get("POSTGRESQL_ADDON_DB")

if DB_HOST and DB_USER and DB_PASSWORD and DB_NAME:
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
else:
    DATABASE_URL = "postgresql://tu_usuario:tu_contraseña@localhost/nombre_de_la_base_de_datos"
    print("Advertencia: Usando configuración de base de datos local. ¡Esto no debería usarse en producción!")

engine = create_engine(DATABASE_URL)
# Crear una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def conectar_db():
    try:
        print("Conexión a la base de datos establecida correctamente (a través de SQLAlchemy).")
        return SessionLocal()
    except Exception as error:
        print(f"Error al conectar a la base de datos: {error}")
        return None


def cerrar_db(session):
    if session:
        session.close()
        print("Conexión a la base de datos cerrada (a través de SQLAlchemy).")



@app.errorhandler(Exception)
def handle_error(error):
    session = conectar_db()
    cerrar_db(session)
    return jsonify({"error": str(error)}), 500


@app.route("/equipos", methods=["POST"])
def crear_equipo_route():
    session = conectar_db()
    try:
        data = request.get_json()
        nombre = data.get("nombre")
        ciudad = data.get("ciudad")
        entrenador = data.get("entrenador")
        if not nombre or not ciudad or not entrenador:
            return jsonify({"error": "Nombre, ciudad y entrenador son requeridos"}), 400
        equipo = crear_equipo(session, nombre=nombre, ciudad=ciudad, entrenador=entrenador)
        return jsonify({"id": equipo.id, "nombre": equipo.nombre, "ciudad": equipo.ciudad, "entrenador": equipo.entrenador}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cerrar_db(session)


@app.route("/equipos/<int:equipo_id>", methods=["GET"])
def obtener_equipo_route(equipo_id):
    session = conectar_db()
    try:
        equipo = obtener_equipo_por_id(session, equipo_id)
        if not equipo:
            return jsonify({"error": "Equipo no encontrado"}), 404
        return jsonify({"id": equipo.id, "nombre": equipo.nombre, "ciudad": equipo.ciudad, "entrenador": equipo.entrenador}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cerrar_db(session)


@app.route("/jugadores", methods=["POST"])
def crear_jugador_route():
    session = conectar_db()
    try:
        data = request.get_json()
        nombre = data.get("nombre")
        apellido = data.get("apellido")
        posicion = data.get("posicion")
        numero = data.get("numero")
        equipo_id = data.get("equipo_id")
        if not nombre or not apellido or not posicion or not numero or not equipo_id:
            return jsonify({"error": "Nombre, apellido, posicion, numero y equipo_id son requeridos"}), 400
        jugador = crear_jugador(session, nombre=nombre, apellido=apellido, posicion=posicion, numero=numero,
                               equipo_id=equipo_id)
        if not jugador:
            return jsonify({"error": "No se pudo crear el jugador"}), 400
        return jsonify(
            {"id": jugador.id, "nombre": jugador.nombre, "apellido": jugador.apellido, "posicion": jugador.posicion,
             "numero": jugador.numero, "equipo_id": jugador.equipo_id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cerrar_db(session)


@app.route("/jugadores/<int:jugador_id>", methods=["GET"])
def obtener_jugador_route(jugador_id):
    session = conectar_db()
    try:
        jugador = obtener_jugador_por_id(session, jugador_id)
        if not jugador:
            return jsonify({"error": "Jugador no encontrado"}), 404
        return jsonify(
            {"id": jugador.id, "nombre": jugador.nombre, "apellido": jugador.apellido, "posicion": jugador.posicion,
             "numero": jugador.numero, "equipo_id": jugador.equipo_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cerrar_db(session)


@app.route("/jugadores/<int:jugador_id>", methods=["PUT"])
def actualizar_jugador_route(jugador_id):
    session = conectar_db()
    try:
        data = request.get_json()
        nombre = data.get("nombre")
        apellido = data.get("apellido")
        posicion = data.get("posicion")
        numero = data.get("numero")
        equipo_id = data.get("equipo_id")

        jugador = actualizar_jugador(session, jugador_id, nombre, apellido, posicion, numero, equipo_id)
        if not jugador:
            return jsonify({"error": "No se pudo actualizar el jugador"}), 400
        return jsonify(
            {"id": jugador.id, "nombre": jugador.nombre, "apellido": jugador.apellido, "posicion": jugador.posicion,
             "numero": jugador.numero, "equipo_id": jugador.equipo_id}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cerrar_db(session)


@app.route("/jugadores/<int:jugador_id>", methods=["DELETE"])
def eliminar_jugador_route(jugador_id):
    session = conectar_db()
    try:
        eliminado = eliminar_jugador(session, jugador_id)
        if not eliminado:
            return jsonify({"error": "No se pudo eliminar el jugador"}), 400
        return jsonify({"mensaje": "Jugador eliminado correctamente"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cerrar_db(session)


@app.route("/partidos", methods=["POST"])
def crear_partido_route():
    session = conectar_db()
    try:
        data = request.get_json()
        fecha = data.get("fecha")
        hora = data.get("hora")
        equipo_local_id = data.get("equipo_local_id")
        equipo_visitante_id = data.get("equipo_visitante_id")
        if not fecha or not hora or not equipo_local_id or not equipo_visitante_id:
            return jsonify({"error": "Fecha, hora, equipo_local_id y equipo_visitante_id son requeridos"}), 400
        partido = crear_partido(session, fecha=fecha, hora=hora, equipo_local_id=equipo_local_id,
                               equipo_visitante_id=equipo_visitante_id)
        if not partido:
            return jsonify({"error": "No se pudo crear el partido"}), 400
        return jsonify(
            {"id": partido.id, "fecha": partido.fecha, "hora": partido.hora, "equipo_local_id": partido.equipo_local_id,
             "equipo_visitante_id": partido.equipo_visitante_id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cerrar_db(session)


@app.route("/partidos/<int:partido_id>", methods=["GET"])
def obtener_partido_route(partido_id):
    session = conectar_db()
    try:
        partido = obtener_partido_por_id(session, partido_id)
        if not partido:
            return jsonify({"error": "Partido no encontrado"}), 404
        return jsonify(
            {"id": partido.id, "fecha": partido.fecha, "hora": partido.hora, "equipo_local_id": partido.equipo_local_id,
             "equipo_visitante_id": partido.equipo_visitante_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cerrar_db(session)


@app.route("/estadisticas", methods=["POST"])
def crear_estadistica_route():
    session = conectar_db()
    try:
        data = request.get_json()
        jugador_id = data.get("jugador_id")
        partido_id = data.get("partido_id")
        puntos = data.get("puntos", 0)
        bloqueos = data.get("bloqueos", 0)
        saques = data.get("saques", 0)
        recepciones = data.get("recepciones", 0)
        if not jugador_id or not partido_id:
            return jsonify({"error": "jugador_id y partido_id son requeridos"}), 400
        estadistica = crear_estadistica(session, jugador_id=jugador_id, partido_id=partido_id, puntos=puntos,
                                         bloqueos=bloqueos, saques=saques, recepciones=recepciones)
        if not estadistica:
            return jsonify({"error": "No se pudo crear la estadística"}), 400
        return jsonify(
            {"id": estadistica.id, "jugador_id": estadistica.jugador_id, "partido_id": estadistica.partido_id,
             "puntos": estadistica.puntos, "bloqueos": estadistica.bloqueos, "saques": estadistica.saques,
             "recepciones": estadistica.recepciones}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cerrar_db(session)


@app.route("/estado_jugadores", methods=["POST"])
def crear_estado_jugador_route():
    session = conectar_db()
    try:
        data = request.get_json()
        jugador_id = data.get("jugador_id")
        partido_id = data.get("partido_id")
        disponible = data.get("disponible")
        lesion_tipo = data.get("lesion_tipo")
        if not jugador_id or not partido_id or disponible is None:
            return jsonify({"error": "jugador_id, partido_id y disponible son requeridos"}), 400
        estado_jugador = crear_estado_jugador(session, jugador_id=jugador_id, partido_id=partido_id,
                                               disponible=disponible, lesion_tipo=lesion_tipo)
        if not estado_jugador:
            return jsonify({"error": "No se pudo crear el estado del jugador"}), 400
        return jsonify(
            {"id": estado_jugador.id, "jugador_id": estado_jugador.jugador_id, "partido_id": estado_jugador.partido_id,
             "disponible": estado_jugador.disponible, "lesion_tipo": estado_jugador.lesion_tipo}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cerrar_db(session)


@app.route("/equipos/<int:equipo_id>/jugadores", methods=["GET"])
def obtener_jugadores_de_equipo_route(equipo_id):
    session = conectar_db()
    try:
        jugadores = obtener_jugadores_de_equipo(session, equipo_id)
        if not jugadores:
            return jsonify({"error": "No se pudieron obtener los jugadores"}), 400
        jugadores_json = [
            {"id": j.id, "nombre": j.nombre, "apellido": j.apellido, "posicion": j.posicion, "numero": j.numero} for j in
            jugadores]
        return jsonify(jugadores_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cerrar_db(session)


@app.route("/equipos/<int:equipo_id>/partidos", methods=["GET"])
def obtener_partidos_de_equipo_route(equipo_id):
    session = conectar_db()
    try:
        partidos = obtener_partidos_de_equipo(session, equipo_id)
        if not partidos:
            return jsonify({"error": "No se pudieron obtener los partidos"}), 400
        partidos_json = [
            {"id": p.id, "fecha": p.fecha, "hora": p.hora, "equipo_local_id": p.equipo_local_id,
             "equipo_visitante_id": p.equipo_visitante_id} for p in partidos]
        return jsonify(partidos_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cerrar_db(session)


@app.route("/partidos/<int:partido_id>/estadisticas", methods=["GET"])
def obtener_estadisticas_de_partido_route(partido_id):
    session = conectar_db()
    try:
        estadisticas = obtener_estadisticas_de_partido(session, partido_id)
        if not estadisticas:
            return jsonify({"error": "No se pudieron obtener las estadísticas"}), 400
        estadisticas_json = [
            {"id": e.id, "jugador_id": e.jugador_id, "puntos": e.puntos, "bloqueos": e.bloqueos, "saques": e.saques,
             "recepciones": e.recepciones} for e in estadisticas]
        return jsonify(estadisticas_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cerrar_db(session)


@app.route("/partidos/<int:partido_id>/estado_jugadores", methods=["GET"])
def obtener_estado_jugadores_de_partido_route(partido_id):
    session = conectar_db()
    try:
        estados_jugadores = obtener_estado_jugadores_de_partido(session, partido_id)
        if not estados_jugadores:
            return jsonify({"error": "No se pudo obtener el estado de los jugadores"}), 400
        estados_jugadores_json = [
            {"id": ej.id, "jugador_id": ej.jugador_id, "disponible": ej.disponible, "lesion_tipo": ej.lesion_tipo} for ej in
            estados_jugadores]
        return jsonify(estados_jugadores_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cerrar_db(session)


if __name__ == "__main__":
    app.run(debug=True)
