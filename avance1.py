class NM:
    def __init__(self, llave, valor) -> None:
        # Inicializa un nodo con una llave, un valor y una referencia al siguiente nodo
        self.llave = llave
        self.valor = valor
        self.liga = None
    
    def asignaLiga(self, nodoALigar) -> None:
        # Asigna el siguiente nodo en la lista
        self.liga = nodoALigar

    def asignaValor(self, valor) -> None:
        # Asigna un nuevo valor al nodo
        self.valor = valor

    def asignaLlave(self, llave):
        # Asigna una nueva llave al nodo
        self.llave = llave

    def retornaLiga(self):
        # Retorna el siguiente nodo en la lista
        return self.liga
    
    def retornaValor(self):
        # Retorna el valor almacenado en el nodo
        return self.valor
    
    def retornaLlave(self):
        # Retorna la llave almacenada en el nodo
        return self.llave

class HashMap:
    def __init__(self):
        # Inicializa un HashMap con un número fijo de buckets (cubos)
        # Complejidad: O(n), donde n es el número de buckets
        self.conteo_buckets = 10
        self.buckets = [None] * self.conteo_buckets

    def obtener(self, llave):
        # Obtiene el nodo asociado con una llave
        # Complejidad: O(1) en promedio (debido a la búsqueda en una lista enlazada en un bucket específico)
        hash_reducido = self.__obtener_hash_reducido(llave)
        iterador = self.buckets[hash_reducido]
        while iterador is not None and llave != iterador.retornaLlave():
            iterador = iterador.retornaLiga()
        if iterador is None:
            raise KeyError(f"No se encontró la llave {llave}")
        return iterador
    
    def contiene(self, llave):
        # Verifica si una llave está en el HashMap
        # Complejidad: O(1) en promedio (se basa en obtener que ya es O(1) en promedio)
        try:
            self.obtener(llave)
        except KeyError:
            return False
        return True
    
    def poner(self, llave, valor):
        # Inserta o actualiza un par llave-valor en el HashMap
        # Complejidad: O(1) en promedio (debido a la inserción en la lista enlazada en un bucket específico)
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
        # Calcula un valor hash reducido basado en el tamaño de los buckets
        # Complejidad: O(1) (la operación de hash y módulo son constantes)
        valor_hash = hash(llave)
        hash_reducido = valor_hash % self.conteo_buckets
        return hash_reducido
    
    def contar(self):
        # Cuenta el número total de pares llave-valor en el HashMap
        # Complejidad: O(n) donde n es el número total de nodos (suma de todos los buckets)
        conteo = 0
        for nodo in self.buckets:
            iterador = nodo
            while iterador is not None:
                conteo += 1
                iterador = iterador.retornaLiga()
        return conteo

    def redimensionar(self, nuevo_tamano):
        # Redimensiona el tamaño del HashMap y redistribuye los elementos
        # Complejidad: O(n) donde n es el número total de nodos (debe recorrer todos los nodos existentes)
        if nuevo_tamano <= 0:
            raise ValueError("El nuevo tamaño debe ser mayor que cero.")
        
        nuevo_buckets = [None] * nuevo_tamano
        
        for bucket in self.buckets:
            iterador = bucket
            while iterador is not None:
                llave = iterador.retornaLlave()
                valor = iterador.retornaValor()
                siguiente_nodo = iterador.retornaLiga()
                hash_reducido = hash(llave) % nuevo_tamano
                
                if nuevo_buckets[hash_reducido] is None:
                    nuevo_buckets[hash_reducido] = NM(llave, valor)
                else:
                    nodo_actual = nuevo_buckets[hash_reducido]
                    while nodo_actual.retornaLiga() is not None:
                        nodo_actual = nodo_actual.retornaLiga()
                    nodo_actual.asignaLiga(NM(llave, valor))

                iterador = siguiente_nodo
        
        self.buckets = nuevo_buckets
        self.conteo_buckets = nuevo_tamano

    def eliminar_clave(self, llave):
        # Elimina el par llave-valor del HashMap
        # Complejidad: O(1) en promedio (búsqueda en la lista enlazada en un bucket específico)
        hash_reducido = self.__obtener_hash_reducido(llave)
        iterador = self.buckets[hash_reducido]
        anterior = None

        while iterador is not None and llave != iterador.retornaLlave():
            anterior = iterador
            iterador = iterador.retornaLiga()
        
        if iterador is None:
            raise KeyError(f"No se encontró la llave {llave}")

        if anterior is None:
            self.buckets[hash_reducido] = iterador.retornaLiga()
        else:
            anterior.asignaLiga(iterador.retornaLiga())

    def fusionar(self, otro_hashmap):
        # Fusiona otro HashMap en el HashMap actual
        # Complejidad: O(n) donde n es el número total de nodos en el otro HashMap (debe recorrer todos los nodos del otro HashMap)
        if not isinstance(otro_hashmap, HashMap):
            raise TypeError("El parámetro debe ser una instancia de HashMap.")
        
        for i in range(otro_hashmap.conteo_buckets):
            nodo = otro_hashmap.buckets[i]
            while nodo is not None:
                self.poner(nodo.retornaLlave(), nodo.retornaValor())
                nodo = nodo.retornaLiga()

    def vaciar(self):
        # Limpia todos los pares llave-valor del HashMap
        # Complejidad: O(n) donde n es el número total de nodos (elimina todos los nodos)
        self.buckets = [None] * self.conteo_buckets

class RecomendadorMusical:
    def __init__(self):
        # Inicializa un recomendador musical con un HashMap para recomendaciones
        # Complejidad: O(1)
        self.recomendaciones = HashMap()
    
    def agregar_cancion(self, estado_emocional, cancion):
        # Agrega una canción a una lista de canciones asociada a un estado emocional
        # Complejidad: O(1) en promedio (debido a las operaciones en el HashMap)
        if not self.recomendaciones.contiene(estado_emocional):
            self.recomendaciones.poner(estado_emocional, [])
        canciones = self.recomendaciones.obtener(estado_emocional).retornaValor()
        canciones.append(cancion)
        self.recomendaciones.obtener(estado_emocional).asignaValor(canciones)
    
    def recomendar_canciones(self, estado_emocional):
        # Devuelve una lista de canciones basadas en el estado emocional proporcionado
        # Complejidad: O(1) en promedio (debido a las operaciones en el HashMap)
        try:
            canciones = self.recomendaciones.obtener(estado_emocional).retornaValor()
            return canciones
        except KeyError:
            return []

    def vaciar_recomendaciones(self):
        # Limpia todas las recomendaciones de canciones
        # Complejidad: O(n) donde n es el número total de nodos en el HashMap (vacía todas las recomendaciones)
        self.recomendaciones.vaciar()

def main():
    # Crear una instancia del recomendador musical
    recomendador = RecomendadorMusical()

    # Agregar canciones para diferentes estados emocionales
    recomendador.agregar_cancion("feliz", "Vivir Mi Vida - Marc Anthony")
    recomendador.agregar_cancion("feliz", "La Bicicleta - Shakira ft. Carlos Vives")
    recomendador.agregar_cancion("triste", "Día de Enero - Shakira")
    recomendador.agregar_cancion("triste", "Te Dejo Libre - Los Ángeles Azules ft. Rubén Albarrán")
    recomendador.agregar_cancion("energético", "
