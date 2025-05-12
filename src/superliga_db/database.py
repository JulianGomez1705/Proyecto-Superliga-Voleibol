
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "mysql://tu_usuario:tu_contraseña@localhost/nombre_de_la_base_de_datos"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

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


class Jugador(Base):
    __tablename__ = "jugador"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    posicion = Column(String(50), nullable=False)
    numero = Column(Integer, nullable=False)

    equipo_id = Column(Integer, ForeignKey("equipo.id"))
    equipo = relationship("Equipo", back_populates="jugadores")
    estadisticas = relationship("Estadistica", back_populates="jugador")
    estado_jugadores = relationship("EstadoJugador", back_populates="jugador")

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.posicion}, #{self.numero})"


class Equipo(Base):
    __tablename__ = "equipo"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=False)
    entrenador = Column(String(100), nullable=False)

    jugadores = relationship("Jugador", back_populates="equipo")
    partidos_local = relationship("Partido", back_populates="equipo_local")
    partidos_visitante = relationship("Partido", back_populates="equipo_visitante")

    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"


class Partido(Base):
    __tablename__ = "partido"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(String(20), nullable=False)
    hora = Column(String(20), nullable=False)

    equipo_local_id = Column(Integer, ForeignKey("equipo.id"))
    equipo_visitante_id = Column(Integer, ForeignKey("equipo.id"))
    equipo_local = relationship("Equipo", foreign_keys=[equipo_local_id], back_populates="partidos_local")
    equipo_visitante = relationship("Equipo", foreign_keys=[equipo_visitante_id], back_populates="partidos_visitante")

    estadisticas = relationship("Estadistica", back_populates="partido")
    estado_jugadores = relationship("EstadoJugador", back_populates="partido")

    def __str__(self):
        return f"{self.equipo_local.nombre} vs {self.equipo_visitante.nombre} ({self.fecha} {self.hora})"


class Estadistica(Base):
    __tablename__ = "estadistica"

    id = Column(Integer, primary_key=True, index=True)
    jugador_id = Column(Integer, ForeignKey("jugador.id"))
    partido_id = Column(Integer, ForeignKey("partido.id"))
    puntos = Column(Integer, default=0)
    bloqueos = Column(Integer, default=0)
    saques = Column(Integer, default=0)
    recepciones = Column(Integer, default=0)

    jugador = relationship("Jugador", back_populates="estadisticas")
    partido = relationship("Partido", back_populates="estadisticas")

    def __str__(self):
        return f"{self.jugador.nombre} - Puntos: {self.puntos}, Bloqueos: {self.bloqueos}, Saques: {self.saques}, Recepciones: {self.recepciones}"


class EstadoJugador(Base):
    __tablename__ = "estado_jugador"

    id = Column(Integer, primary_key=True, index=True)
    jugador_id = Column(Integer, ForeignKey("jugador.id"))
    partido_id = Column(Integer, ForeignKey("partido.id"))
    disponible = Column(Boolean, nullable=False)
    lesion_tipo = Column(String(100), nullable=True)

    jugador = relationship("Jugador", back_populates="estado_jugadores")
    partido = relationship("Partido", back_populates="estado_jugadores")

    def __str__(self):
        estado = "Disponible" if self.disponible else f"Lesionado: {self.lesion_tipo}"
        return f"{self.jugador.nombre} en {self.partido}: {estado}"


Base.metadata.create_all(engine)

if __name__ == "__main__":

    session = conectar_db()
    if session:
        try:

            equipo1 = Equipo(nombre="Los Leones", ciudad="Bogotá", entrenador="Carlos Pérez")
            equipo2 = Equipo(nombre="Las Panteras", ciudad="Cali", entrenador="Ana García")
            session.add_all([equipo1, equipo2])
            session.commit()


            jugador1 = Jugador(nombre="Juan", apellido="Pérez", posicion="Opuesto", numero=1, equipo=equipo1)
            jugador2 = Jugador(nombre="María", apellido="Gómez", posicion="Central", numero=5, equipo=equipo1)
            jugador3 = Jugador(nombre="Andrés", apellido="Rodríguez", posicion="Libero", numero=10, equipo=equipo2)
            session.add_all([jugador1, jugador2, jugador3])
            session.commit()


            partido1 = Partido(fecha="2024-05-20", hora="8:00 PM", equipo_local=equipo1, equipo_visitante=equipo2)
            session.add(partido1)
            session.commit()


            estadistica1 = Estadistica(jugador=jugador1, partido=partido1, puntos=20, bloqueos=5)
            estadistica2 = Estadistica(jugador=jugador2, partido=partido1, puntos=10, bloqueos=2)
            session.add_all([estadistica1, estadistica2])
            session.commit()


            estado_jugador1 = EstadoJugador(jugador=jugador1, partido=partido1, disponible=True)
            estado_jugador2 = EstadoJugador(jugador=jugador3, partido=partido1, disponible=False,
                                            lesion_tipo="Esguince de tobillo")
            session.add_all([estado_jugador1, estado_jugador2])
            session.commit()


            print(f"Jugadores del equipo {equipo1.nombre}:")
            for jugador in equipo1.jugadores:
                print(jugador)


            print(f"Partidos de {equipo1.nombre} como local:")
            for partido in equipo1.partidos_local:
                print(partido)


            print(f"Estadísticas del partido: {partido1}:")
            for estadistica in partido1.estadisticas:
                print(estadistica)


            print(f"Estado de los jugadores en el partido: {partido1}")
            for estado in partido1.estado_jugadores:
                print(estado)


            jugadores = session.query(Jugador).all()
            print("\nTodos los jugadores:")
            for jugador in jugadores:
                print(jugador)

        except Exception as e:
            session.rollback()
            print(f"Error durante la transacción: {e}")
        finally:
            cerrar_db(session)
