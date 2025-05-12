#   Código para las clases del proyecto de la Superliga de Voleibol de Bogotá

#   Carpeta: src/models

#   Archivo: src/models/jugador.py
class Jugador:
    def __init__(self, nombre, apellido, posicion, numero):
        self.nombre = nombre
        self.apellido = apellido
        self.posicion = posicion
        self.numero = numero

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.posicion}, #{self.numero})"

#   Archivo: src/models/equipo.py
class Equipo:
    def __init__(self, nombre, ciudad, entrenador):
        self.nombre = nombre
        self.ciudad = ciudad
        self.entrenador = entrenador
        self.jugadores = []  # Lista de objetos Jugador

    def agregar_jugador(self, jugador):
        self.jugadores.append(jugador)

    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"

#   Archivo: src/models/partido.py
class Partido:
    def __init__(self, fecha, hora, equipo_local, equipo_visitante):
        self.fecha = fecha
        self.hora = hora
        self.equipo_local = equipo_local
        self.equipo_visitante = equipo_visitante
        self.estadisticas = []  # Lista de objetos Estadistica

    def agregar_estadistica(self, estadistica):
        self.estadisticas.append(estadistica)

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante} ({self.fecha} {self.hora})"

# Archivo: src/models/estadistica.py
class Estadistica:
    def __init__(self, jugador, partido, puntos=0, bloqueos=0, saques=0, recepciones=0):
        self.jugador = jugador
        self.partido = partido
        self.puntos = puntos
        self.bloqueos = bloqueos
        self.saques = saques
        self.recepciones = recepciones

    def __str__(self):
        return f"{self.jugador.nombre} - Puntos: {self.puntos}, Bloqueos: {self.bloqueos}, Saques: {self.saques}, Recepciones: {self.recepciones}"

# Archivo: src/models/estado_jugador.py
class EstadoJugador:
    def __init__(self, jugador, partido, disponible, lesion_tipo=None):
        self.jugador = jugador
        self.partido = partido
        self.disponible = disponible
        self.lesion_tipo = lesion_tipo

    def __str__(self):
        estado = "Disponible" if self.disponible else f"Lesionado: {self.lesion_tipo}"
        return f"{self.jugador.nombre} en {self.partido}: {estado}"
