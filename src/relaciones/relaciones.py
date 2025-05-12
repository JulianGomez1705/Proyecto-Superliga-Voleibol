from sqlalchemy.orm import Session
from src.database import (
    conectar_db,
    cerrar_db,
    Jugador,
    Equipo,
    Partido,
    Estadistica,
    EstadoJugador,
)
from datetime import datetime


def crear_equipo(session: Session, nombre: str, ciudad: str, entrenador: str) -> Equipo:
    equipo = Equipo(nombre=nombre, ciudad=ciudad, entrenador=entrenador)
    session.add(equipo)
    session.commit()
    return equipo


def obtener_equipo_por_id(session: Session, equipo_id: int) -> Equipo | None:
    return session.query(Equipo).filter(Equipo.id == equipo_id).first()


def crear_jugador(session: Session, nombre: str, apellido: str, posicion: str, numero: int,
                  equipo_id: int) -> Jugador | None:
    equipo = obtener_equipo_por_id(session, equipo_id)
    if not equipo:
        print(f"No se puede crear el jugador. El equipo con ID {equipo_id} no existe.")
        return None
    jugador = Jugador(nombre=nombre, apellido=apellido, posicion=posicion, numero=numero, equipo=equipo)
    session.add(jugador)
    session.commit()
    return jugador


def obtener_jugador_por_id(session: Session, jugador_id: int) -> Jugador | None:
    return session.query(Jugador).filter(Jugador.id == jugador_id).first()


def actualizar_jugador(session: Session, jugador_id: int, nombre: str = None, apellido: str = None,
                       posicion: str = None, numero: int = None, equipo_id: int = None) -> Jugador | None:
    jugador = obtener_jugador_por_id(session, jugador_id)
    if not jugador:
        print(f"No se puede actualizar el jugador. El jugador con ID {jugador_id} no existe.")
        return None

    if nombre:
        jugador.nombre = nombre
    if apellido:
        jugador.apellido = apellido
    if posicion:
        jugador.posicion = posicion
    if numero:
        jugador.numero = numero
    if equipo_id:
        equipo = obtener_equipo_por_id(session, equipo_id)
        if not equipo:
            print(f"No se puede actualizar el jugador. El equipo con ID {equipo_id} no existe.")
            return None
        jugador.equipo = equipo
    session.commit()
    return jugador


def eliminar_jugador(session: Session, jugador_id: int) -> bool:
    jugador = obtener_jugador_por_id(session, jugador_id)
    if not jugador:
        print(f"No se puede eliminar el jugador. El jugador con ID {jugador_id} no existe.")
        return False
    session.delete(jugador)
    session.commit()
    return True


def crear_partido(session: Session, fecha: str, hora: str, equipo_local_id: int,
                  equipo_visitante_id: int) -> Partido | None:
    equipo_local = obtener_equipo_por_id(session, equipo_local_id)
    equipo_visitante = obtener_equipo_por_id(session, equipo_visitante_id)
    if not equipo_local:
        print(f"No se puede crear el partido. El equipo local con ID {equipo_local_id} no existe.")
        return None
    if not equipo_visitante:
        print(f"No se puede crear el partido. El equipo visitante con ID {equipo_visitante_id} no existe.")
        return None

    partido = Partido(fecha=fecha, hora=hora, equipo_local=equipo_local, equipo_visitante=equipo_visitante)
    session.add(partido)
    session.commit()
    return partido


def obtener_partido_por_id(session: Session, partido_id: int) -> Partido | None:
    return session.query(Partido).filter(Partido.id == partido_id).first()


def crear_estadistica(session: Session, jugador_id: int, partido_id: int, puntos: int = 0, bloqueos: int = 0,
                      saques: int = 0, recepciones: int = 0) -> Estadistica | None:
    jugador = obtener_jugador_por_id(session, jugador_id)
    partido = obtener_partido_por_id(session, partido_id)
    if not jugador:
        print(f"No se puede crear la estadística. El jugador con ID {jugador_id} no existe.")
        return None
    if not partido:
        print(f"No se puede crear la estadística. El partido con ID {partido_id} no existe.")
        return None
    estadistica = Estadistica(jugador=jugador, partido=partido, puntos=puntos, bloqueos=bloqueos, saques=saques,
                              recepciones=recepciones)
    session.add(estadistica)
    session.commit()
    return estadistica


def crear_estado_jugador(session: Session, jugador_id: int, partido_id: int, disponible: bool,
                         lesion_tipo: str = None) -> EstadoJugador | None:
    jugador = obtener_jugador_por_id(session, jugador_id)
    partido = obtener_partido_por_id(session, partido_id)
    if not jugador:
        print(f"No se puede crear el estado del jugador. El jugador con ID {jugador_id} no existe.")
        return None
    if not partido:
        print(f"No se puede crear el estado del jugador. El partido con ID {partido_id} no existe.")
        return None
    estado_jugador = EstadoJugador(jugador=jugador, partido=partido, disponible=disponible, lesion_tipo=lesion_tipo)
    session.add(estado_jugador)
    session.commit()
    return estado_jugador


def obtener_jugadores_de_equipo(session: Session, equipo_id: int) -> list[Jugador]:
    equipo = obtener_equipo_por_id(session, equipo_id)
    if not equipo:
        print(f"No se pueden obtener los jugadores. El equipo con ID {equipo_id} no existe.")
        return []
    return equipo.jugadores


def obtener_partidos_de_equipo(session: Session, equipo_id: int) -> list[Partido]:
    equipo = obtener_equipo_por_id(session, equipo_id)
    if not equipo:
        print(f"No se pueden obtener los partidos. El equipo con ID {equipo_id} no existe.")
        return []
    partidos_local = equipo.partidos_local
    partidos_visitante = equipo.partidos_visitante
    return partidos_local + partidos_visitante


def obtener_estadisticas_de_partido(session: Session, partido_id: int) -> list[Estadistica]:
    partido = obtener_partido_por_id(session, partido_id)
    if not partido:
        print(f"No se pueden obtener las estadísticas. El partido con ID {partido_id} no existe.")
        return []
    return partido.estadisticas


def obtener_estado_jugadores_de_partido(session: Session, partido_id: int) -> list[EstadoJugador]:
    partido = obtener_partido_por_id(session, partido_id)
    if not partido:
        print(f"No se puede obtener el estado de los jugadores. El partido con ID {partido_id} no existe.")
        return []
    return partido.estado_jugadores


def main():
    session = conectar_db()
    if not session:
        return

    try:
        print("\n--- Creación de equipos ---")
        equipo1 = crear_equipo(session, nombre="Los Leones", ciudad="Bogotá", entrenador="Carlos Pérez")
        equipo2 = crear_equipo(session, nombre="Las Panteras", ciudad="Cali", entrenador="Ana García")
        if equipo1 and equipo2:
            print(f"Equipos creados: {equipo1}, {equipo2}")

        print("\n--- Creación de jugadores ---")
        jugador1 = crear_jugador(session, nombre="Juan", apellido="Pérez", posicion="Opuesto", numero=1,
                                 equipo_id=equipo1.id)
        jugador2 = crear_jugador(session, nombre="María", apellido="Gómez", posicion="Central", numero=5,
                                 equipo_id=equipo1.id)
        jugador3 = crear_jugador(session, nombre="Andrés", apellido="Rodríguez", posicion="Libero", numero=10,
                                 equipo_id=equipo2.id)
        if jugador1 and jugador2 and jugador3:
            print(f"Jugadores creados: {jugador1}, {jugador2}, {jugador3}")

        print("\n--- Actualización de jugador ---")
        jugador_actualizado = actualizar_jugador(session, jugador_id=jugador1.id, nombre="Juan Carlos", numero=2)
        if jugador_actualizado:
            print(f"Jugador actualizado: {jugador_actualizado}")

        print("\n--- Creación de partido ---")
        partido1 = crear_partido(session, fecha="2024-05-20", hora="8:00 PM", equipo_local_id=equipo1.id,
                                 equipo_visitante_id=equipo2.id)
        if partido1:
            print(f"Partido creado: {partido1}")

        print("\n--- Creación de estadísticas ---")
        estadistica1 = crear_estadistica(session, jugador_id=jugador1.id, partido_id=partido1.id, puntos=20, bloqueos=5)
        estadistica2 = crear_estadistica(session, jugador_id=jugador2.id, partido_id=partido1.id, puntos=10, bloqueos=2)
        if estadistica1 and estadistica2:
            print(f"Estadísticas creadas: {estadistica1}, {estadistica2}")

        print("\n--- Creación de estado de jugador ---")
        estado_jugador1 = crear_estado_jugador(session, jugador_id=jugador1.id, partido_id=partido1.id, disponible=True)
        estado_jugador2 = crear_estado_jugador(session, jugador_id=jugador3.id, partido_id=partido1.id,
                                               disponible=False, lesion_tipo="Esguince de tobillo")
        if estado_jugador1 and estado_jugador2:
            print(f"Estados de jugador creados: {estado_jugador1}, {estado_jugador2}")

        print("\n--- Obtener jugadores de un equipo ---")
        jugadores_equipo1 = obtener_jugadores_de_equipo(session, equipo1.id)
        if jugadores_equipo1:
            print(f"Jugadores del equipo {equipo1.nombre}:")
            for jugador in jugadores_equipo1:
                print(jugador)

        print("\n--- Obtener partidos de un equipo ---")
        partidos_equipo1 = obtener_partidos_de_equipo(session, equipo1.id)
        if partidos_equipo1:
            print(f"Partidos del equipo {equipo1.nombre}:")
            for partido in partidos_equipo1:
                print(partido)

        print("\n--- Obtener estadísticas de un partido ---")
        estadisticas_partido1 = obtener_estadisticas_de_partido(session, partido1.id)
        if estadisticas_partido1:
            print(f"Estadísticas del partido {partido1}:")
            for estadistica in estadisticas_partido1:
                print(estadistica)

        print("\n--- Obtener estado de jugadores de un partido ---")
        estados_partido1 = obtener_estado_jugadores_de_partido(session, partido1.id)
        if estados_partido1:
            print(f"Estado de jugadores del partido {partido1}:")
            for estado in estados_partido1:
                print(estado)

        print("\n--- Eliminar jugador ---")
        eliminado = eliminar_jugador(session, jugador3.id)
        if eliminado:
            print(f"Jugador con ID {jugador3.id} eliminado correctamente.")

        jugadores = session.query(Jugador).all()
        print("\n--- Todos los jugadores ---")
        for jugador in jugadores:
            print(jugador)

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        session.rollback()
    finally:
        cerrar_db(session)


if __name__ == "__main__":
    main()
