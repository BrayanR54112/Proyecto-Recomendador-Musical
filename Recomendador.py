class NM:
    def __init__(self, llave, valor) -> None:
        self.llave = llave
        self.valor = valor
        self.liga = None
    
    def asignaLiga(self, nodoALigar) -> None:
        self.liga = nodoALigar

    def asignaValor(self, valor) -> None:
        self.valor = valor

    def asignaLlave(self, llave):
        self.llave = llave

    def retornaLiga(self):
        return self.liga
    
    def retornaValor(self):
        return self.valor
    
    def retornaLlave(self):
        return self.llave

class HashMap:
    def __init__(self):
        self.conteo_buckets = 10
        self.buckets = [None] * self.conteo_buckets

    def obtener(self, llave):
        hash_reducido = self.__obtener_hash_reducido(llave)
        iterador = self.buckets[hash_reducido]
        while iterador is not None and llave != iterador.retornaLlave():
            iterador = iterador.retornaLiga()
        if iterador is None:
            raise KeyError(f"No se encontró la llave {llave}")
        return iterador
    
    def contiene(self, llave):
        try:
            self.obtener(llave)
        except KeyError:
            return False
        return True
    
    def poner(self, llave, valor):
        nodo_nuevo = NM(llave, valor)
        hash_reducido = self.__obtener_hash_reducido(llave)

        if self.buckets[hash_reducido] is None:
            self.buckets[hash_reducido] = nodo_nuevo
            return
        
        iterador = self.buckets[hash_reducido]
        anterior = None

        while iterador is not None and llave != iterador.retornaLlave():
            anterior = iterador
            iterador = iterador.retornaLiga()
        
        if iterador is None:
            anterior.asignaLiga(nodo_nuevo)
        else:
            iterador.asignaValor(valor)

    def __obtener_hash_reducido(self, llave):
        valor_hash = hash(llave)
        hash_reducido = valor_hash % self.conteo_buckets
        return hash_reducido
    
    def contar(self):
        conteo = 0
        for nodo in self.buckets:
            iterador = nodo
            while iterador is not None:
                conteo += 1
                iterador = iterador.retornaLiga()
        return conteo

    def vaciar(self):
        self.buckets = [None] * self.conteo_buckets


class NodoCancion:
    def __init__(self, nombre, artista):
        self.nombre = nombre
        self.artista = artista
        self.conexiones = []

    def agregar_conexion(self, otra_cancion):
        if otra_cancion not in self.conexiones:
            self.conexiones.append(otra_cancion)

    def obtener_artista(self):
        return self.artista

class GrafoCanciones:
    def __init__(self):
        self.nodos = {}

    def agregar_cancion(self, nombre, artista):
        if nombre not in self.nodos:
            self.nodos[nombre] = NodoCancion(nombre, artista)

    def conectar_canciones(self, nombre1, nombre2):
        if nombre1 in self.nodos and nombre2 in self.nodos:
            self.nodos[nombre1].agregar_conexion(self.nodos[nombre2])
            self.nodos[nombre2].agregar_conexion(self.nodos[nombre1])

    def obtener_recomendaciones_por_artista(self, artista):
        return [nodo.nombre for nodo in self.nodos.values() if nodo.obtener_artista() == artista]


class Pila:
    def __init__(self):
        self.canciones = []

    def apilar(self, cancion):
        self.canciones.append(cancion)

    def desapilar(self):
        if not self.esta_vacia():
            return self.canciones.pop()
        raise IndexError("La pila está vacía")

    def esta_vacia(self):
        return len(self.canciones) == 0

    def mostrar(self):
        return self.canciones


class RecomendadorMusical:
    def __init__(self):
        self.recomendaciones = HashMap()
        self.grafo_canciones = GrafoCanciones()
    
    def agregar_cancion(self, estado_emocional, cancion, artista):
        if not self.recomendaciones.contiene(estado_emocional):
            self.recomendaciones.poner(estado_emocional, [])
        canciones = self.recomendaciones.obtener(estado_emocional).retornaValor()
        canciones.append(cancion)
        self.recomendaciones.obtener(estado_emocional).asignaValor(canciones)
        self.grafo_canciones.agregar_cancion(cancion, artista)  # Agregar la canción al grafo
    
    def recomendar_canciones(self, estado_emocional):
        try:
            canciones = self.recomendaciones.obtener(estado_emocional).retornaValor()
            return canciones
        except KeyError:
            return []

    def conectar_canciones(self, cancion1, cancion2):
        self.grafo_canciones.conectar_canciones(cancion1, cancion2)

    def recomendar_por_artista(self, artista):
        return self.grafo_canciones.obtener_recomendaciones_por_artista(artista)
    
    def vaciar_recomendaciones(self):
        self.recomendaciones.vaciar()


# Ejemplo de uso con canciones agregadas y recomendaciones basadas en artista
def main():
    recomendador = RecomendadorMusical()
    pila = Pila()  # Crear una instancia de la pila

    # Agregar canciones para diferentes estados emocionales
    recomendador.agregar_cancion("feliz", "Vivir Mi Vida - Marc Anthony", "Marc Anthony")
    recomendador.agregar_cancion("feliz", "La Bicicleta - Shakira ft. Carlos Vives", "Shakira")
    recomendador.agregar_cancion("feliz", "Hips Don't Lie - Shakira", "Shakira")
    recomendador.agregar_cancion("triste", "Condor Herido - Diomedes Diaz", "Diomedes Diaz")
    recomendador.agregar_cancion("triste", "Era Como Yo - Diomedes Diaz", "Diomedes Diaz")
    recomendador.agregar_cancion("energético", "Vital - Crudo Means Raw", "Crudo Means Raw")
    recomendador.agregar_cancion("energético", "We Will Rock You - Queen", "Queen")
    recomendador.agregar_cancion("energético", "Don't Stop Me Now - Queen", "Queen")
    recomendador.agregar_cancion("relajado", "Sunflower - Post Malone", "Post Malone")
    recomendador.agregar_cancion("relajado", "Perfect - Ed Sheeran", "Ed Sheeran")
    recomendador.agregar_cancion("relajado", "Tu Cumpleaños - Diomedes Diaz", "Diomedes Diaz")

    # Leer el estado emocional del usuario desde la entrada estándar
    estado_emocional = input("¿Cómo te sientes hoy? (ej. feliz, triste, energético, relajado): ").strip().lower()

    # Recomendar canciones basadas en el estado emocional
    canciones_recomendadas = recomendador.recomendar_canciones(estado_emocional)
    
    if canciones_recomendadas:
        print(f"\nRecomendaciones si estás {estado_emocional}:")
        for i, cancion in enumerate(canciones_recomendadas, 1):
            print(f"{i}. {cancion}")  # Enumerar las canciones

        # Permitir al usuario apilar canciones
        while True:
            seleccion = input("\nElige el número de la canción que quieres apilar (o 'siguiente' para terminar): ").strip().lower()
            if seleccion == 'siguiente':
                break
            try:
                index = int(seleccion) - 1
                if 0 <= index < len(canciones_recomendadas):
                    pila.apilar(canciones_recomendadas[index])
                    print(f"Apilada: {canciones_recomendadas[index]}")
                else:
                    print("Número fuera de rango.")
            except ValueError:
                print("Por favor, ingresa un número válido.")

    else:
        print(f"No hay recomendaciones para el estado {estado_emocional}.")

    # Recomendaciones por conexión basada en artista
    artista = input("\nEscribe el nombre de algun artista para recibir recomendaciones ").strip()
    recomendaciones_artista = recomendador.recomendar_por_artista(artista)
    
    if recomendaciones_artista:
        print(f"\nCanciones de {artista}:")
        for i, recomendada in enumerate(recomendaciones_artista, 1):
            print(f"{i}. {recomendada}")
        
        # Permitir al usuario apilar canciones recomendadas por artista
        while True:
            seleccion_artista = input("\nElige el número de la canción que quieres apilar (o 'finalizar' para escuchar las canciones elegidas ): ").strip().lower()
            if seleccion_artista == 'finalizar':
                break
            try:
                index_artista = int(seleccion_artista) - 1
                if 0 <= index_artista < len(recomendaciones_artista):
                    pila.apilar(recomendaciones_artista[index_artista])
                    print(f"Apilada: {recomendaciones_artista[index_artista]}")
                else:
                    print("Número fuera de rango.")
            except ValueError:
                print("Por favor, ingresa un número válido.")

    else:
        print(f"No hay canciones recomendadas del artista {artista}.")

    # Mostrar la pila de canciones apiladas
    if not pila.esta_vacia():
        print("\nCanciones apiladas:")
        for i, cancion in enumerate(pila.mostrar(), 1):
            print(f"{i}. {cancion}")
    else:
        print("No hay canciones apiladas.")

    # Vaciar recomendaciones después de mostrar las recomendaciones
    recomendador.vaciar_recomendaciones()

main()


